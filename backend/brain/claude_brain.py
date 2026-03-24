"""
Claude Brain — The AI Orchestrator.

Three-agent architecture:
  • Perplexity (Sonar)     → News & Sentiment Expert
  • Gemini (Flash 2.0)     → Technical Analysis Expert
  • Claude (Opus 4.6)      → Final Orchestrator / Decision Maker

Flow each tick:
  1. Collect all pending strategy signals
  2. Perplexity fetches live news/sentiment for each symbol
  3. Gemini performs deep technical analysis for each symbol
  4. Claude receives signals + Perplexity insights + Gemini analysis via tool calls
  5. Claude reasons holistically and issues final approve/reject/modify decisions
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Any, Optional

log = logging.getLogger(__name__)

# ── Lazy imports ──────────────────────────────────────────────────────────────

_anthropic_available = False
try:
    from anthropic import AsyncAnthropic
    _anthropic_available = True
except ImportError:
    log.warning("anthropic package not installed — Claude Brain disabled. "
                "Run: pip install anthropic")


# ── System prompt (cached via prompt caching) ─────────────────────────────────

SYSTEM_PROMPT = """You are the AI orchestrator of a 3-agent autonomous cryptocurrency trading system.

Your team:
- **Perplexity (News Expert)**: Provides real-time news sentiment, headline analysis, and event detection
- **Gemini (Analysis Expert)**: Provides technical pattern recognition, multi-timeframe trend analysis, and signal scoring
- **You (Claude, Orchestrator)**: Synthesize all inputs and make final trading decisions

Your job:
1. Query your agents (use the tools below) to gather their expert analysis
2. Synthesize technical signals + news sentiment + Polymarket prediction markets
3. Make final go/no-go decisions on each pending strategy signal
4. Apply portfolio-level risk management (correlation, exposure, drawdown)

Signal weighting framework:
- Technical signals (from strategies + Gemini): 40%
- News/sentiment (from Perplexity): 30%
- Prediction markets (Polymarket): 30%

Portfolio risk rules (ENFORCE ALWAYS):
- No single position > 10% of portfolio
- Reject any signal if daily drawdown > 15%
- Don't approve correlated longs simultaneously at high leverage (BTC+ETH+SOL all long)
- Minimum signal confidence after synthesis: 0.65
- When Perplexity detects "extreme bearish" news, override bullish technicals and reject

Decision output format (call execute_trade_decision with this):
{
  "decisions": [
    {
      "symbol": "BTC/USDT",
      "action": "approve" | "reject" | "modify",
      "side": "buy" | "sell",
      "confidence": 0.0-1.0,
      "reason": "concise explanation citing agents",
      "modified_leverage": null or integer,
      "modified_size_pct": null or float
    }
  ],
  "portfolio_notes": "overall assessment",
  "risk_level": "low" | "medium" | "high"
}

