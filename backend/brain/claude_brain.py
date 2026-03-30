"""
Claude Brain — The AI Orchestrator.

Three-agent architecture:
  • Perplexity (Sonar Pro)   → News & Sentiment Expert     (real-time web search)
  • Gemini (2.5 Pro)         → Technical Analysis Expert   (pattern recognition)
  • Claude (Opus 4.6)        → Orchestrator / Final Decider (adaptive thinking)

Capital Preservation Mode (ALWAYS ON):
  ─ All three agents must be consulted before any buy is approved
  ─ Perplexity score < -0.4  →  hard veto on buys (no override)
  ─ Gemini rating sell/strong_sell  →  reject buy signals
  ─ Drawdown > 10%  →  halve all leverages
  ─ Drawdown > 15%  →  reject everything except closing positions
  ─ Correlated longs (BTC+ETH+SOL all long)  →  reject newest
  ─ Same symbol+side already open  →  reject (no doubling up)
  ─ Missing AI decision for a symbol  →  reject (engine default)

Signal weighting (dynamic based on agent availability):
  All online:          Technical 40% / News 30% / Polymarket 30%
  Gemini offline:      Technical 25% / News 45% / Polymarket 30%
  Perplexity offline:  Technical 60% / News  0% / Polymarket 40%
  Both offline:        min confidence 0.85 required to approve
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Any, Optional

log = logging.getLogger(__name__)

# ── Lazy import ───────────────────────────────────────────────────────────────

_anthropic_available = False
try:
    from anthropic import AsyncAnthropic
    _anthropic_available = True
except ImportError:
    log.warning("anthropic not installed — Claude Brain disabled. pip install anthropic")


# ── System prompt builder ─────────────────────────────────────────────────────

def _build_system_prompt(perplexity_online: bool, gemini_online: bool) -> str:
    """Build context-aware system prompt reflecting which agents are available."""

    if perplexity_online and gemini_online:
        weight_section = (
            "Signal weighting (ALL agents online — maximum intelligence):\n"
            "  • Technical signals (strategies + Gemini): 40%\n"
            "  • News/sentiment (Perplexity):              30%\n"
            "  • Prediction markets (Polymarket):          30%\n"
            "  REQUIRED: Call BOTH get_news_sentiment AND get_technical_analysis before deciding."
        )
    elif gemini_online and not perplexity_online:
        weight_section = (
            "Signal weighting (Perplexity OFFLINE — news blind spot):\n"
            "  • Technical signals (strategies + Gemini): 60%\n"
            "  • Prediction markets (Polymarket):          40%\n"
            "  WARNING: No news data. Be extra conservative on buys. Raise min confidence to 0.75.\n"
            "  REQUIRED: Call get_technical_analysis before deciding."
        )
    elif perplexity_online and not gemini_online:
        weight_section = (
            "Signal weighting (Gemini OFFLINE — chart blind spot):\n"
            "  • News/sentiment (Perplexity): 45%\n"
            "  • Prediction markets (Polymarket): 30%\n"
            "  • Strategy signals only:          25%\n"
            "  WARNING: No chart data. Only approve signals with strong news backing.\n"
            "  REQUIRED: Call get_news_sentiment before deciding."
        )
    else:
        weight_section = (
            "Signal weighting (BOTH sub-agents OFFLINE — degraded mode):\n"
            "  • Strategy signals only: 100%\n"
            "  CRITICAL: No AI sub-agents available. Minimum confidence required: 0.85.\n"
            "  Only approve the single highest-confidence signal per tick."
        )

    return f"""You are the orchestrating AI of a 3-agent autonomous cryptocurrency trading system.
Your primary directive: PRESERVE CAPITAL. Never approve a trade you are not highly confident in.

Your expert team:
  • Perplexity (News Expert)   — real-time web search, headline sentiment, event detection
  • Gemini (Analysis Expert)   — technical patterns, multi-timeframe trends, signal scoring
  • You (Claude, Orchestrator) — synthesize all inputs, apply risk rules, make final decisions

{weight_section}

══ CAPITAL PRESERVATION VETO RULES (MANDATORY — no exceptions) ══

1. NEWS VETO: If Perplexity returns score < -0.4 for a symbol → REJECT all BUY signals for it.
   No other analysis overrides this. Negative news = real risk of loss.

2. TECHNICAL VETO: If Gemini returns overall_rating = "sell" or "strong_sell" → REJECT buy signals.

