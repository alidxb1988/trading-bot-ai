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
"""
import asyncio
import json
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import AsyncSessionLocal, Trade, PerformanceSnapshot
from backend.exchange.manager import exchange_manager
from backend.strategies.base import Signal
from backend.strategies.hft_scalping import HFTScalpingStrategy
from backend.strategies.ai_multi import AIMultiStrategy
from backend.strategies.zero_loss_dca import ZeroLossDCAStrategy
from backend.strategies.grid import GridTradingStrategy
from backend.trading.risk import RiskManager
from backend.trading.orders import OrderExecutor

log = logging.getLogger(__name__)


class TradingEngine:
    def __init__(self):
        self.running    = False
        self.risk       = RiskManager(settings)
        self.executor   = OrderExecutor(self.risk)
        self._task      = None
        self._ws_clients: list = []   # WebSocket connections to broadcast to

        # Initialise strategies from config
        self.strategies = self._build_strategies()

        # Stats (updated each tick)
        self.stats = {
            "running":       False,
            "mode":          settings.TRADING_MODE,
            "balance":       0.0,
            "equity":        0.0,
            "open_trades":   0,
            "total_trades":  0,
            "winning_trades":0,
            "daily_pnl":     0.0,
            "uptime_seconds":0,
            "last_tick":     None,
            "active_exchange": settings.ACTIVE_EXCHANGE,
        }
        self._start_time: datetime | None = None

    # ── lifecycle ─────────────────────────────────────────────────────────────

    async def start(self):
        if self.running:
            log.info("Engine already running")
            return
        self.running   = True
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
        """Main trading loop — runs every 60 s (adjustable per strategy)."""
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
        balance_info = {"usdt": settings.MAX_POSITION_SIZE_PCT * 10_000}  # paper default
        if exchange_manager.is_connected(settings.ACTIVE_EXCHANGE):
            balance_info = await exchange_manager.fetch_balance()

        available_usdt = balance_info.get("free", {}).get("USDT",
                          balance_info.get("usdt", 0.0))
        self.stats["balance"] = available_usdt

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

        # ── collect all required pairs ────────────────────────────────────
        all_pairs: set[str] = set()
        for strategy in self.strategies:
            if strategy.enabled:
                all_pairs.update(getattr(strategy, "pairs", []))
                all_pairs.update(getattr(strategy, "xaut_pairs", []))

        # ── fetch OHLCV for all pairs ─────────────────────────────────────
        market_data: dict = {}
        fetch_tasks = {
            symbol: exchange_manager.fetch_ohlcv(symbol, "3m", 200)
            if exchange_manager.is_connected(settings.ACTIVE_EXCHANGE)
            else asyncio.coroutine(lambda: [])()
            for symbol in all_pairs
        }
        results = await asyncio.gather(*fetch_tasks.values(), return_exceptions=True)
        for symbol, result in zip(fetch_tasks.keys(), results):
            if isinstance(result, list) and result:
                market_data[symbol] = result

        # ── run strategies ────────────────────────────────────────────────
        for strategy in self.strategies:
            if not strategy.enabled:
                continue
            try:
                signals: list[Signal] = await strategy.analyze(market_data)
                for signal in signals:
                    await self._handle_signal(signal, available_usdt)
            except Exception as exc:
                log.error("Strategy %s error: %s", strategy.name, exc)

        # ── update stats ──────────────────────────────────────────────────
        if self._start_time:
            self.stats["uptime_seconds"] = int(
                (datetime.utcnow() - self._start_time).total_seconds()
            )
        self.stats["daily_pnl"] = self.risk.daily_pnl

        await self._broadcast({"event": "tick", "data": self.stats})

    # ── signal → order ────────────────────────────────────────────────────────

    async def _handle_signal(self, signal: Signal, available_usdt: float):
        log.info("Signal: %s %s  conf=%.2f  strategy=%s",
                 signal.side.upper(), signal.symbol,
                 signal.confidence, signal.strategy)

        order = await self.executor.execute(signal, available_usdt)
        if order is None:
            return

        # Persist to DB
        async with AsyncSessionLocal() as db:
            trade = Trade(
                order_id   = order.get("id", "unknown"),
                exchange   = settings.ACTIVE_EXCHANGE,
                symbol     = signal.symbol,
                strategy   = signal.strategy,
                side       = signal.side,
                amount     = order.get("amount", 0),
                price      = order.get("price", signal.price),
                cost       = order.get("cost", 0),
                leverage   = signal.leverage,
                stop_loss  = signal.stop_loss,
                take_profit= signal.take_profit,
                status     = order.get("status", "open"),
                meta       = json.dumps(signal.meta),
            )
            db.add(trade)
            await db.commit()
            self.stats["total_trades"] += 1

        await self._broadcast({
            "event":  "new_trade",
            "data":   {
                "symbol":   signal.symbol,
                "side":     signal.side,
                "strategy": signal.strategy,
                "price":    signal.price,
                "amount":   order.get("amount", 0),
                "confidence": signal.confidence,
            },
        })

    # ── WebSocket broadcast ───────────────────────────────────────────────────

    def register_ws(self, ws):
        self._ws_clients.append(ws)

    def unregister_ws(self, ws):
        self._ws_clients.discard(ws) if hasattr(self._ws_clients, "discard") else None
        if ws in self._ws_clients:
            self._ws_clients.remove(ws)

    async def _broadcast(self, payload: dict):
        msg = json.dumps(payload)
        dead = []
        for ws in self._ws_clients:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.unregister_ws(ws)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _build_strategies(self):
        strategies = []
        cfg = {
            "hft": {
                "enabled":      settings.ENABLE_HFT,
                "timeframe":    settings.HFT_TIMEFRAME,
                "pairs":        settings.HFT_PAIRS,
                "capital_pct":  settings.HFT_CAPITAL_PCT,
                "leverage":     settings.HFT_LEVERAGE,
                "micro_orders": settings.HFT_MICRO_ORDERS,
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
            },
            "dca": {
                "enabled":         settings.ENABLE_ZERO_LOSS,
                "timeframe":       settings.DCA_TIMEFRAME,
                "pairs":           settings.DCA_PAIRS,
                "xaut_pairs":      settings.DCA_XAUT_PAIRS,
                "capital_pct":     settings.DCA_CAPITAL_PCT,
                "dip_threshold":   settings.DCA_DIP_THRESHOLD,
                "profit_target":   settings.DCA_PROFIT_TARGET,
                "xaut_dip_threshold": settings.DCA_XAUT_DIP_THRESHOLD,
            },
            "grid": {
                "enabled":     settings.ENABLE_GRID,
                "pairs":       settings.GRID_PAIRS,
                "capital_pct": settings.GRID_CAPITAL_PCT,
                "grid_levels": settings.GRID_LEVELS,
                "spacing_pct": settings.GRID_SPACING_PCT,
            },
        }

        strategies.append(HFTScalpingStrategy(cfg["hft"]))
        strategies.append(AIMultiStrategy(cfg["ai"]))
        strategies.append(ZeroLossDCAStrategy(cfg["dca"]))
        strategies.append(GridTradingStrategy(cfg["grid"]))

        return strategies

    def get_strategy(self, name: str):
        for s in self.strategies:
            if s.name == name:
                return s
        return None


# Global singleton used by the API
engine = TradingEngine()
