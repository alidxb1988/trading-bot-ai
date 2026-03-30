"""
Perplexity Agent — The News & Sentiment Expert.

Uses Perplexity Sonar Pro (real-time web search + deep reasoning) to:
1. Fetch live crypto headlines from the past hour
2. Score sentiment: -1.0 (extreme bearish) to +1.0 (extreme bullish)
3. Detect key events: whale moves, regulatory news, partnerships, hacks, liquidations
4. Measure market fear/greed: extreme_fear → contrarian buy signal
5. Estimate news-driven price impact over the next 1–4 hours

Capital preservation integration:
  • score < -0.4          → Claude applies hard buy veto
  • fear_greed = extreme_greed → Claude reduces leverage on new buys
  • fear_greed = extreme_fear  → Claude considers cautious contrarian buys

API: Perplexity is OpenAI-compatible. Called via httpx.
Model: sonar-pro (deeper reasoning than base sonar).
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional

import httpx

log = logging.getLogger(__name__)

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL   = "sonar-pro"       # upgraded from sonar — deeper web reasoning


class PerplexityAgent:
    """
    News & sentiment expert powered by Perplexity Sonar Pro.
    One instance shared across all ticks.
    """

    def __init__(self, api_key: str = ""):
        self.api_key      = api_key
        self.enabled      = bool(api_key)
        self.last_news:   dict[str, dict] = {}
        self.last_run_at: Optional[str]   = None
        self.total_calls: int = 0
        self.total_errors: int = 0

        if not self.enabled:
            log.info("Perplexity Agent: no PERPLEXITY_API_KEY — news analysis disabled")
        else:
            log.info("Perplexity Agent ready (model=%s)", PERPLEXITY_MODEL)

    # ── Public API ────────────────────────────────────────────────────────────

    async def analyze_news(self, symbols: list[str]) -> dict[str, dict]:
        """
        For each symbol, fetch:
          - Sentiment score (-1.0 → +1.0)
          - Headlines (top 3)
          - Key event tags
          - Fear/greed signal
          - Short-term impact estimate

        Returns: symbol → result dict
        """
        if not self.enabled or not symbols:
            return {}

        results: dict[str, dict] = {}
        async with httpx.AsyncClient(timeout=35.0) as client:
            for symbol in symbols:
                try:
                    result = await self._query_symbol_with_retry(client, symbol)
                    results[symbol] = result
                    self.last_news[symbol] = result
                except Exception as exc:
                    log.warning("Perplexity news for %s failed: %s", symbol, exc)
                    self.total_errors += 1
                    results[symbol] = self._empty_result(symbol)

        self.last_run_at = datetime.utcnow().isoformat()
        self.total_calls += len(symbols)
        return results

    def get_status(self) -> dict:
        return {
            "enabled":         self.enabled,
            "model":           PERPLEXITY_MODEL,
            "role":            "News & Sentiment Expert",
            "last_run_at":     self.last_run_at,
            "total_calls":     self.total_calls,
            "total_errors":    self.total_errors,
            "cached_symbols":  list(self.last_news.keys()),
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _query_symbol_with_retry(
        self, client: httpx.AsyncClient, symbol: str
    ) -> dict:
        """Query with one retry on HTTP 429 (rate limit) after 3 s backoff."""
        try:
            return await self._query_symbol(client, symbol)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                log.info("Perplexity rate limit for %s — retrying in 3s", symbol)
                await asyncio.sleep(3)
                return await self._query_symbol(client, symbol)
            raise

    async def _query_symbol(self, client: httpx.AsyncClient, symbol: str) -> dict:
        base = symbol.replace("/USDT", "").replace("/USD", "")

        prompt = (
            f"Analyze the latest news and market sentiment for {base} cryptocurrency "
            f"RIGHT NOW (past 60 minutes). Focus on:\n"
            f"1. Major breaking events: regulatory actions, exchange listings/delistings, "
            f"   protocol hacks, large liquidations, whale on-chain moves\n"
            f"2. Social media sentiment on X/Twitter and Reddit (fear vs greed)\n"
            f"3. Whether the overall market mood is extreme_fear, fear, neutral, greed, "
            f"   or extreme_greed for {base} specifically\n"
            f"4. An honest numeric sentiment score: -1.0 (very bearish) to +1.0 (very bullish)\n\n"
            f"A score below -0.4 will automatically block new long positions — be accurate.\n\n"
            f"Respond ONLY with this exact JSON (no markdown, no extra text):\n"
            f'{{'
            f'"sentiment": "BULLISH"|"BEARISH"|"NEUTRAL", '
            f'"score": <float -1.0 to 1.0>, '
            f'"fear_greed_signal": "extreme_fear"|"fear"|"neutral"|"greed"|"extreme_greed", '
            f'"headlines": [<top 3 most impactful headlines as strings>], '
            f'"key_events": [<short event tags, e.g. "SEC lawsuit", "whale bought 5000 BTC", "exchange hack">], '
            f'"impact_estimate": "strong bullish"|"mild bullish"|"neutral"|"mild bearish"|"strong bearish", '
            f'"confidence": <float 0.0 to 1.0>, '
            f'"summary": "<2-3 sentence factual summary>"}}'
        )

        payload = {
            "model": PERPLEXITY_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional real-time crypto news analyst. "
                        "Your sentiment scores directly influence trading decisions — be accurate and honest. "
                        "Respond ONLY with valid JSON. No markdown."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens":             600,
            "temperature":            0.1,   # near-deterministic for factual analysis
            "search_recency_filter":  "hour",
            "return_images":          False,
            "return_related_questions": False,
        }

        resp = await client.post(
            PERPLEXITY_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type":  "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Strip markdown fences if model adds them despite instructions
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        parsed = json.loads(content)
        parsed["symbol"]     = symbol
        parsed["fetched_at"] = datetime.utcnow().isoformat()

        # Normalise numeric fields
        parsed["score"]      = float(parsed.get("score", 0.0))
        parsed["confidence"] = float(parsed.get("confidence", 0.5))

        # Default fear_greed_signal if missing
        if "fear_greed_signal" not in parsed:
            score = parsed["score"]
            if score < -0.5:
                parsed["fear_greed_signal"] = "extreme_fear"
            elif score < -0.2:
                parsed["fear_greed_signal"] = "fear"
            elif score > 0.5:
                parsed["fear_greed_signal"] = "extreme_greed"
            elif score > 0.2:
                parsed["fear_greed_signal"] = "greed"
            else:
                parsed["fear_greed_signal"] = "neutral"

        return parsed

    @staticmethod
    def _empty_result(symbol: str) -> dict:
        return {
            "symbol":            symbol,
            "sentiment":         "NEUTRAL",
            "score":             0.0,
            "fear_greed_signal": "neutral",
            "headlines":         [],
            "key_events":        [],
            "impact_estimate":   "neutral",
            "confidence":        0.0,
            "summary":           "News data unavailable.",
            "fetched_at":        datetime.utcnow().isoformat(),
        }


# ── Module-level singleton ────────────────────────────────────────────────────
perplexity_agent: Optional[PerplexityAgent] = None


def init_perplexity(api_key: str) -> PerplexityAgent:
    global perplexity_agent
    perplexity_agent = PerplexityAgent(api_key)
    return perplexity_agent
