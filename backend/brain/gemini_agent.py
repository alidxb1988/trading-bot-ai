"""
Gemini Agent — The Technical Analysis Expert.

Uses Google Gemini 2.5 Pro to perform deep technical analysis on real OHLCV data:
1. Chart pattern recognition (head & shoulders, flags, wedges, triangles, etc.)
2. Multi-timeframe trend alignment (short / medium / long)
3. Support & resistance level identification
4. Volatility regime classification (low / medium / high / extreme)
5. Probabilistic directional forecast with expected range
6. Independent signal scoring for each pending strategy signal
7. Recommended stop-loss level (price) and risk/reward ratio
8. Overall buy/sell/neutral rating — "sell" or "strong_sell" = capital preservation veto

Gemini 2.5 Pro with extended thinking gives the best pattern recognition
quality. Falls back to gemini-2.0-flash if 2.5 Pro is unavailable.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

log = logging.getLogger(__name__)

_gemini_available = False
try:
    import google.generativeai as genai
    _gemini_available = True
except ImportError:
    log.info("google-generativeai not installed — Gemini Agent disabled. "
             "Run: pip install google-generativeai")

# Primary model — best reasoning. Fallback if unavailable.
GEMINI_MODEL_PRIMARY  = "gemini-2.5-pro-preview-05-06"
GEMINI_MODEL_FALLBACK = "gemini-2.0-flash"
GEMINI_MODEL          = GEMINI_MODEL_PRIMARY   # updated in __init__ if fallback used


class GeminiAgent:
    """
    Technical analysis expert powered by Google Gemini.
    One instance shared across all ticks.
    """

    def __init__(self, api_key: str = ""):
        self.api_key  = api_key
        self.enabled  = bool(api_key) and _gemini_available
        self._model   = None
        self.model_name: str = GEMINI_MODEL_PRIMARY
        self.last_analysis: dict[str, dict] = {}
        self.last_run_at: Optional[str] = None
        self.total_calls:  int = 0
        self.total_errors: int = 0

        if not api_key:
            log.info("Gemini Agent: no GEMINI_API_KEY — technical analysis disabled")
        elif not _gemini_available:
            log.info("Gemini Agent: google-generativeai not installed — pip install google-generativeai")
        else:
            genai.configure(api_key=api_key)
            self._model = self._init_model(GEMINI_MODEL_PRIMARY)
            if self._model is None:
                log.info("Gemini 2.5 Pro unavailable — falling back to %s", GEMINI_MODEL_FALLBACK)
                self._model = self._init_model(GEMINI_MODEL_FALLBACK)
                self.model_name = GEMINI_MODEL_FALLBACK
            if self._model:
                log.info("Gemini Agent ready (model=%s)", self.model_name)
            else:
                log.error("Gemini Agent: all models failed to init — disabled")
                self.enabled = False

    def _init_model(self, model_name: str):
        try:
            return genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature":        0.05,    # near-deterministic for analysis
                    "top_p":              0.8,
                    "max_output_tokens":  2048,
                    "response_mime_type": "application/json",
                },
                system_instruction=(
                    "You are an elite quantitative crypto analyst. "
                    "You give actionable, precise technical analysis. "
                    "Your stop-loss recommendations are based on key support levels and ATR. "
                    "Respond ONLY with valid JSON — no markdown, no prose, no fences."
                ),
            )
        except Exception as exc:
            log.debug("Gemini model %s init failed: %s", model_name, exc)
            return None

    # ── Public API ────────────────────────────────────────────────────────────

    async def analyze_market(
        self,
        symbol: str,
        ohlcv: list,
        signals: list[dict],
    ) -> dict:
        """
        Full technical analysis for a symbol.

        Args:
            symbol: e.g. "BTC/USDT"
            ohlcv:  raw candle list [[ts, open, high, low, close, volume], ...] newest last
            signals: pending strategy signals for this symbol

        Returns analysis dict including recommended_stop_loss and risk_reward_ratio.
        """
        if not self.enabled:
            return self._empty_result(symbol)
        if not ohlcv:
            log.debug("Gemini: no OHLCV data for %s — skipping analysis", symbol)
            return self._empty_result(symbol)

        try:
            result = await self._run_analysis(symbol, ohlcv, signals)
            self.last_analysis[symbol] = result
            self.last_run_at = datetime.utcnow().isoformat()
            self.total_calls += 1
            return result
        except Exception as exc:
            log.warning("Gemini analysis for %s failed: %s", symbol, exc)
            self.total_errors += 1
            return self._empty_result(symbol)

    def get_status(self) -> dict:
        return {
            "enabled":        self.enabled,
            "model":          self.model_name,
            "role":           "Technical Analysis Expert",
            "last_run_at":    self.last_run_at,
            "total_calls":    self.total_calls,
            "total_errors":   self.total_errors,
            "cached_symbols": list(self.last_analysis.keys()),
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _run_analysis(
        self, symbol: str, ohlcv: list, signals: list[dict]
    ) -> dict:
        # Use last 80 candles for richer pattern context (2.5 Pro handles longer context)
        candles_subset = ohlcv[-80:]
        candle_rows = [
            f"{i+1:3}. O={c[1]:.4f} H={c[2]:.4f} L={c[3]:.4f} C={c[4]:.4f} V={c[5]:.0f}"
            for i, c in enumerate(candles_subset)
        ]
        candle_text = "\n".join(candle_rows)

        # Current price for SL recommendation context
        current_price = float(candles_subset[-1][4]) if candles_subset else 0

        signal_text = ""
        if signals:
            signal_lines = [
                f"  • {s.get('strategy','?')}: {s.get('side','?').upper()} "
                f"conf={s.get('confidence',0):.2f} lev={s.get('leverage',1)}x"
                for s in signals
            ]
            signal_text = "Pending signals to score:\n" + "\n".join(signal_lines)

        prompt = f"""Perform deep technical analysis for {symbol}.
