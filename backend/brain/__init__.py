"""
AI Agent Cluster — unified initialisation and health reporting.

Agents:
  Claude (Opus 4.6)        → Orchestrator & Final Decision Maker
  Perplexity (Sonar Pro)   → News & Sentiment Expert
  Gemini (2.5 Pro / Flash) → Technical Analysis Expert

Usage:
    from backend.brain import init_agents
    init_agents(settings)   # call once at FastAPI startup
"""
import logging

from backend.brain.claude_brain import claude_brain
from backend.brain.perplexity_agent import init_perplexity
from backend.brain.gemini_agent import init_gemini

log = logging.getLogger(__name__)


def init_agents(settings) -> None:
    """
    Initialise all three agents with their API keys, wire Perplexity + Gemini
    into Claude Brain, then print a clear startup health table.
    """
    perp = init_perplexity(settings.PERPLEXITY_API_KEY or "")
    gem  = init_gemini(settings.GEMINI_API_KEY or "")
    claude_brain.wire_agents(perplexity=perp, gemini=gem)
    _log_health_table(settings, perp, gem)


def _log_health_table(settings, perp, gem) -> None:
    """Log a human-readable agent status table at startup."""
    claude_on = bool(settings.ANTHROPIC_API_KEY)
    perp_on   = getattr(perp, "enabled", False)
    gem_on    = getattr(gem,  "enabled", False)

    perp_model = getattr(perp, "api_key",   "")
    gem_model  = getattr(gem,  "model_name", "—")

    def row(name, online, model):
        icon  = "✓ Online " if online else "✗ OFFLINE"
        key_hint = "key set" if online else "add to .env"
        return f"║  {name:<16} ║  {icon}  ║  {model:<26} ║  {key_hint:<12} ║"

    border = "╠══════════════════╬═════════════╬════════════════════════════╬══════════════╣"
    top    = "╔══════════════════╦═════════════╦════════════════════════════╦══════════════╗"
    title  = "║  AI Agent Cluster Startup Status                                           ║"
    head   = "║  Agent           ║  Status     ║  Model                     ║  API Key     ║"
    bot    = "╚══════════════════╩═════════════╩════════════════════════════╩══════════════╝"

    lines = [
        top,
        title,
        border,
        head,
        border,
        row("Claude",     claude_on, "claude-opus-4-6 (adaptive)"),
        border,
        row("Perplexity", perp_on,   "sonar-pro"),
        border,
        row("Gemini",     gem_on,    gem_model if gem_on else "—"),
        bot,
    ]

    for line in lines:
        log.info(line)

    # Warn clearly about degraded modes
    if not claude_on:
        log.warning(
            "CRITICAL: ANTHROPIC_API_KEY not set — Claude Brain DISABLED. "
            "All strategy signals will execute WITHOUT AI oversight. "
            "Add ANTHROPIC_API_KEY to .env immediately."
        )
    if not perp_on:
        log.warning(
            "Perplexity offline — trading without live news/sentiment. "
            "Claude will apply extra caution. Add PERPLEXITY_API_KEY to .env."
        )
    if not gem_on:
        log.warning(
            "Gemini offline — trading without technical chart analysis. "
            "Claude will apply extra caution. Add GEMINI_API_KEY to .env."
        )
    if claude_on and perp_on and gem_on:
        log.info(
            "All 3 AI agents ONLINE — Triple consensus capital preservation mode active."
        )


__all__ = ["claude_brain", "init_agents"]
