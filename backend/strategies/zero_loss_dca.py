"""
Zero-Loss / DCA Strategy
─────────────────────────
• Buys confirmed dips (price drops ≥ dip_threshold from recent peak).
• Dollar-cost-averages on further drops (up to max_dca_orders layers).
• Holds until the blended average cost reaches the profit target.
• Also trades XAUT (gold token) on its own dip threshold.
• "Zero-loss" is enforced by never setting a hard stop-loss;
  DCA layers bring the average cost down so the position eventually turns green.
"""
import logging
from typing import Optional

import pandas as pd

from backend.strategies.base import BaseStrategy, Signal
from backend.indicators.technical import ohlcv_to_df, ema, rsi

log = logging.getLogger(__name__)


class ZeroLossDCAStrategy(BaseStrategy):
    name = "zero_loss_dca"

    def __init__(self, config: dict):
        super().__init__(config)
        self.timeframe        = config.get("timeframe",          "1h")
        self.pairs            = config.get("pairs",              ["BTC/USDT", "ETH/USDT"])
        self.xaut_pairs       = config.get("xaut_pairs",         ["XAUT/USDT"])
        self.capital_pct      = config.get("capital_pct",        0.25)
        self.dip_threshold    = config.get("dip_threshold",      0.12)   # 12 %
        self.profit_target    = config.get("profit_target",      0.15)   # 15 %
        self.xaut_dip         = config.get("xaut_dip_threshold", 0.08)   # 8 %
        self.max_dca_orders   = config.get("max_dca_orders",     5)
        self.dca_multiplier   = config.get("dca_size_multiplier",1.5)    # each layer is 1.5× bigger

        # State per symbol: { "peak_price", "avg_cost", "total_invested", "dca_count" }
        self._positions: dict[str, dict] = {}
        # Rolling 30-bar high (peak)
        self._peaks: dict[str, float] = {}

    # ── main entry ────────────────────────────────────────────────────────────

    async def analyze(self, market_data: dict) -> list[Signal]:
        signals: list[Signal] = []
        all_pairs = self.pairs + self.xaut_pairs

        for symbol, raw_ohlcv in market_data.items():
            if symbol not in all_pairs:
                continue
            if not raw_ohlcv or len(raw_ohlcv) < 10:
                continue
            try:
                sig = self._evaluate(symbol, raw_ohlcv)
                if sig:
                    signals.append(sig)
            except Exception as exc:
                log.error("[zero_loss_dca] %s error: %s", symbol, exc)
        return signals

    # ── per-symbol logic ──────────────────────────────────────────────────────

    def _evaluate(self, symbol: str, raw_ohlcv: list) -> Optional[Signal]:
        df    = ohlcv_to_df(raw_ohlcv)
        close = df["close"]
        price = float(close.iloc[-1])

        # Track rolling 30-candle peak
        peak = float(close.tail(30).max())
        self._peaks[symbol] = max(self._peaks.get(symbol, price), peak)

        is_xaut = symbol in self.xaut_pairs
        threshold = self.xaut_dip if is_xaut else self.dip_threshold

        pos = self._positions.get(symbol)

        # ── No open position: check for initial dip entry ─────────────────
        if pos is None:
            drop_pct = (self._peaks[symbol] - price) / self._peaks[symbol]
            if drop_pct >= threshold:
                # Confirm with RSI below 40 (oversold confirmation)
                rsi_val = rsi(close, 14).iloc[-1]
                if rsi_val < 45:
                    confidence = min(0.60 + drop_pct, 0.92)
                    self._positions[symbol] = {
                        "avg_cost":      price,
                        "total_invested":self.capital_pct,
                        "dca_count":     1,
                        "peak_at_entry": self._peaks[symbol],
                    }
                    return Signal(
                        symbol      = symbol,
                        side        = "buy",
                        strategy    = self.name,
                        confidence  = confidence,
                        price       = price,
                        amount      = self.capital_pct,
                        leverage    = 1,   # spot-style, no leverage
                        stop_loss   = None,
                        take_profit = price * (1 + self.profit_target),
                        meta        = {"dip_pct": drop_pct, "layer": 1,
                                       "rsi": rsi_val, "is_xaut": is_xaut},
                    )

        # ── Existing position ─────────────────────────────────────────────
        else:
            avg_cost = pos["avg_cost"]

            # Check profit target → emit CLOSE/SELL
            if price >= avg_cost * (1 + self.profit_target):
                self._positions.pop(symbol, None)
                self._peaks[symbol] = price   # reset peak
                return Signal(
                    symbol      = symbol,
                    side        = "sell",
                    strategy    = self.name,
                    confidence  = 0.95,
                    price       = price,
                    amount      = pos["total_invested"],
                    leverage    = 1,
                    meta        = {"reason": "profit_target_reached",
                                   "avg_cost": avg_cost,
                                   "layer": pos["dca_count"]},
                )

            # DCA: further drop from avg_cost
            further_drop = (avg_cost - price) / avg_cost
            if (further_drop >= threshold and
                    pos["dca_count"] < self.max_dca_orders):
                layer      = pos["dca_count"] + 1
                add_amount = self.capital_pct * (self.dca_multiplier ** (layer - 1))
                new_total  = pos["total_invested"] + add_amount
                new_avg    = (pos["avg_cost"] * pos["total_invested"] +
                              price * add_amount) / new_total

                self._positions[symbol] = {
                    "avg_cost":      new_avg,
                    "total_invested":new_total,
                    "dca_count":     layer,
                    "peak_at_entry": pos["peak_at_entry"],
                }
                return Signal(
                    symbol      = symbol,
                    side        = "buy",
                    strategy    = self.name,
                    confidence  = 0.80,
                    price       = price,
                    amount      = add_amount,
                    leverage    = 1,
                    take_profit = new_avg * (1 + self.profit_target),
                    meta        = {"reason": "dca_layer",
                                   "layer":  layer,
                                   "new_avg_cost": new_avg,
                                   "drop_from_avg": further_drop},
                )

        return None