Current price: {current_price:.4f}

Last {len(candles_subset)} candles (OHLCV, oldest→newest):
{candle_text}

{signal_text}

Return a JSON object with this EXACT structure (no extra keys, no markdown):
{{
  "symbol": "{symbol}",
  "trend": {{
    "short_term":  "bullish"|"bearish"|"sideways",
    "medium_term": "bullish"|"bearish"|"sideways",
    "long_term":   "bullish"|"bearish"|"sideways",
    "alignment":   "aligned"|"mixed"|"conflicting"
  }},
  "patterns": [
    {{"name": "<pattern>", "type": "bullish"|"bearish"|"neutral", "confidence": 0.0-1.0}}
  ],
  "key_levels": {{
    "support_1":    <nearest support price>,
    "support_2":    <next support price>,
    "resistance_1": <nearest resistance price>,
    "resistance_2": <next resistance price>
  }},
  "volatility": {{
    "regime":      "low"|"medium"|"high"|"extreme",
    "atr_estimate": <float — estimated ATR in price units>,
    "squeeze":      true|false
  }},
  "momentum": {{
    "rsi_estimate":  <float 0-100>,
    "macd_signal":   "bullish"|"bearish"|"neutral",
    "volume_trend":  "increasing"|"decreasing"|"flat"
  }},
  "forecast": {{
    "direction":          "up"|"down"|"sideways",
    "confidence":          0.0-1.0,
    "expected_range_pct":  <float — expected % move in next 1-4h>,
    "risk_reward_ratio":   <float — e.g. 2.5 means 2.5:1 reward:risk>,
    "timeframe":           "next 1-4 hours"
  }},
  "recommended_stop_loss": <price below nearest support or 2xATR from entry — null if no clear level>,
  "signal_scores": [
    {{
      "strategy":      "<name>",
      "side":          "buy"|"sell",
      "technical_score": 0.0-1.0,
      "assessment":    "strong"|"moderate"|"weak"|"against_trend"
    }}
  ],
  "overall_rating": "strong_buy"|"buy"|"neutral"|"sell"|"strong_sell",
  "analyst_notes":  "<2-3 sentence technical summary with specific price levels cited>"
}}"""

        response = await self._model.generate_content_async(prompt)
        text = response.text.strip()

        # Strip markdown fences (safety — response_mime_type should prevent these)
        if text.startswith("```"):
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else text
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        parsed = json.loads(text)
        parsed["fetched_at"] = datetime.utcnow().isoformat()
        parsed["model_used"] = self.model_name

        # Ensure recommended_stop_loss is present
        if "recommended_stop_loss" not in parsed:
            parsed["recommended_stop_loss"] = None

        return parsed

    @staticmethod
    def _empty_result(symbol: str) -> dict:
        return {
            "symbol":                symbol,
            "trend": {
                "short_term":  "sideways",
                "medium_term": "sideways",
                "long_term":   "sideways",
                "alignment":   "mixed",
            },
            "patterns":     [],
            "key_levels":   {"support_1": 0, "support_2": 0, "resistance_1": 0, "resistance_2": 0},
            "volatility":   {"regime": "medium", "atr_estimate": 0, "squeeze": False},
            "momentum":     {"rsi_estimate": 50, "macd_signal": "neutral", "volume_trend": "flat"},
            "forecast": {
                "direction":         "sideways",
                "confidence":        0.0,
                "expected_range_pct": 0,
                "risk_reward_ratio":  0,
                "timeframe":         "next 1-4 hours",
            },
            "recommended_stop_loss": None,
            "signal_scores":  [],
            "overall_rating": "neutral",
            "analyst_notes":  "Technical analysis unavailable — Gemini offline or no OHLCV data.",
            "fetched_at":     datetime.utcnow().isoformat(),
            "model_used":     "none",
        }


# ── Module-level singleton ────────────────────────────────────────────────────
gemini_agent: Optional[GeminiAgent] = None


def init_gemini(api_key: str) -> GeminiAgent:
    global gemini_agent
    gemini_agent = GeminiAgent(api_key)
    return gemini_agent
