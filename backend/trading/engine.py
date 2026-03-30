"""
Trading Engine
───────────────
Central orchestrator that:
1. Fetches OHLCV data for all required pairs from all active strategies.
2. Passes data to each strategy's analyze() method.
3. Feeds signals through RiskManager and OrderExecutor.
4. Persists completed trades to the database.
5. Broadcasts real-time events via the WebSocket event bus.
6. Enforces circuit-breakers (daily loss, max drawdown).
7. Writes periodic PerformanceSnapshots to the database.
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Optional

from backend.config import settings
from backend.database import AsyncSessionLocal, Trade, PerformanceSnapshot
from backend.exchange.manager import exchange_manager
from backend.strategies.base import Signal
from backend.strategies.hft_scalping import HFTScalpingStrategy
from backend.strategies.ai_multi import AIMultiStrategy
from backend.strategies.zero_loss_dca import ZeroLossDCAStrategy
from backend.strategies.grid import GridTradingStrategy
from backend.strategies.gomale import GomaleStrategy
from backend.trading.risk import RiskManager
from backend.trading.orders import OrderExecutor
from backend.brain.claude_brain import claude_brain

log = logging.getLogger(__name__)


async def _empty_ohlcv() -> list:
    """Async no-op used when exchange is not connected (paper mode)."""
    return []


class TradingEngine:
    def __init__(self):
        self.running    = False
        self.risk       = RiskManager(settings)
        self.executor   = OrderExecutor(self.risk)
        self._task: Optional[asyncio.Task] = None
        self._ws_clients: list = []

        # In-memory open position tracker: symbol → {side, entry_price, strategy}
        # Updated in _handle_signal(); gives Claude correlated-position context.
        self._active_positions: dict[str, dict] = {}

        # Initialise strategies from config
        self.strategies = self._build_strategies()

        # Stats (updated each tick)
        self.stats = {
            "running":        False,
            "mode":           settings.TRADING_MODE,
            "balance":        0.0,
            "equity":         0.0,
            "open_trades":    0,
            "total_trades":   0,
            "winning_trades": 0,
            "daily_pnl":      0.0,
            "uptime_seconds": 0,
            "last_tick":      None,
            "active_exchange": settings.ACTIVE_EXCHANGE,
            "brain_enabled": settings.CLAUDE_BRAIN_ENABLED,
            "brain_calls": 0,
        }
        self._start_time: Optional[datetime] = None
        self._snap_counter: int = 0   # write a snapshot every N ticks

    # ── lifecycle ─────────────────────────────────────────────────────────────

    async def start(self):
        if self.running:
            log.info("Engine already running")
            return
        self.running    = True
        self._start_time = datetime.utcnow()
        self.stats["running"] = True
        log.info("Trading engine starting (mode=%s)", settings.TRADING_MODE)
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self.running = False
        self.stats["running"] = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        log.info("Trading engine stopped")

    # ── main loop ─────────────────────────────────────────────────────────────

    async def _loop(self):
        """Main trading loop — runs every 60 s."""
        log.info("Engine loop started")
        while self.running:
            try:
                await self._tick()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                log.error("Engine tick error: %s", exc, exc_info=True)
            await asyncio.sleep(60)

    async def _tick(self):
        """One iteration: fetch data → analyse → execute → persist."""
        tick_start = datetime.utcnow()
        self.stats["last_tick"] = tick_start.isoformat()

        # ── fetch balance ─────────────────────────────────────────────────
        if exchange_manager.is_connected(settings.ACTIVE_EXCHANGE):
            balance_info = await exchange_manager.fetch_balance()
        else:
            # Paper mode: use configurable starting balance
            balance_info = {"usdt": settings.PAPER_BALANCE}

        available_usdt = balance_info.get("free", {}).get("USDT",
                          balance_info.get("usdt", 0.0))
        self.stats["balance"] = available_usdt
        self.risk.update_equity(available_usdt)

        # ── circuit breakers ──────────────────────────────────────────────
        if self.risk.check_daily_loss(available_usdt):
            log.warning("Daily loss limit reached — halting engine for today")
            await self._broadcast({"event": "daily_loss_halt"})
            await self.stop()
            return

        if self.risk.check_max_drawdown(available_usdt):
            log.warning("Max drawdown reached — halting engine")
            await self._broadcast({"event": "max_drawdown_halt"})
            await self.stop()
            return

        # ── collect required pairs + their timeframes ─────────────────────
        # Build a map: (symbol, timeframe) → fetch coroutine
        # so each strategy gets candles at its own timeframe.
        symbol_tf: dict = {}
        for strategy in self.strategies:
            if not strategy.enabled:
                continue
            tf = getattr(strategy, "timeframe", "15m")
            pairs = list(getattr(strategy, "pairs", [])) + list(getattr(strategy, "xaut_pairs", []))
            for symbol in pairs:
                key = (symbol, tf)
                if key not in symbol_tf:
                    if exchange_manager.is_connected(settings.ACTIVE_EXCHANGE):
                        symbol_tf[key] = exchange_manager.fetch_ohlcv(symbol, tf, 200)
                    else:
                        symbol_tf[key] = _empty_ohlcv()

        # ── fetch OHLCV concurrently ───────────────────────────────────────
        keys = list(symbol_tf.keys())
        results = await asyncio.gather(*symbol_tf.values(), return_exceptions=True)

        # Build per-strategy market_data: key = (symbol, tf) for lookup
        raw_by_key: dict[tuple[str, str], list] = {}
        for key, result in zip(keys, results):
            if isinstance(result, list) and result:
                raw_by_key[key] = result

        # ── run strategies — collect all signals ──────────────────────────
        all_signals: list[Signal] = []
        for strategy in self.strategies:
            if not strategy.enabled:
                continue
            tf = getattr(strategy, "timeframe", "15m")
            market_data: dict[str, list] = {
                symbol: raw_by_key[(symbol, tf)]
                for symbol in (
                    list(getattr(strategy, "pairs", [])) +
                    list(getattr(strategy, "xaut_pairs", []))
                )
                if (symbol, tf) in raw_by_key
            }
            try:
                signals: list[Signal] = await strategy.analyze(market_data)
                all_signals.extend(signals)
            except Exception as exc:
                log.error("Strategy %s error: %s", strategy.name, exc)

        # ── Claude Brain — orchestrate signals ────────────────────────────
        if all_signals and settings.CLAUDE_BRAIN_ENABLED:
            try:
                # FIX 3: Pass full raw OHLCV candle lists (not just price summaries)
                # so Gemini Agent actually receives candle data for technical analysis.
                brain_market_data = self._build_brain_ohlcv(raw_by_key)

                # FIX 4: Include open positions detail so Claude can detect correlation.
                drawdown_pct = max(0, (self.risk.peak_equity - available_usdt)
                                   / max(self.risk.peak_equity, 1) * 100)
                brain_portfolio = {
                    "balance":          available_usdt,
                    "equity":           self.risk.peak_equity,
                    "open_trades":      self.stats["open_trades"],
                    "daily_pnl":        self.risk.daily_pnl,
                    "daily_pnl_pct":    (self.risk.daily_pnl / max(available_usdt, 1)) * 100,
                    "drawdown_pct":     drawdown_pct,
                    # Full open position list for correlated-long detection
                    "open_positions":   list(self._active_positions.values()),
                    "open_position_symbols": list(self._active_positions.keys()),
                    "open_positions_by_side": {
                        "buy":  [s for s, p in self._active_positions.items() if p["side"] == "buy"],
                        "sell": [s for s, p in self._active_positions.items() if p["side"] == "sell"],
                    },
                }

                signal_dicts = [
                    {
                        "symbol":     s.symbol,
                        "strategy":   s.strategy,
                        "side":       s.side,
                        "confidence": s.confidence,
                        "price":      s.price,
                        "leverage":   s.leverage,
                        "stop_loss":  s.stop_loss,
                        "take_profit": s.take_profit,
                        "meta":       s.meta,
                    }
                    for s in all_signals
                ]

                brain_decisions = await claude_brain.analyze_and_decide(
                    strategy_signals=signal_dicts,
                    market_data=brain_market_data,
                    portfolio=brain_portfolio,
                    polymarket={},
                )

                # Build decision map: symbol → decision
                decision_map: dict[str, dict] = {}
                for d in brain_decisions:
                    sym = d.get("symbol")
                    if sym:
                        decision_map[sym] = d

                await self._broadcast({
                    "event": "brain_decision",
                    "data": {
                        "decisions": brain_decisions,
                        "reasoning_preview": claude_brain.last_reasoning[:300],
                        "total_signals": len(all_signals),
                    }
                })

                # FIX 1: Default action is "reject" — missing symbol = no trade.
                # A signal with no AI decision gets blocked, never slips through.
                for signal in all_signals:
                    decision = decision_map.get(signal.symbol, {})
                    action = decision.get("action", "reject")   # was "approve" — FIXED
                    if action == "reject":
                        log.info("Brain REJECTED %s %s — %s",
                                 signal.side.upper(), signal.symbol,
                                 decision.get("reason", "no decision returned"))
                        continue
                    # Apply any modifications from brain
                    if action == "modify":
                        if decision.get("modified_leverage"):
                            signal.leverage = decision["modified_leverage"]
                        brain_conf = decision.get("confidence", signal.confidence)
                        signal.confidence = brain_conf
                    await self._handle_signal(signal, available_usdt)

            except Exception as exc:
                # FIX 2: On brain crash, REJECT all signals (was: approve all).
                # Never trade without AI oversight when the brain is supposed to be active.
                log.error(
                    "Claude Brain error — REJECTING all %d signals for safety: %s",
                    len(all_signals), exc, exc_info=True,
                )
                await self._broadcast({
                    "event": "brain_error",
                    "data": {"error": str(exc), "rejected_signals": len(all_signals)},
                })
        else:
            # Brain disabled — execute all signals directly (paper/manual mode)
            for signal in all_signals:
                await self._handle_signal(signal, available_usdt)

        # ── update stats ──────────────────────────────────────────────────
        if self._start_time:
            self.stats["uptime_seconds"] = int(
                (datetime.utcnow() - self._start_time).total_seconds()
            )
        self.stats["daily_pnl"] = self.risk.daily_pnl
        self.stats["brain_calls"] = claude_brain.total_calls

        await self._broadcast({"event": "tick", "data": self.stats})

        # ── persist performance snapshot every 5 ticks (~5 min) ───────────
        self._snap_counter += 1
        if self._snap_counter >= 5:
            self._snap_counter = 0
            await self._save_snapshot(available_usdt)

    # ── signal → order ────────────────────────────────────────────────────────

    async def _handle_signal(self, signal: Signal, available_usdt: float):
        log.info("Signal: %s %s  conf=%.2f  strategy=%s",
                 signal.side.upper(), signal.symbol,
                 signal.confidence, signal.strategy)

        # Track open positions so Claude can detect correlation on the next tick.
        if signal.side in ("buy", "sell"):
            self._active_positions[signal.symbol] = {
                "symbol":      signal.symbol,
                "side":        signal.side,
                "entry_price": signal.price,
                "strategy":    signal.strategy,
                "leverage":    signal.leverage,
            }

        order = await self.executor.execute(signal, available_usdt)
        if order is None:
            return

        # Safely serialise meta — non-JSON-serialisable values are dropped
        try:
            meta_json = json.dumps(signal.meta)
        except (TypeError, ValueError):
            meta_json = json.dumps({k: str(v) for k, v in signal.meta.items()})

        # Persist to DB
        try:
            async with AsyncSessionLocal() as db:
                # Guarantee unique order_id even when exchange doesn't provide one
                raw_order_id = order.get("id")
                if not raw_order_id or raw_order_id == "unknown":
                    raw_order_id = f"local_{uuid.uuid4().hex[:12]}"
                trade = Trade(
                    order_id    = raw_order_id,
                    exchange    = settings.ACTIVE_EXCHANGE,
                    symbol      = signal.symbol,
                    strategy    = signal.strategy,
                    side        = signal.side,
                    amount      = order.get("amount", 0),
                    price       = order.get("price", signal.price),
                    cost        = order.get("cost", 0),
                    leverage    = signal.leverage,
                    stop_loss   = signal.stop_loss,
                    take_profit = signal.take_profit,
                    status      = order.get("status", "open"),
                    meta        = meta_json,
                )
                db.add(trade)
                await db.commit()
                self.stats["total_trades"] += 1
        except Exception as exc:
            log.error("Failed to persist trade for %s: %s", signal.symbol, exc)

        await self._broadcast({
            "event": "new_trade",
            "data":  {
                "symbol":     signal.symbol,
                "side":       signal.side,
                "strategy":   signal.strategy,
                "price":      signal.price,
                "amount":     order.get("amount", 0),
                "confidence": signal.confidence,
            },
        })

    # ── performance snapshot ──────────────────────────────────────────────────

    async def _save_snapshot(self, balance: float):
        try:
            async with AsyncSessionLocal() as db:
                snap = PerformanceSnapshot(
                    balance        = balance,
                    equity         = self.risk.peak_equity,
                    daily_pnl      = self.risk.daily_pnl,
                    total_trades   = self.stats["total_trades"],
                    winning_trades = self.stats["winning_trades"],
                )
                db.add(snap)
                await db.commit()
        except Exception as exc:
            log.error("Failed to save performance snapshot: %s", exc)

    # ── WebSocket broadcast ───────────────────────────────────────────────────

    def register_ws(self, ws):
        self._ws_clients.append(ws)

    def unregister_ws(self, ws):
        try:
            self._ws_clients.remove(ws)
        except ValueError:
            pass

    async def _broadcast(self, payload: dict):
        msg = json.dumps(payload)
        dead = []
        for ws in list(self._ws_clients):
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.unregister_ws(ws)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _build_brain_ohlcv(self, raw_by_key: dict) -> dict:
        """
        Return raw OHLCV candle lists keyed by symbol.

        This is what Claude Brain stores as _ctx_market and passes to Gemini Agent.
        Gemini needs the actual candle list (not a price summary) for technical analysis.
        If multiple timeframes exist for the same symbol, prefer the one with more candles.
        """
        ohlcv_ctx: dict[str, list] = {}
        for (symbol, _tf), candles in raw_by_key.items():
            if not candles:
                continue
            existing = ohlcv_ctx.get(symbol)
            if existing is None or len(candles) > len(existing):
                ohlcv_ctx[symbol] = candles
        return ohlcv_ctx

    def _build_strategies(self):
        strategies = []
        cfg = {
            "hft": {
                "enabled":         settings.ENABLE_HFT,
                "timeframe":       settings.HFT_TIMEFRAME,
                "pairs":           settings.HFT_PAIRS,
                "capital_pct":     settings.HFT_CAPITAL_PCT,
                "leverage":        settings.HFT_LEVERAGE,
                "micro_orders":    settings.HFT_MICRO_ORDERS,
                "profit_transfer": settings.HFT_PROFIT_TRANSFER,
            },
            "ai": {
                "enabled":              settings.ENABLE_AI_MULTI,
                "timeframe":            settings.AI_TIMEFRAME,
                "pairs":                settings.AI_PAIRS,
                "capital_pct":          settings.AI_CAPITAL_PCT,
                "leverage":             settings.AI_LEVERAGE,
                "confidence_threshold": settings.AI_CONFIDENCE_THRESHOLD,
                "auto_reinvest":        settings.AI_AUTO_REINVEST,
                "volatility_mode":      settings.AI_VOLATILITY_MODE,
            },
            "dca": {
                "enabled":            settings.ENABLE_ZERO_LOSS,
                "timeframe":          settings.DCA_TIMEFRAME,
                "pairs":              settings.DCA_PAIRS,
                "xaut_pairs":         settings.DCA_XAUT_PAIRS,
                "capital_pct":        settings.DCA_CAPITAL_PCT,
                "dip_threshold":      settings.DCA_DIP_THRESHOLD,
                "profit_target":      settings.DCA_PROFIT_TARGET,
                "xaut_dip_threshold": settings.DCA_XAUT_DIP_THRESHOLD,
            },
            "grid": {
                "enabled":     settings.ENABLE_GRID,
                "pairs":       settings.GRID_PAIRS,
                "capital_pct": settings.GRID_CAPITAL_PCT,
                "grid_levels": settings.GRID_LEVELS,
                "spacing_pct": settings.GRID_SPACING_PCT,
            },
            "gomale": {
                "enabled":              settings.ENABLE_GOMALE,
                "timeframe":            settings.GOMALE_TIMEFRAME,
                "pairs":                settings.GOMALE_PAIRS,
                "capital_pct":          settings.GOMALE_CAPITAL_PCT,
                "leverage":             settings.GOMALE_LEVERAGE,
                "confidence_threshold": settings.GOMALE_CONFIDENCE_THRESHOLD,
                "risk_per_trade":       settings.GOMALE_RISK_PER_TRADE,
            },
        }

        strategies.append(HFTScalpingStrategy(cfg["hft"]))
        strategies.append(AIMultiStrategy(cfg["ai"]))
        strategies.append(ZeroLossDCAStrategy(cfg["dca"]))
        strategies.append(GridTradingStrategy(cfg["grid"]))
        strategies.append(GomaleStrategy(cfg["gomale"]))

        return strategies

    def get_strategy(self, name: str):
        for s in self.strategies:
            if s.name == name:
                return s
        return None


# Global singleton used by the API
engine = TradingEngine()
