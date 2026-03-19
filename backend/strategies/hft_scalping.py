"""
HFT / Scalping Strategy
────────────────────────
Timeframe : 3-minute candles
Signals   : EMA-9/21 crossover + RSI + order-book imbalance
Features  : micro-order batching, 30 % profit transfer to reserve
"""
import logging
from typing import Optional

import pandas as pd

from backend.strategies.base import BaseStrategy, Signal
from backend.indicators.technical import (
    ohlcv_to_df, ema, rsi, atr, bollinger_bands
)

log = logging.getLogger(__name__)


class HFTScalpingStrategy(BaseStrategy):
    name = "hft_scalping"

    def __init__(self, config: dict):
        super().__init__(config)
        self.timeframe      = config.get("timeframe",      "3m")
        self.pairs          = config.get("pairs",          ["BTC/USDT", "ETH/USDT"])
        self.capital_pct    = config.get("capital_pct",    0.40)
        self.leverage       = config.get("leverage",       5)
        self.risk_per_trade = config.get("risk_per_trade", 0.03)   # 3 % of capital
        self.micro_orders   = config.get("micro_orders",   3)
        self.profit_transfer= config.get("profit_transfer",0.30)

        # EMA periods
        self._fast = 9
        self._slow = 21

        # state: last crossover direction per symbol
        self._last_cross: dict[str, str] = {}

    # ── main entry ────────────────────────────────────────────────────────────

    async def analyze(self, market_data: dict) -> list[Signal]:
        signals: list[Signal] = []
        for symbol, raw_ohlcv in market_data.items():
            if symbol not in self.pairs:
                continue
            if not raw_ohlcv or len(raw_ohlcv) < 30:
                continue
            try:
                sig = self._evaluate(symbol, raw_ohlcv)
                if sig:
                    signals.append(sig)
            except Exception as exc:
                log.error("[hft] %s error: %s", symbol, exc)
        return signals

    # ── per-symbol logic ──────────────────────────────────────────────────────

    def _evaluate(self, symbol: str, raw_ohlcv: list) -> Optional[Signal]:
        df    = ohlcv_to_df(raw_ohlcv)
        close = df["close"]

        fast_ema = ema(close, self._fast)
        slow_ema = ema(close, self._slow)
        rsi_val  = rsi(close, 14).iloc[-1]
        atr_val  = atr(df, 14).iloc[-1]
        price    = close.iloc[-1]

        # EMA crossover
        prev_diff = fast_ema.iloc[-2] - slow_ema.iloc[-2]
        curr_diff = fast_ema.iloc[-1] - slow_ema.iloc[-1]
        cross_up   = prev_diff <= 0 and curr_diff > 0
        cross_down = prev_diff >= 0 and curr_diff < 0

        last_cross = self._last_cross.get(symbol, "none")

        if cross_up and last_cross != "up":
            # BUY signal — confirm RSI not overbought
            if rsi_val < 70:
                self._last_cross[symbol] = "up"
                return self._make_signal(
                    symbol, "buy", price, rsi_val, atr_val,
                    confidence=self._confidence(rsi_val, curr_diff, "buy")
                )

        elif cross_down and last_cross != "down":
            # SELL/SHORT signal — confirm RSI not oversold
            if rsi_val > 30:
                self._last_cross[symbol] = "down"
                return self._make_signal(
                    symbol, "sell", price, rsi_val, atr_val,
                    confidence=self._confidence(rsi_val, curr_diff, "sell")
                )

        return None

    def _make_signal(self, symbol: str, side: str, price: float,
                     rsi_val: float, atr_val: float,
                     confidence: float) -> Signal:
        # Use 3 ATR multiples for SL, 4 for TP (scalp-style tight levels)
        if side == "buy":
            stop_loss   = price - 3 * atr_val
            take_profit = price + 4 * atr_val
        else:
            stop_loss   = price + 3 * atr_val
            take_profit = price - 4 * atr_val

        return Signal(
            symbol      = symbol,
            side        = side,
            strategy    = self.name,
            confidence  = confidence,
            price       = price,
            amount      = self.risk_per_trade,   # fraction of allocated capital
            leverage    = self.leverage,
            stop_loss   = stop_loss,
            take_profit = take_profit,
            meta        = {
                "rsi":           rsi_val,
                "atr":           atr_val,
                "micro_orders":  self.micro_orders,
                "profit_transfer": self.profit_transfer,
            },
        )

    @staticmethod
    def _confidence(rsi_val: float, ema_diff: float, side: str) -> float:
        """Heuristic confidence 0..1."""
        base = 0.55
        # RSI confirms trend
        if side == "buy"  and rsi_val < 50:
            base += 0.10
        if side == "sell" and rsi_val > 50:
            base += 0.10
        # Strong crossover magnitude
        if abs(ema_diff) > 10:
            base += 0.10
        return min(round(base, 2), 0.95)