3. DRAWDOWN ESCALATION:
   • drawdown_pct > 5%   → reduce approved leverage to max 3x
   • drawdown_pct > 10%  → reduce approved leverage to max 2x, reject all new longs with leverage > 2
   • drawdown_pct > 15%  → REJECT EVERYTHING except signals with side="sell" that close existing longs
   • drawdown_pct > 20%  → REJECT ALL. Emit portfolio_notes: "HALT — max drawdown hit"

4. CORRELATION VETO: If open_positions already has BTC, ETH, AND SOL all as "buy" → reject any
   additional buy for correlated assets. Do not pile into correlated longs.

5. NO DOUBLING UP: If a symbol already appears in open_position_symbols → REJECT that signal.
   We never add to an existing position without a dedicated scale-in strategy.

6. MINIMUM CONFIDENCE: After synthesis, minimum composite confidence to approve = 0.65.
   For leverage > 5x, minimum = 0.80.

7. FEAR SIGNAL OVERRIDE: If Perplexity returns fear_greed_signal = "extreme_fear" →
   This is a potential contrarian BUY signal. Consider approving cautious buys at reduced size.
   If fear_greed_signal = "extreme_greed" → Be very cautious with new longs, reduce leverage.

══ DECISION PROCEDURE ══

For each tick with pending signals:
1. Call get_portfolio_status — check drawdown, open positions, balance
2. Call get_news_sentiment — Perplexity analyzes all signal symbols
3. Call get_technical_analysis — Gemini analyzes each symbol's charts
4. Call get_open_positions — verify no doubling up
5. Call execute_trade_decision — submit final decisions with reasons citing your agents

Every decision MUST cite which agent(s) informed it.

══ OUTPUT FORMAT for execute_trade_decision ══

{{
  "decisions": [
    {{
      "symbol": "BTC/USDT",
      "action": "approve" | "reject" | "modify",
      "side": "buy" | "sell",
      "confidence": 0.0-1.0,
      "reason": "Gemini: bullish flag + aligned trends. Perplexity: neutral news (score 0.1). Approved at 3x.",
      "modified_leverage": null or integer,
      "modified_size_pct": null or float
    }}
  ],
  "portfolio_notes": "Overall risk assessment for this tick",
  "risk_level": "low" | "medium" | "high"
}}

