"""
REST API routes for the trading bot.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import get_db, Trade, PerformanceSnapshot
from backend.exchange.manager import exchange_manager
from backend.trading.engine import engine
from backend.backtesting.engine import run_backtest as _run_backtest

log = logging.getLogger(__name__)
router = APIRouter()


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class ExchangeConfig(BaseModel):
    exchange:   str
    api_key:    str
    api_secret: str
    passphrase: Optional[str] = ""
    testnet:    bool = True
    mode:       str  = "futures"   # spot | futures | margin


class TradingConfig(BaseModel):
    mode:            str   = "paper"   # paper | live
    max_open_trades: int   = 5
    risk_per_trade:  float = 0.02
    stop_loss_pct:   float = 0.05
    take_profit_pct: float = 0.10


class StrategyConfig(BaseModel):
    hft_enabled:        bool  = True
    ai_enabled:         bool  = True
    dca_enabled:        bool  = True
    grid_enabled:       bool  = False
    gomale_enabled:     bool  = True
    hft_capital:        float = 0.40
    ai_capital:         float = 0.35
    dca_capital:        float = 0.25
    grid_capital:       float = 0.20
    gomale_capital:     float = 0.25
    ai_confidence:      float = 0.75
    gomale_confidence:  float = 0.70


class BacktestConfig(BaseModel):
    symbol:           str   = "SOL"     # SOL | ETH
    starting_capital: float = 1000.0
    timeframe:        str   = "6months"
    risk_per_trade:   float = 10.0      # percent
    confidence_gate:  float = 70.0      # percent


# ── Exchange endpoints ────────────────────────────────────────────────────────

@router.post("/api/exchange/connect")
async def connect_exchange(cfg: ExchangeConfig):
    """Connect to an exchange with the provided credentials."""
    ok = await exchange_manager.connect(
        cfg.exchange, cfg.api_key, cfg.api_secret,
        cfg.passphrase, cfg.testnet
    )
    if not ok:
        raise HTTPException(status_code=400, detail=f"Failed to connect to {cfg.exchange}")
    settings.ACTIVE_EXCHANGE = cfg.exchange
    return {"status": "connected", "exchange": cfg.exchange, "testnet": cfg.testnet}


@router.post("/api/connection/test")
async def test_connection(cfg: ExchangeConfig):
    """Test exchange credentials without saving them."""
    ok = await exchange_manager.connect(
        cfg.exchange, cfg.api_key, cfg.api_secret,
        cfg.passphrase, cfg.testnet
    )
    if not ok:
        return {"success": False, "message": f"Could not connect to {cfg.exchange}"}

    balance = await exchange_manager.fetch_balance(cfg.exchange)
    return {
        "success": True,
        "exchange": cfg.exchange,
        "balance_usdt": balance.get("usdt", 0),
    }


@router.get("/api/exchange/status")
async def exchange_status():
    connected = {name: exchange_manager.is_connected(name)
                 for name in ["bybit", "binance", "kucoin", "okx"]}
    return {"exchanges": connected, "active": settings.ACTIVE_EXCHANGE}


# ── Balance / portfolio ───────────────────────────────────────────────────────

@router.get("/api/balance")
async def get_balance():
    if not exchange_manager.is_connected(settings.ACTIVE_EXCHANGE):
        return {"usdt": engine.stats.get("balance", 0), "paper": True}
    balance = await exchange_manager.fetch_balance()
    positions = await exchange_manager.fetch_positions()
    return {
        "usdt":      balance.get("usdt", 0),
        "free":      balance.get("free", {}).get("USDT", 0),
        "used":      balance.get("used", {}).get("USDT", 0),
        "positions": positions,
        "paper":     settings.TRADING_MODE == "paper",
    }


# ── Trading controls ──────────────────────────────────────────────────────────

@router.post("/api/trading/start")
async def start_trading(cfg: Optional[TradingConfig] = None):
    if engine.running:
        return {"status": "already_running"}

    if cfg:
        settings.TRADING_MODE = cfg.mode

    await engine.start()
    return {"status": "started", "mode": settings.TRADING_MODE}


@router.post("/api/trading/stop")
async def stop_trading():
    await engine.stop()
    return {"status": "stopped"}


@router.get("/api/status")
async def get_status():
    risk_stats = engine.risk.stats()
    return {
        **engine.stats,
        **risk_stats,
        "mode":       settings.TRADING_MODE,
        "strategies": {
            "hft":    settings.ENABLE_HFT,
            "ai":     settings.ENABLE_AI_MULTI,
            "dca":    settings.ENABLE_ZERO_LOSS,
            "grid":   settings.ENABLE_GRID,
            "gomale": settings.ENABLE_GOMALE,
        },
    }


# ── Config ────────────────────────────────────────────────────────────────────

@router.post("/api/config/save")
async def save_config(config: dict = Body(...)):
    """Save arbitrary config blob to the engine settings at runtime."""
    updated = []

    if "trading" in config:
        t = config["trading"]
        if "mode" in t:
            settings.TRADING_MODE = t["mode"]
            updated.append("trading.mode")
        if "max_open_trades" in t:
            settings.MAX_OPEN_TRADES = int(t["max_open_trades"])
        if "stop_loss_pct" in t:
            settings.STOP_LOSS_PCT = float(t["stop_loss_pct"])
        if "take_profit_pct" in t:
            settings.TAKE_PROFIT_PCT = float(t["take_profit_pct"])

    if "strategies" in config:
        s = config["strategies"]
        if "hft_enabled"  in s: settings.ENABLE_HFT       = bool(s["hft_enabled"])
        if "ai_enabled"   in s: settings.ENABLE_AI_MULTI  = bool(s["ai_enabled"])
        if "dca_enabled"  in s: settings.ENABLE_ZERO_LOSS = bool(s["dca_enabled"])
        if "grid_enabled" in s: settings.ENABLE_GRID      = bool(s["grid_enabled"])
        if "ai_confidence"in s: settings.AI_CONFIDENCE_THRESHOLD = float(s["ai_confidence"])
        updated.append("strategies")

    return {"status": "saved", "updated": updated}


@router.post("/api/strategies/update")
async def update_strategies(cfg: StrategyConfig):
    settings.ENABLE_HFT       = cfg.hft_enabled
    settings.ENABLE_AI_MULTI  = cfg.ai_enabled
    settings.ENABLE_ZERO_LOSS = cfg.dca_enabled
    settings.ENABLE_GRID      = cfg.grid_enabled
    settings.ENABLE_GOMALE    = cfg.gomale_enabled
    settings.HFT_CAPITAL_PCT  = cfg.hft_capital
    settings.AI_CAPITAL_PCT   = cfg.ai_capital
    settings.DCA_CAPITAL_PCT  = cfg.dca_capital
    settings.GRID_CAPITAL_PCT = cfg.grid_capital
    settings.GOMALE_CAPITAL_PCT = cfg.gomale_capital
    settings.AI_CONFIDENCE_THRESHOLD    = cfg.ai_confidence
    settings.GOMALE_CONFIDENCE_THRESHOLD = cfg.gomale_confidence

    # Sync strategy objects
    for strategy in engine.strategies:
        if strategy.name == "hft_scalping":
            strategy.enabled     = cfg.hft_enabled
            strategy.capital_pct = cfg.hft_capital
        elif strategy.name == "ai_multi":
            strategy.enabled     = cfg.ai_enabled
            strategy.capital_pct = cfg.ai_capital
            strategy.threshold   = cfg.ai_confidence
        elif strategy.name == "zero_loss_dca":
            strategy.enabled     = cfg.dca_enabled
            strategy.capital_pct = cfg.dca_capital
        elif strategy.name == "grid":
            strategy.enabled     = cfg.grid_enabled
            strategy.capital_pct = cfg.grid_capital
        elif strategy.name == "gomale":
            strategy.enabled     = cfg.gomale_enabled
            strategy.capital_pct = cfg.gomale_capital
            strategy.threshold   = cfg.gomale_confidence

    return {"status": "updated"}


# ── Backtest ───────────────────────────────────────────────────────────────────

@router.post("/api/backtest/run")
async def backtest_run(cfg: BacktestConfig):
    """
    Run a Gomale backtest for a single symbol and return full results.
    To run both SOL and ETH call this endpoint twice in parallel from the frontend.
    """
    symbol = cfg.symbol.upper()
    if symbol not in ("SOL", "ETH"):
        raise HTTPException(status_code=400, detail="symbol must be SOL or ETH")

    result = _run_backtest(symbol, {
        "starting_capital": cfg.starting_capital,
        "timeframe":        cfg.timeframe,
        "risk_per_trade":   cfg.risk_per_trade,
        "confidence_gate":  cfg.confidence_gate,
    })

    return {
        "symbol": symbol,
        "metrics": {
            "finalBalance":  result.metrics.final_balance,
            "totalReturn":   result.metrics.total_return,
            "winRate":       result.metrics.win_rate,
            "wins":          result.metrics.wins,
            "losses":        result.metrics.losses,
            "totalTrades":   result.metrics.total_trades,
            "avgWin":        result.metrics.avg_win,
            "avgLoss":       result.metrics.avg_loss,
            "profitFactor":  result.metrics.profit_factor,
            "maxDrawdown":   result.metrics.max_drawdown,
            "sharpeRatio":   result.metrics.sharpe_ratio,
        },
        "equityCurve": [
            {"date": p.date, "equity": p.equity, "buyHold": p.buy_hold}
            for p in result.equity_curve
        ],
        "trades": [
            {
                "date":       t.date,
                "type":       t.type,
                "price":      t.price,
                "size":       t.size,
                "pnl":        t.pnl,
                "confidence": t.confidence,
            }
            for t in result.trades
        ],
        "monthlyReturns": [
            {"month": m.month, "return": m.ret}
            for m in result.monthly_returns
        ],
    }


# ── Trades ────────────────────────────────────────────────────────────────────

@router.get("/api/trades/active")
async def get_active_trades(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Trade).where(Trade.status == "open").order_by(desc(Trade.opened_at)).limit(50)
    )
    trades = result.scalars().all()
    return [_trade_to_dict(t) for t in trades]


@router.get("/api/trades/history")
async def get_trade_history(
    limit: int = 50,
    strategy: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    q = select(Trade).where(Trade.status == "closed").order_by(desc(Trade.closed_at))
    if strategy:
        q = q.where(Trade.strategy == strategy)
    q = q.limit(limit)
    result = await db.execute(q)
    trades = result.scalars().all()
    return [_trade_to_dict(t) for t in trades]


@router.get("/api/performance")
async def get_performance(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PerformanceSnapshot)
        .order_by(desc(PerformanceSnapshot.timestamp))
        .limit(100)
    )
    snaps = result.scalars().all()
    return [
        {
            "timestamp":      s.timestamp.isoformat(),
            "balance":        s.balance,
            "equity":         s.equity,
            "daily_pnl":      s.daily_pnl,
            "total_trades":   s.total_trades,
            "winning_trades": s.winning_trades,
        }
        for s in reversed(snaps)
    ]


# ── Market data ───────────────────────────────────────────────────────────────

@router.get("/api/market/{symbol:path}")
async def get_market_data(symbol: str, timeframe: str = "1h", limit: int = 100):
    symbol = symbol.replace("-", "/").upper()
    ohlcv = await exchange_manager.fetch_ohlcv(symbol, timeframe, limit)
    ticker = await exchange_manager.fetch_ticker(symbol)
    return {
        "symbol":   symbol,
        "ohlcv":    ohlcv,
        "ticker":   ticker,
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _trade_to_dict(t: Trade) -> dict:
    return {
        "id":          t.id,
        "order_id":    t.order_id,
        "exchange":    t.exchange,
        "symbol":      t.symbol,
        "strategy":    t.strategy,
        "side":        t.side,
        "amount":      t.amount,
        "price":       t.price,
        "cost":        t.cost,
        "pnl":         t.pnl,
        "pnl_pct":     t.pnl_pct,
        "status":      t.status,
        "leverage":    t.leverage,
        "stop_loss":   t.stop_loss,
        "take_profit": t.take_profit,
        "opened_at":   t.opened_at.isoformat() if t.opened_at else None,
        "closed_at":   t.closed_at.isoformat() if t.closed_at else None,
    }
