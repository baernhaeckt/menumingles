"""WebSocket service for centralized WebSocket server management."""

import asyncio
import logging
from typing import Dict, List, Optional

from app.managers.websocket_server import WebSocketServer

logger = logging.getLogger(__name__)


class WebSocketService:
    """Centralized WebSocket service for managing WebSocket connections.
    
    This service provides a singleton pattern for accessing the WebSocket server
    from anywhere in the application, including other managers and services.
    """
    
    _instance: Optional['WebSocketService'] = None
    _websocket_server: Optional[WebSocketServer] = None
    _is_initialized: bool = False
    
    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the WebSocket service (only once due to singleton)."""
        if not self._is_initialized:
            self._websocket_server = None
            self._is_initialized = True
            logger.debug("WebSocket service initialized")
    
    @classmethod
    def get_instance(cls) -> 'WebSocketService':
        """Get the singleton instance of the WebSocket service.
        
        Returns:
            WebSocketService: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def initialize_server(self, host: str = "localhost", port: int = 8765) -> WebSocketServer:
        """Initialize the WebSocket server.
        
        Args:
            host: Host address to bind the server to
            port: Port number to bind the server to
            
        Returns:
            WebSocketServer: The initialized WebSocket server instance
            
        Raises:
            RuntimeError: If server is already initialized
        """
        if self._websocket_server is not None:
            raise RuntimeError("WebSocket server is already initialized")
        
        self._websocket_server = WebSocketServer(host=host, port=port)
        logger.info(f"WebSocket server initialized on {host}:{port}")
        return self._websocket_server
    
    def get_server(self) -> Optional[WebSocketServer]:
        """Get the WebSocket server instance.
        
        Returns:
            WebSocketServer or None: The WebSocket server instance if initialized
        """
        return self._websocket_server
    
    def is_initialized(self) -> bool:
        """Check if the WebSocket server is initialized.
        
        Returns:
            bool: True if server is initialized, False otherwise
        """
        return self._websocket_server is not None
    
    async def start_server(self) -> None:
        """Start the WebSocket server.
        
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        await self._websocket_server.start()
    
    async def stop_server(self) -> None:
        """Stop the WebSocket server.
        
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        await self._websocket_server.stop()
    
    async def broadcast_message(self, message: Dict) -> None:
        """Broadcast a message to all connected WebSocket clients.
        
        Args:
            message: The message to broadcast
            
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        await self._websocket_server.broadcast_to_all(message)
    
    async def send_to_client(self, client_id: str, message: Dict) -> None:
        """Send a message to a specific WebSocket client.
        
        Args:
            client_id: The ID of the client to send to
            message: The message to send
            
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        await self._websocket_server.send_to_client(client_id, message)
    
    def get_client_count(self) -> int:
        """Get the number of connected WebSocket clients.
        
        Returns:
            int: Number of connected clients
            
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        return self._websocket_server.get_client_count()
    
    def get_client_info(self) -> List[Dict]:
        """Get information about all connected WebSocket clients.
        
        Returns:
            List[Dict]: List of client information dictionaries
            
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        return self._websocket_server.get_client_info()
    
    async def health_check(self) -> Dict:
        """Get health status of the WebSocket server.
        
        Returns:
            Dict: Health status dictionary
            
        Raises:
            RuntimeError: If server is not initialized
        """
        if not self.is_initialized():
            raise RuntimeError("WebSocket server not initialized")
        
        return await self._websocket_server.health_check()
