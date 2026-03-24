"""
AI Agent Cluster for the Trading Bot.

Agents:
  - Perplexity  → News & Sentiment Expert (real-time web search)
  - Gemini      → Technical Analysis Expert (pattern recognition)
  - Claude      → Orchestrator & Final Decision Maker

Call `init_agents(settings)` once at application startup.
"""
from backend.brain.claude_brain import claude_brain
from backend.brain.perplexity_agent import init_perplexity
from backend.brain.gemini_agent import init_gemini


def init_agents(settings) -> None:
    """
    Initialise all agents with API keys from settings and wire them to Claude Brain.
    Call this once during FastAPI startup.
    """
    perp = init_perplexity(settings.PERPLEXITY_API_KEY or "")
    gem  = init_gemini(settings.GEMINI_API_KEY or "")
    claude_brain.wire_agents(perplexity=perp, gemini=gem)


__all__ = ["claude_brain", "init_agents"]
