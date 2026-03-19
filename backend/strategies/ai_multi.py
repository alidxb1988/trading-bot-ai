"""
AI Multi-Strategy
──────────────────
Combines EMA / RSI / MACD / Bollinger / OBV / Supertrend into a weighted
confidence score.  Trades when confidence exceeds the configured threshold.
Auto-reinvestment: PnL is folded back into the strategy's capital bucket.
"""
import logging
from typing import Optional

import numpy as np

from backend.strategies.base import BaseStrategy, Signal
from backend.indicators.technical import ohlcv_to_df, compute_signal_score, atr

log = logging.getLogger(__name__)


class AIMultiStrategy(BaseStrategy):
    name = "ai_multi"

    def __init__(self, config: dict):
        super().__init__(config)
        self.timeframe    = config.get("timeframe",   "15m")
        self.pairs        = config.get("pairs",       ["BTC/USDT", "ETH/USDT"])
        self.capital_pct  = config.get("capital_pct", 0.35)
        self.leverage     = config.get("leverage",    3)
        self.threshold    = config.get("confidence_threshold", 0.75)
        self.auto_reinvest= config.get("auto_reinvest", True)
        self.volatility_mode = config.get("volatility_mode", "medium")  # low/medium/high

        # Accumulated PnL for reinvestment
        self._reinvest_pool: float = 0.0

        # Prevent flipping positions too quickly
        self._last_side: dict[str, str] = {}

    # ── main entry ────────────────────────────────────────────────────────────

    async def analyze(self, market_data: dict) -> list[Signal]:
        signals: list[Signal] = []
        for symbol, raw_ohlcv in market_data.items():
            if symbol not in self.pairs:
                continue
            if not raw_ohlcv or len(raw_ohlcv) < 50:
                continue
            try:
                sig = self._evaluate(symbol, raw_ohlcv)
                if sig:
                    signals.append(sig)
            except Exception as exc:
                log.error("[ai_multi] %s error: %s", symbol, exc)
        return signals

    def record_pnl(self, pnl: float):
        """Called by the engine when a trade closes; folds profit into pool."""
        if self.auto_reinvest and pnl > 0:
            self._reinvest_pool += pnl
            log.info("[ai_multi] reinvest pool: +%.4f  total=%.4f", pnl, self._reinvest_pool)

    # ── per-symbol logic ──────────────────────────────────────────────────────

    def _evaluate(self, symbol: str, raw_ohlcv: list) -> Optional[Signal]:
        df      = ohlcv_to_df(raw_ohlcv)
        result  = compute_signal_score(df)
        confidence = result["confidence"]
        price      = df["close"].iloc[-1]
        atr_val    = result["atr"]

        # Adjust for volatility regime
        adjusted_threshold = self._adjust_threshold(result["volatility"])

        # Determine direction
        if confidence >= adjusted_threshold:
            side = "buy"
        elif confidence <= (1 - adjusted_threshold):
            side = "sell"
        else:
            return None  # No clear signal

        # Avoid flipping back-to-back on same symbol
        if self._last_side.get(symbol) == side:
            return None
        self._last_side[symbol] = side

        # SL / TP based on ATR
        atr_mult_sl = 2.5 if self.volatility_mode == "low" else (
                      2.0 if self.volatility_mode == "medium" else 1.5)
        atr_mult_tp = atr_mult_sl * 2.0

        if side == "buy":
            stop_loss   = price - atr_mult_sl * atr_val
            take_profit = price + atr_mult_tp * atr_val
        else:
            stop_loss   = price + atr_mult_sl * atr_val
            take_profit = price - atr_mult_tp * atr_val

        return Signal(
            symbol      = symbol,
            side        = side,
            strategy    = self.name,
            confidence  = confidence,
            price       = price,
            amount      = self.capital_pct,   # fraction of total capital
            leverage    = self.leverage,
            stop_loss   = stop_loss,
            take_profit = take_profit,
            meta        = {
                **result["signals"],
                "rsi":        result["rsi"],
                "atr":        result["atr"],
                "volatility": result["volatility"],
                "reinvest_pool": self._reinvest_pool,
            },
        )

    def _adjust_threshold(self, volatility: float) -> float:
        """Lower the bar slightly in high-volatility environments."""
        base = self.threshold
        if self.volatility_mode == "high" and volatility > 2.0:
            base = max(base - 0.05, 0.60)
        elif self.volatility_mode == "low" and volatility < 0.5:
            base = min(base + 0.05, 0.90)
        return base
