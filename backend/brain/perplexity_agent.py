"""
Perplexity Agent — The News & Sentiment Expert.

Uses Perplexity's Sonar model (real-time web search + LLM reasoning) to:
1. Fetch live crypto news for each symbol under consideration
2. Score sentiment: bullish / bearish / neutral with confidence
3. Surface key events: whale moves, regulatory news, partnerships, hacks
4. Estimate news-driven price impact over the next 1–4 hours

Perplexity's API is OpenAI-compatible — we call it via httpx to avoid
adding the openai package as a dependency.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Optional

import httpx

log = logging.getLogger(__name__)

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL   = "sonar"          # real-time web search model


class PerplexityAgent:
    """
    News & sentiment expert powered by Perplexity Sonar.
    One instance shared across all ticks.
    """

    def __init__(self, api_key: str = ""):
        self.api_key   = api_key
        self.enabled   = bool(api_key)
        self.last_news: dict[str, dict] = {}   # symbol → latest analysis
        self.last_run_at: Optional[str] = None
        self.total_calls: int = 0
        self.total_errors: int = 0

        if not self.enabled:
            log.info("Perplexity Agent: no API key — news analysis disabled")
        else:
            log.info("Perplexity Agent initialized (model=%s)", PERPLEXITY_MODEL)

    # ── Public API ────────────────────────────────────────────────────────────

    async def analyze_news(self, symbols: list[str]) -> dict[str, dict]:
        """
        For each symbol, ask Perplexity for:
        - Recent news summary (last 4 hours)
        - Sentiment score (-1.0 to +1.0)
        - Key event tags
        - Short-term impact estimate

        Returns dict: symbol → {sentiment, score, headlines, impact, sources}
        """
        if not self.enabled or not symbols:
            return {}

        results: dict[str, dict] = {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for symbol in symbols:
                try:
                    result = await self._query_symbol(client, symbol)
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
            "enabled":      self.enabled,
            "model":        PERPLEXITY_MODEL,
            "role":         "News & Sentiment Expert",
            "last_run_at":  self.last_run_at,
            "total_calls":  self.total_calls,
            "total_errors": self.total_errors,
            "cached_symbols": list(self.last_news.keys()),
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _query_symbol(self, client: httpx.AsyncClient, symbol: str) -> dict:
        base = symbol.replace("/USDT", "").replace("/USD", "")
        prompt = (
            f"Analyze the latest news and market sentiment for {base} (cryptocurrency) "
            f"in the past 4 hours. Focus on:\n"
            f"1. Major news events (regulatory, partnerships, hacks, large trades)\n"
            f"2. Social sentiment on X/Twitter and Reddit\n"
            f"3. Any whale activity or large on-chain movements\n"
            f"4. Your overall sentiment: BULLISH, BEARISH, or NEUTRAL\n\n"
            f"Respond ONLY with a valid JSON object:\n"
            f'{{"sentiment": "BULLISH"|"BEARISH"|"NEUTRAL", '
            f'"score": <float -1.0 to 1.0>, '
            f'"headlines": [<top 3 headline strings>], '
            f'"key_events": [<event tags like "SEC approval", "hack", "whale buy">], '
            f'"impact_estimate": "strong bullish"|"mild bullish"|"neutral"|"mild bearish"|"strong bearish", '
            f'"confidence": <float 0.0 to 1.0>, '
            f'"summary": "<2-3 sentence summary>"}}'
        )

        payload = {
            "model": PERPLEXITY_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional crypto news analyst. "
                        "Always respond with valid JSON only — no markdown, no extra text."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.2,
            "search_recency_filter": "hour",
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

        # Strip markdown fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        parsed = json.loads(content)
        parsed["symbol"]     = symbol
        parsed["fetched_at"] = datetime.utcnow().isoformat()

        # Normalise score to float
        parsed["score"] = float(parsed.get("score", 0.0))
        parsed["confidence"] = float(parsed.get("confidence", 0.5))
        return parsed

    @staticmethod
    def _empty_result(symbol: str) -> dict:
        return {
            "symbol":          symbol,
            "sentiment":       "NEUTRAL",
            "score":           0.0,
            "headlines":       [],
            "key_events":      [],
            "impact_estimate": "neutral",
            "confidence":      0.0,
            "summary":         "News data unavailable.",
            "fetched_at":      datetime.utcnow().isoformat(),
        }


# Module-level singleton — configured after settings load
perplexity_agent: Optional[PerplexityAgent] = None


def init_perplexity(api_key: str) -> PerplexityAgent:
    global perplexity_agent
    perplexity_agent = PerplexityAgent(api_key)
    return perplexity_agent
