"""
Gomale Trading Strategy
────────────────────────
Multi-condition signal system using RSI + MACD + ADX + sentiment proxy,
targeting SOL/USDT and ETH/USDT.

Signal tiers (derived from the Gomale React dashboard logic):

  Tier 1 – Strong BUY  : RSI < 30  AND sentiment > 60  AND ADX > 30  → confidence 85–95 %
  Tier 2 – BUY         : RSI < 35  AND sentiment > 50  AND MACD > 0  → confidence 75–95 %
  Tier 3 – Moderate BUY: RSI < 45  AND sentiment > 55  AND MACD > 20 → confidence 65–80 %
  Tier 4 – SELL        : RSI > 65  (open position)                    → confidence 70–90 %
  Tier 5 – Strong SELL : RSI > 70  AND sentiment < 40                 → confidence 80–95 %

Confidence gate: signal is only acted on when confidence >= threshold (default 70 %).
Sentiment proxy: derived from OBV trend strength + volume ratio vs 20-period average.
"""
import logging
import random
from typing import Optional

import pandas as pd

from backend.strategies.base import BaseStrategy, Signal
from backend.indicators.technical import (
    ohlcv_to_df, rsi, macd, adx, atr, obv, ema
)

log = logging.getLogger(__name__)


class GomaleStrategy(BaseStrategy):
    name = "gomale"

    def __init__(self, config: dict):
        super().__init__(config)
        self.timeframe  = config.get("timeframe", "15m")
        self.pairs      = config.get("pairs", ["SOL/USDT", "ETH/USDT"])
        self.capital_pct = config.get("capital_pct", 0.25)
        self.leverage   = config.get("leverage", 2)
        self.threshold  = config.get("confidence_threshold", 0.70)
        self.risk_per_trade = config.get("risk_per_trade", 0.10)
        self._last_side: dict[str, str] = {}

    # ── Public interface ───────────────────────────────────────────────────────

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
                log.error("[gomale] %s error: %s", symbol, exc)
        return signals

    # ── Per-symbol evaluation ─────────────────────────────────────────────────

    def _evaluate(self, symbol: str, raw_ohlcv: list) -> Optional[Signal]:
        df = ohlcv_to_df(raw_ohlcv)

        rsi_val   = float(rsi(df["close"]).iloc[-1])
        macd_line, _sig, _hist = macd(df["close"])
        macd_val  = float(macd_line.iloc[-1])
        adx_val   = float(adx(df).iloc[-1])
        atr_val   = float(atr(df).iloc[-1])
        price     = float(df["close"].iloc[-1])
        sentiment = self._sentiment_proxy(df)

        signal_side, confidence = self._get_decision(
            rsi_val, macd_val, adx_val, sentiment,
            has_position=self._last_side.get(symbol) == "buy"
        )

        if signal_side == "HOLD" or confidence < self.threshold * 100:
            return None

        side = "buy" if signal_side == "BUY" else "sell"

        # Avoid back-to-back same direction
        if self._last_side.get(symbol) == side:
            return None
        self._last_side[symbol] = side

        # ATR-based stop-loss / take-profit (2× / 4× ATR)
        if side == "buy":
            stop_loss   = price - 2.0 * atr_val
            take_profit = price + 4.0 * atr_val
        else:
            stop_loss   = price + 2.0 * atr_val
            take_profit = price - 4.0 * atr_val

        return Signal(
            symbol      = symbol,
            side        = side,
            strategy    = self.name,
            confidence  = round(confidence / 100, 4),
            price       = price,
            amount      = self.capital_pct,
            leverage    = self.leverage,
            stop_loss   = stop_loss,
            take_profit = take_profit,
            meta        = {
                "rsi":       round(rsi_val, 2),
                "macd":      round(macd_val, 4),
                "adx":       round(adx_val, 2),
                "sentiment": round(sentiment, 2),
                "atr":       round(atr_val, 6),
            },
        )

    # ── Signal logic (mirrors React getClaudeDecision) ────────────────────────

    @staticmethod
    def _get_decision(
        rsi_val: float,
        macd_val: float,
        adx_val: float,
        sentiment: float,
        has_position: bool,
    ) -> tuple[str, float]:
        """
        Returns (signal, confidence_pct).
        Confidence is in [0, 100]; caller normalises to [0, 1].
        """
        # Tier 1 – Strong BUY
        if rsi_val < 30 and sentiment > 60 and adx_val > 30:
            return "BUY", 85 + random.random() * 10

        # Tier 2 – BUY
        if rsi_val < 35 and sentiment > 50 and macd_val > 0:
            return "BUY", 75 + random.random() * 20

        # Tier 3 – Moderate BUY
        if rsi_val < 45 and sentiment > 55 and macd_val > 20:
            return "BUY", 65 + random.random() * 15

        # Tier 5 – Strong SELL
        if rsi_val > 70 and sentiment < 40:
            return "SELL", 80 + random.random() * 15

        # Tier 4 – SELL (requires open position)
        if rsi_val > 65 and has_position:
            return "SELL", 70 + random.random() * 20

        return "HOLD", 50.0

    # ── Sentiment proxy ───────────────────────────────────────────────────────

    @staticmethod
    def _sentiment_proxy(df: pd.DataFrame) -> float:
        """
        Estimates a 0–100 sentiment score without an external API.
        Combines OBV trend direction and recent volume ratio.
        """
        try:
            obv_series = obv(df)
            obv_ema    = ema(obv_series, 10)
            obv_signal = 1 if float(obv_series.iloc[-1]) > float(obv_ema.iloc[-1]) else -1

            vol_mean = df["volume"].rolling(20).mean().iloc[-1]
            vol_ratio = df["volume"].iloc[-1] / vol_mean if vol_mean > 0 else 1.0
            vol_score = min(max(vol_ratio, 0.5), 2.0)  # clamp to [0.5, 2.0]

            # Price momentum over last 5 bars
            price_change = (df["close"].iloc[-1] - df["close"].iloc[-6]) / df["close"].iloc[-6]
            momentum = min(max(price_change * 100, -30), 30)  # clamp to [-30, 30]

            # Combine: OBV direction (±20), volume score (0–40), momentum (−30 to +30) → centre at 50
            raw = 50 + obv_signal * 20 + (vol_score - 1.0) * 20 + momentum
            return float(min(max(raw, 0), 100))
        except Exception:
            return 50.0
