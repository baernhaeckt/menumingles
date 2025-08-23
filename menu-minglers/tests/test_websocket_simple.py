"""Simple WebSocket server tests without importing the main app."""

import pytest

from app.managers.websocket_server import WebSocketServer


class TestWebSocketServer:
    """Test WebSocket server functionality."""

    def test_websocket_server_initialization(self):
        """Test WebSocket server initialization."""
        server = WebSocketServer(host="localhost", port=8765)
        assert server.host == "localhost"
        assert server.port == 8765
        assert not server.is_running
        assert len(server.clients) == 0

    def test_websocket_server_client_count(self):
        """Test client count functionality."""
        server = WebSocketServer()
        assert server.get_client_count() == 0

    def test_websocket_server_client_info(self):
        """Test client info functionality."""
        server = WebSocketServer()
        client_info = server.get_client_info()
        assert isinstance(client_info, list)
        assert len(client_info) == 0

    @pytest.mark.asyncio
    async def test_websocket_server_health_check(self):
        """Test health check functionality."""
        server = WebSocketServer()
        health = await server.health_check()
        assert "status" in health
        assert "host" in health
        assert "port" in health
        assert "client_count" in health
        assert "clients" in health
        assert health["status"] == "stopped"
        assert health["client_count"] == 0


if __name__ == "__main__":
    pytest.main([__file__])
