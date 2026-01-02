"""Integration tests for FastAPI server."""

import pytest
from fastapi.testclient import TestClient

from src.server import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "status" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_mcp_endpoint_invalid_request():
    """Test MCP endpoint with invalid request."""
    response = client.post("/mcp", json={"invalid": "data"})
    assert response.status_code == 400


def test_mcp_endpoint_valid_request():
    """Test MCP endpoint with valid request."""
    request_data = {
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": "initialize",
        "params": {},
    }
    response = client.post("/mcp", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "jsonrpc" in data
    assert "id" in data
    assert "result" in data or "error" in data

