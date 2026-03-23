"""
Trading Bot AI — FastAPI Application Entry Point
"""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from backend.config import settings
from backend.database import init_db
from backend.exchange.manager import exchange_manager
from backend.api.routes import router
from backend.api.websocket import ws_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
log = logging.getLogger(__name__)


# ── App lifecycle ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("=== Trading Bot AI starting up ===")
    await init_db()

    # Auto-connect exchanges if API keys are configured in .env
    connections = await exchange_manager.connect_from_config()
    if connections:
        log.info("Exchange connections: %s", connections)
    else:
        log.info("No exchange API keys found — running in paper-trade mode")

    yield   # app is running

    log.info("=== Trading Bot AI shutting down ===")
    await exchange_manager.close_all()


# ── FastAPI app ───────────────────────────────────────────────────────────────

app = FastAPI(
    title       = "Trading Bot AI",
    description = "Live crypto trading bot with HFT, AI Multi-Strategy, Zero-Loss DCA, and Grid strategies",
    version     = "1.0.0",
    lifespan    = lifespan,
)

# CORS — allow the frontend (served on same origin or localhost dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# REST + WebSocket routes
app.include_router(router)
app.include_router(ws_router)


# ── Serve the frontend HTML ───────────────────────────────────────────────────

FRONTEND_FILE = os.path.join(os.path.dirname(__file__), "..", "complete-trading-bot")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """
    Serve the frontend HTML.
    The source file is wrapped in markdown code fences (```html / ```) for
    documentation purposes — strip them before sending to the browser.
    """
    with open(FRONTEND_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    # Drop the opening ```html fence and the closing ``` fence
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return HTMLResponse(content="".join(lines))


# ── Run directly ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host    = settings.HOST,
        port    = settings.PORT,
        reload  = settings.DEBUG,
        log_level = "debug" if settings.DEBUG else "info",
    )