Be decisive. Cite your agents when explaining decisions. Capital preservation is paramount."""


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_news_sentiment",
        "description": (
            "Query Perplexity (News Expert) for live news, sentiment scores, "
            "and key events for one or more crypto symbols. "
            "Always call this before deciding on any signal."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of trading pairs, e.g. [\"BTC/USDT\", \"ETH/USDT\"]"
                }
            },
            "required": ["symbols"]
        }
    },
    {
        "name": "get_technical_analysis",
        "description": (
            "Query Gemini (Analysis Expert) for deep technical analysis: "
            "patterns, trend alignment, support/resistance, and signal scoring. "
            "Call this for any symbol you want a deeper read on."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Trading pair, e.g. BTC/USDT"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_strategy_signals",
        "description": "Get full details of all pending signals from the 5 sub-strategies.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strategy": {
                    "type": "string",
                    "description": "Filter by strategy (hft/ai_multi/dca/grid/gomale) or 'all'",
                    "default": "all"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_portfolio_status",
        "description": "Get current balance, open positions, daily P&L, and drawdown metrics.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_polymarket_odds",
        "description": "Get Polymarket prediction market probabilities for crypto price targets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Asset base symbol: BTC, ETH, SOL, etc."
                }
            },
            "required": []
        }
    },
    {
        "name": "execute_trade_decision",
        "description": (
            "Submit your final trade decisions for execution. "
            "Call this LAST, after consulting all agents and gathering context."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "symbol":             {"type": "string"},
                            "action":             {"type": "string", "enum": ["approve", "reject", "modify"]},
                            "side":               {"type": "string", "enum": ["buy", "sell"]},
                            "confidence":         {"type": "number"},
                            "reason":             {"type": "string"},
                            "modified_leverage":  {"type": ["integer", "null"]},
                            "modified_size_pct":  {"type": ["number", "null"]}
                        },
                        "required": ["symbol", "action", "side", "confidence", "reason"]
                    }
                },
                "portfolio_notes": {"type": "string"},
                "risk_level":      {"type": "string", "enum": ["low", "medium", "high"]}
            },
            "required": ["decisions", "portfolio_notes", "risk_level"]
        }
    }
]


# ── ClaudeBrain ───────────────────────────────────────────────────────────────

class ClaudeBrain:
    """
    The orchestrator agent. Coordinates Perplexity + Gemini + itself (Claude)
    to make final trading decisions each engine tick.
    """

    def __init__(self):
        self.enabled = _anthropic_available
        self._client: Optional[Any] = None

        # Agent references (set via wire_agents)
        self._perplexity = None
        self._gemini     = None

        # State
        self.last_reasoning: str = ""
        self.last_decision: dict = {}
        self.last_run_at: Optional[str] = None
        self.total_calls: int = 0
        self.total_approved: int = 0
        self.total_rejected: int = 0

        # Per-tick context (populated before each agentic loop)
        self._ctx_signals:    list  = []
        self._ctx_market:     dict  = {}
        self._ctx_portfolio:  dict  = {}
        self._ctx_polymarket: dict  = {}

        # Cached agent outputs for this tick (populated lazily via tools)
        self._news_cache:     dict  = {}
        self._gemini_cache:   dict  = {}

        if self.enabled:
            try:
                self._client = AsyncAnthropic()
                log.info("Claude Brain (Orchestrator) initialized — model=claude-opus-4-6")
            except Exception as exc:
                log.error("Claude Brain init failed: %s", exc)
                self.enabled = False

    def wire_agents(self, perplexity, gemini):
        """Attach sub-agents after they are initialised with API keys."""
        self._perplexity = perplexity
        self._gemini     = gemini
        log.info("Claude Brain wired — Perplexity=%s  Gemini=%s",
                 getattr(perplexity, "enabled", False),
                 getattr(gemini, "enabled", False))

    # ── Public API ────────────────────────────────────────────────────────────

    async def analyze_and_decide(
        self,
        strategy_signals: list[dict],
        market_data: dict,
        portfolio: dict,
        polymarket: dict,
    ) -> list[dict]:
        """
        Main entry point called once per engine tick.
        Returns list of trade decisions: [{symbol, action, side, confidence, reason, ...}]
        """
        if not self.enabled or not self._client:
            return self._passthrough(strategy_signals, "Brain disabled")

        if not strategy_signals:
            return []

        # Populate per-tick context
        self._ctx_signals   = strategy_signals
        self._ctx_market    = market_data
        self._ctx_portfolio = portfolio
        self._ctx_polymarket = polymarket

        # Clear cached agent results for fresh analysis
        self._news_cache   = {}
        self._gemini_cache = {}

        self.total_calls += 1
        start = time.monotonic()

        try:
            decisions = await self._run_agentic_loop(strategy_signals)
            log.info("Claude Brain done in %.1fs — %d decisions", time.monotonic() - start, len(decisions))
            self.last_run_at = datetime.utcnow().isoformat()
            return decisions
        except Exception as exc:
            log.error("Claude Brain error: %s", exc, exc_info=True)
            return self._passthrough(strategy_signals, f"Error: {exc}", confidence_scale=0.8)

    def get_status(self) -> dict:
        return {
            "enabled":               self.enabled,
            "model":                 "claude-opus-4-6",
            "thinking":              "adaptive",
            "role":                  "Orchestrator",
            "last_run_at":           self.last_run_at,
            "total_calls":           self.total_calls,
            "total_approved":        self.total_approved,
            "total_rejected":        self.total_rejected,
            "last_reasoning_preview": self.last_reasoning[:500] if self.last_reasoning else "",
            "last_decision":         self.last_decision,
            "agents": {
                "perplexity": getattr(self._perplexity, "get_status", lambda: {})(),
                "gemini":     getattr(self._gemini,     "get_status", lambda: {})(),
            }
        }

    # ── Agentic loop ─────────────────────────────────────────────────────────

    async def _run_agentic_loop(self, strategy_signals: list[dict]) -> list[dict]:
        messages = [{"role": "user", "content": self._build_user_message(strategy_signals)}]
        final_decisions: list[dict] = []

        for _round in range(10):
            async with self._client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=8192,
                thinking={"type": "adaptive"},
                system=[
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                tools=TOOLS,
                messages=messages,
            ) as stream:
                response = await stream.get_final_message()

            # Capture thinking block
            for block in response.content:
                if block.type == "thinking":
                    self.last_reasoning = block.thinking
                    break

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if block.type == "text":
                        final_decisions = self._extract_decisions_from_text(
                            block.text, strategy_signals
                        )
                break

            if response.stop_reason != "tool_use":
                break

            # Handle tool calls
            tool_results = []
            called_execute = False

            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_output = await self._dispatch_tool(block.name, block.input)

                if block.name == "execute_trade_decision":
                    called_execute = True
                    final_decisions = block.input.get("decisions", [])
                    self.last_decision = block.input
                    for d in final_decisions:
                        if d.get("action") == "approve":
                            self.total_approved += 1
                        elif d.get("action") == "reject":
                            self.total_rejected += 1

                tool_results.append({
                    "type":        "tool_result",
                    "tool_use_id": block.id,
                    "content":     json.dumps(tool_output),
                })

            messages.append({"role": "user", "content": tool_results})

            if called_execute:
                break

        return final_decisions

    # ── Tool dispatcher ───────────────────────────────────────────────────────

    async def _dispatch_tool(self, name: str, inputs: dict) -> dict:
        try:
            if name == "get_news_sentiment":
                return await self._tool_news_sentiment(inputs)
            elif name == "get_technical_analysis":
                return await self._tool_technical_analysis(inputs)
            elif name == "get_strategy_signals":
                return self._tool_strategy_signals(inputs)
            elif name == "get_portfolio_status":
                return self._tool_portfolio()
            elif name == "get_polymarket_odds":
                return self._tool_polymarket(inputs)
            elif name == "execute_trade_decision":
                return {"status": "captured", "count": len(inputs.get("decisions", []))}
            else:
                return {"error": f"Unknown tool: {name}"}
        except Exception as exc:
            log.warning("Tool %s error: %s", name, exc)
            return {"error": str(exc)}

    # ── Tool handlers ─────────────────────────────────────────────────────────

    async def _tool_news_sentiment(self, inputs: dict) -> dict:
        symbols = inputs.get("symbols", [])
        if not symbols:
            symbols = list({s.get("symbol") for s in self._ctx_signals})

        # Check cache first
        uncached = [s for s in symbols if s not in self._news_cache]
        if uncached and self._perplexity and self._perplexity.enabled:
            fresh = await self._perplexity.analyze_news(uncached)
            self._news_cache.update(fresh)

        return {
            "source":  "Perplexity Sonar (real-time web search)",
            "results": {
                sym: self._news_cache.get(sym, {"sentiment": "NEUTRAL", "score": 0,
                                                "summary": "No data", "confidence": 0})
                for sym in symbols
            }
        }

    async def _tool_technical_analysis(self, inputs: dict) -> dict:
        symbol = inputs.get("symbol", "")
        if not symbol:
            return {"error": "symbol required"}

        if symbol not in self._gemini_cache:
            if self._gemini and self._gemini.enabled:
                ohlcv = self._ctx_market.get(symbol, [])
                sym_signals = [s for s in self._ctx_signals if s.get("symbol") == symbol]
                result = await self._gemini.analyze_market(symbol, ohlcv, sym_signals)
                self._gemini_cache[symbol] = result
            else:
                self._gemini_cache[symbol] = {"note": "Gemini not available", "symbol": symbol}

        return {
            "source": "Gemini 2.0 Flash (technical pattern analysis)",
            "analysis": self._gemini_cache.get(symbol, {})
        }

    def _tool_strategy_signals(self, inputs: dict) -> dict:
        filt = inputs.get("strategy", "all")
        sigs = self._ctx_signals if filt == "all" else \
               [s for s in self._ctx_signals if s.get("strategy") == filt]
        return {"count": len(sigs), "signals": sigs}

    def _tool_portfolio(self) -> dict:
        p = self._ctx_portfolio
        return {
            "balance_usdt":  p.get("balance", 0),
            "open_trades":   p.get("open_trades", 0),
            "daily_pnl_pct": p.get("daily_pnl_pct", 0),
            "drawdown_pct":  p.get("drawdown_pct", 0),
            "risk_level":    p.get("risk_level", "medium"),
        }

    def _tool_polymarket(self, inputs: dict) -> dict:
        sym = inputs.get("symbol", "").upper().replace("/USDT", "")
        markets = self._ctx_polymarket.get(sym, self._ctx_polymarket)
        return {"symbol": sym, "markets": markets if isinstance(markets, list) else []}

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _build_user_message(self, strategy_signals: list[dict]) -> str:
        lines = [
            f"- {s.get('strategy','?').upper()} | {s.get('symbol')} | "
            f"{s.get('side','?').upper()} | conf={s.get('confidence',0):.2f} | "
            f"lev={s.get('leverage',1)}x | price={s.get('price',0):.4f}"
            for s in strategy_signals
        ]
        return (
            f"**{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} — "
            f"{len(strategy_signals)} pending signal(s):**\n"
            + "\n".join(lines)
            + "\n\n"
            "Steps:\n"
            "1. `get_portfolio_status` — check current risk\n"
            "2. `get_news_sentiment` — ask Perplexity for news on all symbols\n"
            "3. `get_technical_analysis` — ask Gemini for technical analysis\n"
            "4. `get_polymarket_odds` — check prediction market sentiment\n"
            "5. `execute_trade_decision` — issue your final decisions\n\n"
            "Synthesize all three sources. Be selective."
        )

    def _extract_decisions_from_text(
        self, text: str, original_signals: list[dict]
    ) -> list[dict]:
        try:
            s, e = text.find("{"), text.rfind("}") + 1
            if s >= 0 and e > s:
                parsed = json.loads(text[s:e])
                if "decisions" in parsed:
                    return parsed["decisions"]
        except (json.JSONDecodeError, ValueError):
            pass
        log.warning("Claude Brain: could not extract decisions — approving at 0.65")
        return self._passthrough(original_signals, "Fallback approval", confidence_scale=0.65/0.8)

    @staticmethod
    def _passthrough(
        signals: list[dict], reason: str, confidence_scale: float = 1.0
    ) -> list[dict]:
        return [
            {
                "symbol":     s.get("symbol"),
                "action":     "approve",
                "side":       s.get("side", "buy"),
                "confidence": min(s.get("confidence", 0.7) * confidence_scale, 0.9),
                "reason":     reason,
            }
            for s in signals
        ]


# ── Global singleton ──────────────────────────────────────────────────────────
claude_brain = ClaudeBrain()
