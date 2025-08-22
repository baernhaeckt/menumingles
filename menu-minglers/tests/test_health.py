"""Tests for health endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data
    assert "environment" in data
    assert "details" in data


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_ping_endpoint():
    """Test the ping endpoint."""
    response = client.get("/ping")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "pong"
