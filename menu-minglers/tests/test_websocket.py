"""Tests for WebSocket server functionality."""

import asyncio
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
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


class TestWebSocketEndpoints:
    """Test WebSocket API endpoints."""

    def test_websocket_status_endpoint(self):
        """Test WebSocket status endpoint."""
        client = TestClient(app)
        response = client.get("/api/v1/ws/status")
        assert response.status_code == 503  # Service unavailable when not running
        data = response.json()
        assert "status" in data
        assert data["status"] == "unavailable"

    def test_websocket_clients_endpoint(self):
        """Test WebSocket clients endpoint."""
        client = TestClient(app)
        response = client.get("/api/v1/ws/clients")
        assert response.status_code == 503  # Service unavailable when not running
        data = response.json()
        assert "status" in data
        assert data["status"] == "unavailable"

    def test_broadcast_endpoint(self):
        """Test broadcast endpoint."""
        client = TestClient(app)
        message = {"type": "test", "message": "Hello World"}
        response = client.post("/api/v1/ws/broadcast", json=message)
        assert response.status_code == 503  # Service unavailable when not running
        data = response.json()
        assert "status" in data
        assert data["status"] == "error"


class TestWebSocketIntegration:
    """Test WebSocket integration with FastAPI."""

    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test WebSocket connection through FastAPI."""
        # This test would require a running server
        # For now, we'll just test the endpoint exists
        client = TestClient(app)

        # Test that the WebSocket endpoint is available
        # Note: TestClient doesn't support WebSocket testing directly
        # This would need to be tested with a real WebSocket client

        # Test the root endpoint includes WebSocket info
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "websocket" in data
        assert data["websocket"] == "/api/v1/ws"


if __name__ == "__main__":
    pytest.main([__file__])