Be decisive. Capital preservation is not optional — it is the primary objective."""


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_news_sentiment",
        "description": (
            "Query Perplexity (News Expert) for live news, sentiment scores, fear/greed signal, "
            "and key events for one or more crypto symbols. "
            "Call this before deciding on any buy signal. A score below -0.4 is an auto-veto."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "e.g. [\"BTC/USDT\", \"ETH/USDT\"]"
                }
            },
            "required": ["symbols"]
        }
    },
    {
        "name": "get_technical_analysis",
        "description": (
            "Query Gemini (Analysis Expert) for deep technical analysis: "
            "chart patterns, trend alignment, support/resistance, stop-loss levels, "
            "risk/reward ratio, and independent signal scoring. "
            "A rating of sell/strong_sell is a veto on buys."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "e.g. BTC/USDT"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_open_positions",
        "description": (
            "Return all currently open positions with symbol, side, entry price, and strategy. "
            "Use this to detect doubling-up risk and correlated long exposure."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
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
                    "description": "Filter: hft/ai_multi/dca/grid/gomale or 'all'",
                    "default": "all"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_portfolio_status",
        "description": (
            "Get balance, daily P&L, drawdown %, open trade count, and open position detail. "
            "Always call this first to check drawdown escalation rules."
        ),
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
                    "description": "Asset base: BTC, ETH, SOL, etc."
                }
            },
            "required": []
        }
    },
    {
        "name": "execute_trade_decision",
        "description": (
            "Submit your final approve/reject/modify decisions for all pending signals. "
            "Call this LAST, after calling all relevant analysis tools. "
            "Every decision must include a reason citing the agents consulted."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "symbol":            {"type": "string"},
                            "action":            {"type": "string", "enum": ["approve", "reject", "modify"]},
                            "side":              {"type": "string", "enum": ["buy", "sell"]},
                            "confidence":        {"type": "number"},
                            "reason":            {"type": "string"},
                            "modified_leverage": {"type": ["integer", "null"]},
                            "modified_size_pct": {"type": ["number", "null"]}
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
    Orchestrator agent coordinating Perplexity + Gemini to make
    capital-preservation-first trading decisions each engine tick.
    """

    def __init__(self):
        self.enabled = _anthropic_available
        self._client: Optional[Any] = None

        # Sub-agent references (set via wire_agents)
        self._perplexity = None
        self._gemini     = None

        # State
        self.last_reasoning: str = ""
        self.last_decision: dict = {}
        self.last_run_at: Optional[str] = None
        self.total_calls:    int = 0
        self.total_approved: int = 0
        self.total_rejected: int = 0

        # Per-tick context (populated before each agentic loop)
        self._ctx_signals:    list = []
        self._ctx_market:     dict = {}   # symbol → raw OHLCV candle list (for Gemini)
        self._ctx_portfolio:  dict = {}
        self._ctx_polymarket: dict = {}

        # Per-tick agent output cache (populated lazily via tool calls)
        self._news_cache:   dict = {}
        self._gemini_cache: dict = {}

        if self.enabled:
            try:
                self._client = AsyncAnthropic()
                log.info("Claude Brain (Orchestrator) ready — claude-opus-4-6 + adaptive thinking")
            except Exception as exc:
                log.error("Claude Brain init failed: %s", exc)
                self.enabled = False

    # ── Wiring ────────────────────────────────────────────────────────────────

    def wire_agents(self, perplexity, gemini):
        """Attach sub-agents. Called once at startup by init_agents()."""
        self._perplexity = perplexity
        self._gemini     = gemini
        perp_on = getattr(perplexity, "enabled", False)
        gem_on  = getattr(gemini,     "enabled", False)
        log.info(
            "Claude Brain wired — Perplexity=%s  Gemini=%s  "
            "(capital_preservation=ALWAYS_ON)",
            perp_on, gem_on,
        )

    @property
    def _perplexity_online(self) -> bool:
        return bool(self._perplexity and getattr(self._perplexity, "enabled", False))

    @property
    def _gemini_online(self) -> bool:
        return bool(self._gemini and getattr(self._gemini, "enabled", False))

    # ── Public API ────────────────────────────────────────────────────────────

    async def analyze_and_decide(
        self,
        strategy_signals: list[dict],
        market_data: dict,       # symbol → raw OHLCV candle list
        portfolio: dict,
        polymarket: dict,
    ) -> list[dict]:
        """
        Main entry point — one call per engine tick.
        Returns list of decisions: [{symbol, action, side, confidence, reason, ...}]
        """
        if not self.enabled or not self._client:
            return self._passthrough(strategy_signals, "Brain disabled")

        if not strategy_signals:
            return []

        # Populate per-tick context
        self._ctx_signals    = strategy_signals
        self._ctx_market     = market_data          # raw OHLCV now — Gemini can use it
        self._ctx_portfolio  = portfolio
        self._ctx_polymarket = polymarket

        # Clear per-tick caches
        self._news_cache   = {}
        self._gemini_cache = {}

        self.total_calls += 1
        start = time.monotonic()

        try:
            decisions = await self._run_agentic_loop(strategy_signals)
            elapsed = time.monotonic() - start
            approved = sum(1 for d in decisions if d.get("action") == "approve")
            rejected = sum(1 for d in decisions if d.get("action") == "reject")
            log.info(
                "Claude Brain: %.1fs | %d approved | %d rejected",
                elapsed, approved, rejected,
            )
            self.last_run_at = datetime.utcnow().isoformat()
            return decisions
        except Exception as exc:
            log.error("Claude Brain error: %s", exc, exc_info=True)
            # Safety: reject all on brain failure. The engine will log + skip execution.
            return self._reject_all(strategy_signals, f"Brain error: {exc}")

    def get_status(self) -> dict:
        return {
            "enabled":                self.enabled,
            "model":                  "claude-opus-4-6",
            "thinking":               "adaptive",
            "role":                   "Orchestrator",
            "capital_preservation":   "ALWAYS ON",
            "perplexity_online":      self._perplexity_online,
            "gemini_online":          self._gemini_online,
            "last_run_at":            self.last_run_at,
            "total_calls":            self.total_calls,
            "total_approved":         self.total_approved,
            "total_rejected":         self.total_rejected,
            "last_reasoning_preview": self.last_reasoning[:500] if self.last_reasoning else "",
            "last_decision":          self.last_decision,
            "agents": {
                "perplexity": getattr(self._perplexity, "get_status", lambda: {})(),
                "gemini":     getattr(self._gemini,     "get_status", lambda: {})(),
            },
        }

    # ── Agentic loop ─────────────────────────────────────────────────────────

    async def _run_agentic_loop(self, strategy_signals: list[dict]) -> list[dict]:
        system_prompt = _build_system_prompt(
            self._perplexity_online, self._gemini_online
        )
        messages = [{"role": "user", "content": self._build_user_message(strategy_signals)}]
        final_decisions: list[dict] = []

        for _round in range(12):   # cap at 12 tool-call rounds
            async with self._client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=8192,
                thinking={"type": "adaptive"},
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                tools=TOOLS,
                messages=messages,
            ) as stream:
                response = await stream.get_final_message()

            # Capture extended thinking block
            for block in response.content:
                if block.type == "thinking":
                    self.last_reasoning = block.thinking
                    break

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                # Claude chose not to call execute_trade_decision — parse text fallback
                for block in response.content:
                    if block.type == "text":
                        final_decisions = self._extract_decisions_from_text(
                            block.text, strategy_signals
                        )
                break

            if response.stop_reason != "tool_use":
                break

            # Process tool calls
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

        # Safety net: any signal without a decision is rejected by the engine
        # (engine default is now "reject"), but also reject explicitly here.
        decided_symbols = {d.get("symbol") for d in final_decisions}
        for sig in strategy_signals:
            if sig.get("symbol") not in decided_symbols:
                final_decisions.append({
                    "symbol":     sig.get("symbol"),
                    "action":     "reject",
                    "side":       sig.get("side", "buy"),
                    "confidence": 0.0,
                    "reason":     "No AI decision returned — safety reject",
                })
                self.total_rejected += 1

        return final_decisions

    # ── Tool dispatcher ───────────────────────────────────────────────────────

    async def _dispatch_tool(self, name: str, inputs: dict) -> dict:
        try:
            if name == "get_news_sentiment":
                return await self._tool_news_sentiment(inputs)
            elif name == "get_technical_analysis":
                return await self._tool_technical_analysis(inputs)
            elif name == "get_open_positions":
                return self._tool_open_positions()
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

        uncached = [s for s in symbols if s not in self._news_cache]
        if uncached and self._perplexity_online:
            fresh = await self._perplexity.analyze_news(uncached)
            self._news_cache.update(fresh)

        if not self._perplexity_online:
            return {
                "source": "Perplexity OFFLINE",
                "warning": "No news data — apply extra caution on buys",
                "results": {
                    sym: {
                        "sentiment": "NEUTRAL", "score": 0.0,
                        "summary": "Perplexity not configured.", "confidence": 0.0,
                        "fear_greed_signal": "unknown",
                    }
                    for sym in symbols
                },
            }

        return {
            "source": "Perplexity Sonar Pro (real-time web search)",
            "capital_preservation_note": (
                "Any score < -0.4 = HARD VETO on buys. "
                "extreme_greed = reduce leverage. extreme_fear = consider contrarian buy."
            ),
            "results": {
                sym: self._news_cache.get(sym, {
                    "sentiment": "NEUTRAL", "score": 0.0,
                    "summary": "No data returned.", "confidence": 0.0,
                    "fear_greed_signal": "unknown",
                })
                for sym in symbols
            },
        }

    async def _tool_technical_analysis(self, inputs: dict) -> dict:
        symbol = inputs.get("symbol", "")
        if not symbol:
            return {"error": "symbol required"}

        if symbol not in self._gemini_cache:
            if self._gemini_online:
                # FIX 3 payoff: _ctx_market now contains raw OHLCV candle lists
                ohlcv = self._ctx_market.get(symbol, [])
                sym_signals = [s for s in self._ctx_signals if s.get("symbol") == symbol]
                result = await self._gemini.analyze_market(symbol, ohlcv, sym_signals)
                self._gemini_cache[symbol] = result
            else:
                self._gemini_cache[symbol] = {
                    "symbol":         symbol,
                    "note":           "Gemini offline — no technical analysis",
                    "overall_rating": "neutral",
                }

        if not self._gemini_online:
            return {
                "source":  "Gemini OFFLINE",
                "warning": "No chart analysis — apply extra caution and check news carefully",
                "analysis": self._gemini_cache.get(symbol, {}),
            }

        return {
            "source": "Gemini 2.5 Pro (deep technical analysis)",
            "capital_preservation_note": (
                "overall_rating=sell or strong_sell = VETO on buys. "
                "Use recommended_stop_loss for position sizing."
            ),
            "analysis": self._gemini_cache.get(symbol, {}),
        }

    def _tool_open_positions(self) -> dict:
        """Return open positions from portfolio context for correlation checking."""
        p = self._ctx_portfolio
        return {
            "open_positions":         p.get("open_positions", []),
            "open_position_symbols":  p.get("open_position_symbols", []),
            "open_positions_by_side": p.get("open_positions_by_side", {"buy": [], "sell": []}),
            "warning": (
                "REJECT any signal for a symbol already in open_position_symbols. "
                "REJECT any buy if BTC, ETH, and SOL are all already long (correlation veto)."
            ),
        }

    def _tool_strategy_signals(self, inputs: dict) -> dict:
        filt = inputs.get("strategy", "all")
        sigs = (self._ctx_signals if filt == "all"
                else [s for s in self._ctx_signals if s.get("strategy") == filt])
        return {"count": len(sigs), "signals": sigs}

    def _tool_portfolio(self) -> dict:
        p = self._ctx_portfolio
        dd = p.get("drawdown_pct", 0)
        # Compute escalation level inline so Claude sees it clearly
        if dd > 20:
            escalation = "HALT — reject ALL signals immediately"
        elif dd > 15:
            escalation = "CRITICAL — reject all except closing positions"
        elif dd > 10:
            escalation = "HIGH — max leverage 2x, reject new longs above 2x"
        elif dd > 5:
            escalation = "ELEVATED — max leverage 3x"
        else:
            escalation = "NORMAL — full rules apply"

        return {
            "balance_usdt":          p.get("balance", 0),
            "open_trades":           p.get("open_trades", 0),
            "daily_pnl_pct":         round(p.get("daily_pnl_pct", 0), 3),
            "drawdown_pct":          round(dd, 3),
            "drawdown_escalation":   escalation,
            "open_position_symbols": p.get("open_position_symbols", []),
            "open_positions_by_side": p.get("open_positions_by_side", {"buy": [], "sell": []}),
        }

    def _tool_polymarket(self, inputs: dict) -> dict:
        sym = inputs.get("symbol", "").upper().replace("/USDT", "")
        markets = self._ctx_polymarket.get(sym, self._ctx_polymarket)
        return {"symbol": sym, "markets": markets if isinstance(markets, list) else []}

    # ── Message builder ───────────────────────────────────────────────────────

    def _build_user_message(self, strategy_signals: list[dict]) -> str:
        perp_status = "ONLINE" if self._perplexity_online else "OFFLINE (no key)"
        gem_status  = "ONLINE" if self._gemini_online  else "OFFLINE (no key)"

        lines = [
            f"- {s.get('strategy','?').upper():12} | {s.get('symbol'):12} | "
            f"{s.get('side','?').upper():4} | conf={s.get('confidence',0):.2f} | "
            f"lev={s.get('leverage',1)}x | price={s.get('price',0):.4f}"
            for s in strategy_signals
        ]

        return (
            f"**{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} — "
            f"{len(strategy_signals)} pending signal(s)**\n"
            f"Agent status: Perplexity={perp_status}  Gemini={gem_status}\n\n"
            + "\n".join(lines)
            + "\n\n"
            "Required procedure:\n"
            "1. `get_portfolio_status` — check drawdown escalation level\n"
            "2. `get_open_positions`   — check for doubling-up and correlation risk\n"
            "3. `get_news_sentiment`   — Perplexity: news veto check (score < -0.4 = veto)\n"
            "4. `get_technical_analysis` — Gemini: chart veto check (sell = veto)\n"
            "5. `execute_trade_decision` — final decisions citing both agents\n\n"
            "Capital preservation is the primary objective. When in doubt, REJECT."
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _extract_decisions_from_text(
        self, text: str, original_signals: list[dict]
    ) -> list[dict]:
        """Try to parse decisions from Claude's text response; reject all on failure."""
        try:
            s, e = text.find("{"), text.rfind("}") + 1
            if s >= 0 and e > s:
                parsed = json.loads(text[s:e])
                if "decisions" in parsed:
                    return parsed["decisions"]
        except (json.JSONDecodeError, ValueError):
            pass
        # Cannot parse — reject everything for capital safety
        log.warning(
            "Claude Brain: could not parse decisions from text — "
            "REJECTING all %d signals for safety", len(original_signals)
        )
        return self._reject_all(original_signals, "Unparseable response — safety reject")

    @staticmethod
    def _reject_all(signals: list[dict], reason: str) -> list[dict]:
        """Reject every signal — used as the safe failure mode."""
        return [
            {
                "symbol":     s.get("symbol"),
                "action":     "reject",
                "side":       s.get("side", "buy"),
                "confidence": 0.0,
                "reason":     reason,
            }
            for s in signals
        ]

    @staticmethod
    def _passthrough(
        signals: list[dict], reason: str, confidence_scale: float = 1.0
    ) -> list[dict]:
        """
        Approve signals at reduced confidence.
        Used ONLY when brain is completely disabled (no Anthropic key).
        When brain is enabled but errors, use _reject_all instead.
        """
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
