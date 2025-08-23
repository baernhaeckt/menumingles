"""WebSocket endpoints for real-time communication."""

import json
import logging
import time
from typing import Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse

from app.models.chat_message_model import ChatMessage
from app.services.websocket_service import WebSocketService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_websocket_service() -> WebSocketService:
    return WebSocketService.get_instance()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for client connections."""
    ws_service = get_websocket_service()
    await ws_service.connect(websocket)

    try:
        # Welcome
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "Welcome to Menu Minglers WebSocket server!"
        })

        while True:
            data = await websocket.receive_text()
            # Try JSON first; fallback to plain text
            try:
                message_data: Dict[str, Any] = json.loads(data)
                msg_type = message_data.get("type", "message")
                logger.info("Received %s from WebSocket client", msg_type)

                if msg_type == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg_type == "echo":
                    await websocket.send_json({
                        "type": "echo",
                        "original": message_data,
                        "timestamp": time.time()
                    })
                elif msg_type == "broadcast":
                    await ws_service.broadcast_message({
                        "type": "broadcast",
                        "message": message_data.get("message", ""),
                        "timestamp": time.time()
                    })
                else:
                    await websocket.send_json({
                        "type": "echo",
                        "message": message_data,
                        "timestamp": time.time()
                    })

            except json.JSONDecodeError:
                logger.info("Received plain text: %s", data)
                await websocket.send_json({
                    "type": "echo",
                    "message": data,
                    "timestamp": time.time()
                })
            except Exception as e:
                logger.exception("Error processing message")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Failed to process message: {e.__class__.__name__}"
                })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception:
        logger.exception("WebSocket error")
    finally:
        ws_service.disconnect(websocket)


@router.get("/ws/status")
async def websocket_status():
    """Return simple WebSocket service status."""
    ws_service = get_websocket_service()
    clients = ws_service.get_client_info()
    return JSONResponse(content={
        "status": "ok",
        "clientCount": len(clients),
        "clients": clients
    })


@router.post("/ws/broadcast")
async def broadcast_message(message: ChatMessage):
    """Broadcast a message to all WebSocket clients."""
    ws_service = get_websocket_service()
    try:
        payload = message.model_dump()  # pydantic v2
        await ws_service.broadcast_message({
            "type": "chat",
            "message": payload,
            "timestamp": time.time()
        })
        return JSONResponse(content={
            "status": "success",
            "message": "Message broadcast successfully"
        })
    except Exception:
        logger.exception("Error broadcasting message")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error",
                     "message": "Failed to broadcast message"}
        )


@router.get("/ws/clients")
async def get_websocket_clients():
    """List connected clients."""
    ws_service = get_websocket_service()
    clients = ws_service.get_client_info()
    return JSONResponse(content={"clients": clients, "total": len(clients)})
