"""Tests for WebSocket service."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from app.services.websocket_service import WebSocketService
from app.managers.websocket_server import WebSocketServer


class TestWebSocketService:
    """Test cases for WebSocketService."""

    def test_singleton_pattern(self):
        """Test that WebSocketService follows singleton pattern."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        # Create first instance
        service1 = WebSocketService()
        service2 = WebSocketService()
        service3 = WebSocketService.get_instance()
        
        # All should be the same instance
        assert service1 is service2
        assert service1 is service3
        assert service2 is service3

    def test_initialization(self):
        """Test WebSocket service initialization."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        service = WebSocketService()
        
        # Should not be initialized initially
        assert not service.is_initialized()
        assert service.get_server() is None

    def test_server_initialization(self):
        """Test WebSocket server initialization."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        service = WebSocketService()
        
        # Initialize server
        server = service.initialize_server(host="localhost", port=8765)
        
        # Should be initialized now
        assert service.is_initialized()
        assert service.get_server() is not None
        assert isinstance(server, WebSocketServer)
        assert server.host == "localhost"
        assert server.port == 8765

    def test_double_initialization_error(self):
        """Test that double initialization raises error."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        service = WebSocketService()
        
        # Initialize once
        service.initialize_server()
        
        # Second initialization should raise error
        with pytest.raises(RuntimeError, match="WebSocket server is already initialized"):
            service.initialize_server()

    @pytest.mark.asyncio
    async def test_server_operations_without_initialization(self):
        """Test that operations fail when server is not initialized."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        service = WebSocketService()
        
        # All operations should fail
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            await service.start_server()
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            await service.stop_server()
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            await service.broadcast_message({"test": "message"})
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            await service.send_to_client("client_id", {"test": "message"})
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            service.get_client_count()
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            service.get_client_info()
            
        with pytest.raises(RuntimeError, match="WebSocket server not initialized"):
            await service.health_check()

    @pytest.mark.asyncio
    async def test_server_operations_with_mock(self):
        """Test server operations with mocked WebSocket server."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        service = WebSocketService()
        
        # Create mock server
        mock_server = MagicMock()
        mock_server.start = AsyncMock()
        mock_server.stop = AsyncMock()
        mock_server.broadcast_to_all = AsyncMock()
        mock_server.send_to_client = AsyncMock()
        mock_server.get_client_count.return_value = 5
        mock_server.get_client_info.return_value = [{"id": "1"}, {"id": "2"}]
        mock_server.health_check = AsyncMock(return_value={"status": "healthy"})
        
        # Set the mock server
        service._websocket_server = mock_server
        
        # Test operations
        await service.start_server()
        mock_server.start.assert_called_once()
        
        await service.stop_server()
        mock_server.stop.assert_called_once()
        
        test_message = {"type": "test", "message": "hello"}
        await service.broadcast_message(test_message)
        mock_server.broadcast_to_all.assert_called_once_with(test_message)
        
        await service.send_to_client("client_id", test_message)
        mock_server.send_to_client.assert_called_once_with("client_id", test_message)
        
        assert service.get_client_count() == 5
        assert service.get_client_info() == [{"id": "1"}, {"id": "2"}]
        
        health_result = await service.health_check()
        assert health_result == {"status": "healthy"}

    def test_access_from_different_modules(self):
        """Test that WebSocket service can be accessed from different modules."""
        # Clear any existing instance
        WebSocketService._instance = None
        WebSocketService._is_initialized = False
        
        # Simulate access from different modules
        service1 = WebSocketService.get_instance()
        service1.initialize_server()
        
        # Simulate access from another module
        service2 = WebSocketService.get_instance()
        
        # Should be the same instance and initialized
        assert service1 is service2
        assert service2.is_initialized()
        assert service2.get_server() is not None
