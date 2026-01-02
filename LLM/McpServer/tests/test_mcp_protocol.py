"""Unit tests for MCP protocol."""

import pytest
from src.mcp.protocol import MCPProtocolHandler, MCPRequest, MCPResponse


@pytest.fixture
def protocol_handler():
    """Create protocol handler instance."""
    return MCPProtocolHandler()


@pytest.fixture
def sample_request():
    """Create sample MCP request."""
    return MCPRequest(
        id="test-1",
        method="initialize",
        params={"protocolVersion": "2024-11-05"},
    )


@pytest.mark.asyncio
async def test_register_handler(protocol_handler):
    """Test handler registration."""
    async def test_handler():
        return {"status": "ok"}

    protocol_handler.register_handler("test", test_handler)
    assert "test" in protocol_handler.handlers


@pytest.mark.asyncio
async def test_handle_request_success(protocol_handler, sample_request):
    """Test successful request handling."""
    async def initialize_handler(**kwargs):
        return {"initialized": True}

    protocol_handler.register_handler("initialize", initialize_handler)
    response = await protocol_handler.handle_request(sample_request)

    assert isinstance(response, MCPResponse)
    assert response.id == sample_request.id
    assert response.result is not None
    assert response.error is None


@pytest.mark.asyncio
async def test_handle_request_method_not_found(protocol_handler, sample_request):
    """Test handling of unknown method."""
    sample_request.method = "unknown_method"
    response = await protocol_handler.handle_request(sample_request)

    assert isinstance(response, MCPResponse)
    assert response.error is not None
    assert response.error["code"] == -32601


@pytest.mark.asyncio
async def test_handle_request_error(protocol_handler):
    """Test error handling in request."""
    async def failing_handler():
        raise ValueError("Test error")

    request = MCPRequest(id="test-2", method="failing")
    protocol_handler.register_handler("failing", failing_handler)
    response = await protocol_handler.handle_request(request)

    assert isinstance(response, MCPResponse)
    assert response.error is not None
    assert response.error["code"] == -32603


def test_parse_message_valid(protocol_handler):
    """Test parsing valid message."""
    data = {
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": "initialize",
        "params": {},
    }
    request = protocol_handler.parse_message(data)
    assert isinstance(request, MCPRequest)
    assert request.method == "initialize"


def test_parse_message_invalid(protocol_handler):
    """Test parsing invalid message."""
    data = {"invalid": "data"}
    request = protocol_handler.parse_message(data)
    assert request is None

