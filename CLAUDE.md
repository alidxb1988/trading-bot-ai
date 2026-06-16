# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
cp .env.example .env                        # Fill in API keys before running
pip install -r backend/requirements.txt

# Run locally
python -m backend.main
# or with hot-reload:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Docker
docker-compose up --build
./start.sh                                   # Helper start script
```

No test framework is configured. Backtesting runs via `backend/backtesting/`.

## Architecture

### Startup Sequence (`backend/main.py`)

FastAPI app with a `lifespan` context that runs in order on startup:
1. `init_db()` — creates SQLite tables (aiosqlite, SQLAlchemy async)
2. `init_agents(settings)` — instantiates Claude, Perplexity, and Gemini agent objects
3. `exchange_manager.connect_from_config()` — auto-connects any exchange whose API keys are present in `.env`

The frontend is a single HTML file (`complete-trading-bot` in the repo root, wrapped in markdown code fences for version control). FastAPI strips the fences and serves it at `GET /`.

**Critical**: `TRADING_MODE=paper` by default. Change to `live` in `.env` only when real exchange keys are confirmed and risk limits have been reviewed.

### Configuration (`backend/config.py`)

Single `settings` singleton via pydantic-settings, reads from `.env`. Controls everything: exchange selection, strategy toggles (`ENABLE_HFT`, `ENABLE_AI_MULTI`, `ENABLE_ZERO_LOSS`, `ENABLE_GRID`, `ENABLE_GOMALE`), capital allocations, risk limits, and AI API keys.

### 3-Agent AI Brain (`backend/brain/`)

Trading signals pass through a sequential consultation pipeline before any order is placed:

1. **`perplexity_agent.py`** — fetches live news & market sentiment (Perplexity API)
2. **`gemini_agent.py`** — runs technical analysis on price/indicator data (Gemini API)
3. **`claude_brain.py`** — Orchestrator: receives outputs from both agents, applies risk rules, and emits the final `BUY / SELL / HOLD` decision. Gated by `CLAUDE_BRAIN_CONFIDENCE_THRESHOLD` (default `0.65`) and `CLAUDE_BRAIN_MAX_POSITIONS`.

### Strategies (`backend/strategies/`)

All strategies extend `BaseStrategy` in `base.py`. Each manages its own capital slice and runs independently:

| Strategy | File | Timeframe | Default Capital |
|----------|------|-----------|------------------|
| HFT Scalping | `hft_scalping.py` | 3m | 40% |
| AI Multi | `ai_multi.py` | 15m | 35% |
| Zero-Loss DCA | `zero_loss_dca.py` | 1h | 25% |
| Gomale | `gomale.py` | 15m | 25% |
| Grid | `grid.py` | — | 20% (disabled by default) |

Capital percentages are set in `.env`. When adding a new strategy: extend `BaseStrategy`, add an `ENABLE_<NAME>` toggle to `config.py`, and document it in `.env.example`.

### Exchange Layer (`backend/exchange/`)

CCXT-based `exchange_manager` supporting Bybit, Binance, KuCoin, and OKX. `ACTIVE_EXCHANGE` in `.env` selects which one is used. Paper mode simulates fills against `PAPER_BALANCE` with no real exchange calls.

### API (`backend/api/`)

- `routes.py` — REST endpoints for bot control, trade history, portfolio state
- `websocket.py` — WebSocket push for real-time P&L, signals, and trade events to the frontend

### Risk Circuit Breakers

Enforced globally across all strategies via `backend/config.py`:
- `MAX_DRAWDOWN_PCT=0.20` — halt all trading if portfolio drops 20%
- `MAX_DAILY_LOSS_PCT=0.05` — halt if daily loss exceeds 5%
- `MAX_POSITION_SIZE_PCT=0.10` — no single position exceeds 10% of portfolio

## Claude Code Skills

See `.claude/SKILLS.md` for the full skill catalog. Relevant to this repo:
- `claude-trading-skills` — market analysis, backtesting, sector screening
- `customs-trade-compliance` — if extending the bot for commodity/FX trading
- `claude-mem-memory` — persistent memory for multi-session development work
