"""
WebSocket endpoint for real-time updates.
"""
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.trading.engine import engine

log = logging.getLogger(__name__)
ws_router = APIRouter()


@ws_router.websocket("/ws/live")
async def live_feed(websocket: WebSocket):
    """
    Client connects here to receive real-time events:
    - tick      : engine stats every ~60 s
    - new_trade : emitted when a trade is executed
    - halt      : emitted when a circuit-breaker fires
    """
    await websocket.accept()
    engine.register_ws(websocket)
    log.info("WebSocket client connected")

    try:
        # Send current status immediately on connect
        await websocket.send_text(json.dumps({
            "event": "connected",
            "data":  engine.stats,
        }))

        # Keep connection alive — engine broadcasts to us
        while True:
            # We also accept messages from the client (e.g. ping)
            try:
                data = await websocket.receive_text()
                msg  = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except Exception:
                break

    except WebSocketDisconnect:
        log.info("WebSocket client disconnected")
    finally:
        engine.unregister_ws(websocket)
