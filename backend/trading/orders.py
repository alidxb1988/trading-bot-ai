"""
Order Executor
────────────────
Translates strategy Signals into real exchange orders via the ExchangeManager.
Supports market and limit orders, stop-loss / take-profit attachment.
"""
import logging
import uuid
from datetime import datetime

from backend.strategies.base import Signal
from backend.exchange.manager import exchange_manager
from backend.trading.risk import RiskManager
from backend.config import settings

log = logging.getLogger(__name__)


class OrderExecutor:
    def __init__(self, risk: RiskManager):
        self.risk = risk

    async def execute(self, signal: Signal, available_usdt: float,
                      exchange: str = None) -> dict | None:
        """
        Execute a signal.  Returns the exchange order dict or None on failure.
        In PAPER mode returns a synthetic order dict.
        """
        if not signal.is_valid:
            log.warning("Invalid signal ignored: %s", signal)
            return None

        exchange = exchange or settings.ACTIVE_EXCHANGE

        # Compute position size
        usdt_size = self.risk.position_size_usdt(
            signal.amount, available_usdt,
            signal.price, signal.meta.get("atr", 0.0),
            signal.leverage,
        )
        quantity = self.risk.compute_quantity(usdt_size, signal.price, signal.leverage)

        if quantity <= 0:
            log.warning("Zero quantity computed for %s, skipping", signal.symbol)
            return None

        log.info("[executor] %s %s %s  qty=%.6f  usdt=%.2f  leverage=%dx",
                 signal.side.upper(), signal.symbol, signal.strategy,
                 quantity, usdt_size, signal.leverage)

        if settings.TRADING_MODE == "paper":
            return self._paper_order(signal, quantity, usdt_size)

        # ── Live trading ──────────────────────────────────────────────────────
        try:
            # Set leverage first
            await exchange_manager.set_leverage(signal.symbol, signal.leverage, exchange)

            params = {}
            # Attach stop-loss / take-profit if exchange supports it
            if signal.stop_loss:
                params["stopLoss"] = {"type": "market", "triggerPrice": signal.stop_loss}
            if signal.take_profit:
                params["takeProfit"] = {"type": "market", "triggerPrice": signal.take_profit}

            order_type = signal.meta.get("order_type", "market")

            if order_type == "limit" and "grid_price" in signal.meta:
                order = await exchange_manager.create_limit_order(
                    signal.symbol, signal.side, quantity,
                    signal.meta["grid_price"], params=params, exchange=exchange
                )
            else:
                order = await exchange_manager.create_market_order(
                    signal.symbol, signal.side, quantity,
                    params=params, exchange=exchange
                )

            return order

        except Exception as exc:
            log.error("[executor] order failed for %s: %s", signal.symbol, exc)
            return None

    @staticmethod
    def _paper_order(signal: Signal, quantity: float, usdt_size: float) -> dict:
        """Synthetic order for paper trading."""
        return {
            "id":       str(uuid.uuid4())[:12],
            "symbol":   signal.symbol,
            "side":     signal.side,
            "type":     "market",
            "amount":   quantity,
            "price":    signal.price,
            "cost":     usdt_size,
            "status":   "closed",   # paper orders fill instantly
            "strategy": signal.strategy,
            "leverage": signal.leverage,
            "stopLoss":    signal.stop_loss,
            "takeProfit":  signal.take_profit,
            "timestamp":   int(datetime.utcnow().timestamp() * 1000),
            "paper":       True,
        }
