"""WebSocket server manager for handling real-time connections."""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Set
from uuid import uuid4

import websockets
from websockets.server import WebSocketServerProtocol

logger = logging.getLogger(__name__)


class WebSocketServer:
    """WebSocket server for handling real-time connections and messages."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        """Initialize the WebSocket server.

        Args:
            host: Host address to bind the server to
            port: Port number to bind the server to
        """
        self.host = host
        self.port = port
        self.clients: Dict[str, WebSocketServerProtocol] = {}
        self.client_info: Dict[str, Dict] = {}
        self.server: Optional[websockets.WebSocketServer] = None
        self.is_running = False

    async def start(self):
        """Start the WebSocket server."""
        if self.is_running:
            logger.warning("WebSocket server is already running")
            return

        try:
            self.server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port
            )
            self.is_running = True
            logger.info(
                f"WebSocket server started on ws://{self.host}:{self.port}")

            # Keep the server running
            await self.server.wait_closed()
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise

    async def stop(self):
        """Stop the WebSocket server."""
        if not self.is_running:
            logger.warning("WebSocket server is not running")
            return

        try:
            # Close all client connections
            for client_id in list(self.clients.keys()):
                await self.disconnect_client(client_id)

            # Stop the server
            if self.server:
                self.server.close()
                await self.server.wait_closed()

            self.is_running = False
            logger.info("WebSocket server stopped")
        except Exception as e:
            logger.error(f"Error stopping WebSocket server: {e}")
            raise

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new client connection.

        Args:
            websocket: The WebSocket connection
            path: The request path
        """
        client_id = str(uuid4())

        try:
            # Store client connection
            self.clients[client_id] = websocket
            self.client_info[client_id] = {
                "id": client_id,
                "connected_at": asyncio.get_event_loop().time(),
                "path": path
            }

            logger.info(
                f"Client {client_id} connected from {websocket.remote_address}")

            # Send welcome message
            await self.send_to_client(client_id, {
                "type": "connection",
                "status": "connected",
                "client_id": client_id,
                "message": "Welcome to Menu Minglers WebSocket server!"
            })

            # Broadcast client joined
            await self.broadcast_to_others(client_id, {
                "type": "client_joined",
                "client_id": client_id,
                "total_clients": len(self.clients)
            })

            # Handle incoming messages
            async for message in websocket:
                await self.handle_message(client_id, message)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            await self.disconnect_client(client_id)

    async def handle_message(self, client_id: str, message: str):
        """Handle incoming message from a client.

        Args:
            client_id: The ID of the client sending the message
            message: The message content
        """
        try:
            # Try to parse as JSON
            data = json.loads(message)
            message_type = data.get("type", "message")

            logger.info(f"Received {message_type} from client {client_id}")

            # Handle different message types
            if message_type == "ping":
                await self.send_to_client(client_id, {"type": "pong"})
            elif message_type == "broadcast":
                # Broadcast message to all other clients
                await self.broadcast_to_others(client_id, {
                    "type": "broadcast",
                    "from": client_id,
                    "message": data.get("message", ""),
                    "timestamp": asyncio.get_event_loop().time()
                })
            elif message_type == "private":
                # Send private message to specific client
                target_id = data.get("to")
                if target_id and target_id in self.clients:
                    await self.send_to_client(target_id, {
                        "type": "private",
                        "from": client_id,
                        "message": data.get("message", ""),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                else:
                    await self.send_to_client(client_id, {
                        "type": "error",
                        "message": f"Target client {target_id} not found"
                    })
            else:
                # Echo back the message
                await self.send_to_client(client_id, {
                    "type": "echo",
                    "original": data,
                    "timestamp": asyncio.get_event_loop().time()
                })

        except json.JSONDecodeError:
            # Handle plain text messages
            logger.info(
                f"Received plain text from client {client_id}: {message}")
            await self.send_to_client(client_id, {
                "type": "echo",
                "message": message,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(
                f"Error handling message from client {client_id}: {e}")
            await self.send_to_client(client_id, {
                "type": "error",
                "message": "Failed to process message"
            })

    async def send_to_client(self, client_id: str, data: dict):
        """Send a message to a specific client.

        Args:
            client_id: The ID of the client to send to
            data: The data to send (will be JSON serialized)
        """
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found")
            return

        try:
            message = json.dumps(data)
            await self.clients[client_id].send(message)
        except Exception as e:
            logger.error(f"Error sending message to client {client_id}: {e}")
            await self.disconnect_client(client_id)

    async def broadcast_to_all(self, data: dict):
        """Broadcast a message to all connected clients.

        Args:
            data: The data to broadcast (will be JSON serialized)
        """
        logger.info(f"Broadcasting to all clients: {data}")
        if not self.clients:
            return

        message = json.dumps(data)
        disconnected_clients = []

        for client_id, websocket in self.clients.items():
            try:
                logger.info(f"Broadcasting to client {client_id}: {message}")
                await websocket.send(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {e}")
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect_client(client_id)

    async def broadcast_to_others(self, exclude_client_id: str, data: dict):
        """Broadcast a message to all clients except the specified one.

        Args:
            exclude_client_id: The ID of the client to exclude
            data: The data to broadcast (will be JSON serialized)
        """
        message = json.dumps(data)
        disconnected_clients = []

        for client_id, websocket in self.clients.items():
            if client_id != exclude_client_id:
                try:
                    await websocket.send(message)
                except Exception as e:
                    logger.error(
                        f"Error broadcasting to client {client_id}: {e}")
                    disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect_client(client_id)

    async def disconnect_client(self, client_id: str):
        """Disconnect a client and clean up resources.

        Args:
            client_id: The ID of the client to disconnect
        """
        if client_id in self.clients:
            try:
                await self.clients[client_id].close()
            except Exception as e:
                logger.error(
                    f"Error closing connection for client {client_id}: {e}")

            # Remove from tracking
            del self.clients[client_id]
            if client_id in self.client_info:
                del self.client_info[client_id]

            # Broadcast client left
            await self.broadcast_to_all({
                "type": "client_left",
                "client_id": client_id,
                "total_clients": len(self.clients)
            })

            logger.info(
                f"Client {client_id} disconnected. Total clients: {len(self.clients)}")

    def get_client_count(self) -> int:
        """Get the number of connected clients.

        Returns:
            Number of connected clients
        """
        return len(self.clients)

    def get_client_info(self) -> List[Dict]:
        """Get information about all connected clients.

        Returns:
            List of client information dictionaries
        """
        return list(self.client_info.values())

    async def health_check(self) -> Dict:
        """Get health status of the WebSocket server.

        Returns:
            Health status dictionary
        """
        return {
            "status": "healthy" if self.is_running else "stopped",
            "host": self.host,
            "port": self.port,
            "client_count": len(self.clients),
            "clients": self.get_client_info()
        }
