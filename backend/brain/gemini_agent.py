"""
Gemini Agent — The Market Analysis Expert.

Uses Google Gemini (gemini-2.0-flash) to perform deep technical analysis:
1. Pattern recognition on OHLCV candle data (head & shoulders, flags, wedges, etc.)
2. Multi-timeframe trend alignment (short / medium / long term)
3. Support/resistance level identification
4. Volatility regime classification (low / medium / high)
5. Probabilistic price range forecast for next candle session
6. Strategy signal scoring — independently rates each pending signal

Gemini's flash model is fast and cost-effective for per-tick analysis.
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

GEMINI_MODEL = "gemini-2.0-flash"


class GeminiAgent:
    """
    Technical analysis expert powered by Google Gemini.
    One instance shared across all ticks.
    """

    def __init__(self, api_key: str = ""):
        self.api_key  = api_key
        self.enabled  = bool(api_key) and _gemini_available
        self._model   = None
        self.last_analysis: dict[str, dict] = {}  # symbol → latest analysis
        self.last_run_at: Optional[str] = None
        self.total_calls: int = 0
        self.total_errors: int = 0

        if not api_key:
            log.info("Gemini Agent: no API key — technical analysis disabled")
        elif not _gemini_available:
            log.info("Gemini Agent: google-generativeai not installed")
        else:
            try:
                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel(
                    model_name=GEMINI_MODEL,
                    generation_config={
                        "temperature":       0.1,
                        "top_p":             0.8,
                        "max_output_tokens": 1024,
                        "response_mime_type": "application/json",
                    },
                    system_instruction=(
                        "You are an elite quantitative analyst specializing in "
                        "cryptocurrency technical analysis. Respond ONLY with valid JSON."
                    ),
                )
                log.info("Gemini Agent initialized (model=%s)", GEMINI_MODEL)
            except Exception as exc:
                log.error("Gemini Agent init failed: %s", exc)
                self.enabled = False

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
            ohlcv:  list of [ts, open, high, low, close, volume] candles (most recent last)
            signals: pending strategy signals for this symbol

        Returns dict with technical analysis, pattern recognition, and signal scores.
        """
        if not self.enabled or not ohlcv:
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

    async def analyze_all(
        self,
        market_data: dict[str, list],
        signals: list[dict],
    ) -> dict[str, dict]:
        """
        Analyze all symbols that have pending signals.
        Returns dict: symbol → analysis result.
        """
        if not self.enabled:
            return {}

        # Only analyze symbols that have pending signals
        active_symbols = list({s.get("symbol") for s in signals if s.get("symbol")})
        results: dict[str, dict] = {}

        for symbol in active_symbols:
            ohlcv = market_data.get(symbol, [])
            sym_signals = [s for s in signals if s.get("symbol") == symbol]
            results[symbol] = await self.analyze_market(symbol, ohlcv, sym_signals)

        return results

    def get_status(self) -> dict:
        return {
            "enabled":         self.enabled,
            "model":           GEMINI_MODEL,
            "role":            "Technical Analysis Expert",
            "last_run_at":     self.last_run_at,
            "total_calls":     self.total_calls,
            "total_errors":    self.total_errors,
            "cached_symbols":  list(self.last_analysis.keys()),
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _run_analysis(
        self, symbol: str, ohlcv: list, signals: list[dict]
    ) -> dict:
        # Summarise candles — send last 50 to keep prompt short
        candles_subset = ohlcv[-50:]
        candle_rows = [
            f"{i+1}. O={c[1]:.4f} H={c[2]:.4f} L={c[3]:.4f} C={c[4]:.4f} V={c[5]:.0f}"
            for i, c in enumerate(candles_subset)
        ]
        candle_text = "\n".join(candle_rows)

        signal_text = ""
        if signals:
            signal_lines = [
                f"- {s.get('strategy','?')}: {s.get('side','?').upper()} "
                f"conf={s.get('confidence',0):.2f} lev={s.get('leverage',1)}x"
                for s in signals
            ]
            signal_text = "Pending signals:\n" + "\n".join(signal_lines)

        prompt = f"""Perform comprehensive technical analysis for {symbol}.

Last {len(candles_subset)} candles (OHLCV, oldest first):
{candle_text}

{signal_text}

Analyze and return JSON with this exact structure:
{{
  "symbol": "{symbol}",
  "trend": {{
    "short_term": "bullish"|"bearish"|"sideways",
    "medium_term": "bullish"|"bearish"|"sideways",
    "long_term": "bullish"|"bearish"|"sideways",
    "alignment": "aligned"|"mixed"|"conflicting"
  }},
  "patterns": [
    {{"name": "<pattern name>", "type": "bullish"|"bearish"|"neutral", "confidence": 0.0-1.0}}
  ],
  "key_levels": {{
    "support_1": <price>,
    "support_2": <price>,
    "resistance_1": <price>,
    "resistance_2": <price>
  }},
  "volatility": {{
    "regime": "low"|"medium"|"high"|"extreme",
    "atr_estimate": <float>,
    "squeeze": true|false
  }},
  "momentum": {{
    "rsi_estimate": <float 0-100>,
    "macd_signal": "bullish"|"bearish"|"neutral",
    "volume_trend": "increasing"|"decreasing"|"flat"
  }},
  "forecast": {{
    "direction": "up"|"down"|"sideways",
    "confidence": 0.0-1.0,
    "expected_range_pct": <float>,
    "timeframe": "next 1-4 hours"
  }},
  "signal_scores": [
    {{"strategy": "<name>", "side": "buy"|"sell", "technical_score": 0.0-1.0, "assessment": "strong"|"moderate"|"weak"|"against_trend"}}
  ],
  "overall_rating": "strong_buy"|"buy"|"neutral"|"sell"|"strong_sell",
  "analyst_notes": "<2-3 sentence technical summary>"
}}"""

        # Gemini's generate_content_async for async support
        response = await self._model.generate_content_async(prompt)
        text = response.text.strip()

        # Strip markdown fences
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        parsed = json.loads(text)
        parsed["fetched_at"] = datetime.utcnow().isoformat()
        return parsed

    @staticmethod
    def _empty_result(symbol: str) -> dict:
        return {
            "symbol":          symbol,
            "trend":           {"short_term": "sideways", "medium_term": "sideways",
                                "long_term": "sideways", "alignment": "mixed"},
            "patterns":        [],
            "key_levels":      {"support_1": 0, "support_2": 0,
                                "resistance_1": 0, "resistance_2": 0},
            "volatility":      {"regime": "medium", "atr_estimate": 0, "squeeze": False},
            "momentum":        {"rsi_estimate": 50, "macd_signal": "neutral",
                                "volume_trend": "flat"},
            "forecast":        {"direction": "sideways", "confidence": 0.0,
                                "expected_range_pct": 0, "timeframe": "next 1-4 hours"},
            "signal_scores":   [],
            "overall_rating":  "neutral",
            "analyst_notes":   "Technical analysis unavailable.",
            "fetched_at":      datetime.utcnow().isoformat(),
        }


# Module-level singleton — configured after settings load
gemini_agent: Optional[GeminiAgent] = None


def init_gemini(api_key: str) -> GeminiAgent:
    global gemini_agent
    gemini_agent = GeminiAgent(api_key)
    return gemini_agent
