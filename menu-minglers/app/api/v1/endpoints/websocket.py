"""WebSocket endpoints for real-time communication."""

import asyncio
import json
import logging
from typing import Dict, Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse

from app.models.chat_message_model import ChatMessage
from app.services.websocket_service import WebSocketService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_websocket_service() -> WebSocketService:
    """Get the WebSocket service instance.

    Returns:
        WebSocketService: The WebSocket service instance
    """
    return WebSocketService.get_instance()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for client connections.

    Args:
        websocket: The WebSocket connection
    """
    await websocket.accept()

    # Get WebSocket service instance
    ws_service = get_websocket_service()
    if not ws_service.is_initialized():
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "WebSocket server not available"
        }))
        await websocket.close()
        return

    # Get the WebSocket server instance
    ws_server = ws_service.get_server()

    # Generate client ID
    client_id = None

    try:
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Welcome to Menu Minglers WebSocket server!"
        }))

        # Handle incoming messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                # Parse JSON message
                message_data = json.loads(data)
                message_type = message_data.get("type", "message")

                logger.info(f"Received {message_type} from WebSocket client")

                # Handle different message types
                if message_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif message_type == "echo":
                    # Echo back the message
                    await websocket.send_text(json.dumps({
                        "type": "echo",
                        "original": message_data,
                        "timestamp": asyncio.get_event_loop().time()
                    }))
                elif message_type == "broadcast":
                    # Broadcast to all other WebSocket clients
                    await ws_server.broadcast_to_all({
                        "type": "broadcast",
                        "message": message_data.get("message", ""),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                else:
                    # Default echo response
                    await websocket.send_text(json.dumps({
                        "type": "echo",
                        "message": message_data,
                        "timestamp": asyncio.get_event_loop().time()
                    }))

            except json.JSONDecodeError:
                # Handle plain text messages
                logger.info(f"Received plain text: {data}")
                await websocket.send_text(json.dumps({
                    "type": "echo",
                    "message": data,
                    "timestamp": asyncio.get_event_loop().time()
                }))
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Failed to process message"
                }))

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Clean up if needed
        pass


@router.get("/ws/status")
async def websocket_status():
    """Get WebSocket server status.

    Returns:
        JSON response with WebSocket server status
    """
    ws_service = get_websocket_service()
    if not ws_service.is_initialized():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unavailable",
                "message": "WebSocket server not initialized"
            }
        )

    status_info = await ws_service.health_check()
    return JSONResponse(content=status_info)


@router.post("/ws/broadcast")
async def broadcast_message(message: ChatMessage):
    """Broadcast a message to all WebSocket clients.

    Args:
        message: The message to broadcast

    Returns:
        JSON response with broadcast status
    """
    ws_service = get_websocket_service()
    if not ws_service.is_initialized():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "message": "WebSocket server not available"
            }
        )

    try:
        await ws_service.broadcast_message(message)
        return JSONResponse(content={
            "status": "success",
            "message": "Message broadcasted successfully"
        })
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Failed to broadcast message"
            }
        )


@router.get("/ws/clients")
async def get_websocket_clients():
    """Get information about connected WebSocket clients.

    Returns:
        JSON response with client information
    """
    ws_service = get_websocket_service()
    if not ws_service.is_initialized():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unavailable",
                "message": "WebSocket server not initialized"
            }
        )

    clients = ws_service.get_client_info()
    return JSONResponse(content={
        "clients": clients,
        "total": len(clients)
    })
