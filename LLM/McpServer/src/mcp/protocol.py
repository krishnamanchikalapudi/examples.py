"""MCP Protocol implementation - core message handling."""

import asyncio
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, Field

from src.config.logger import logger


class MCPMessage(BaseModel):
    """Base MCP message model."""

    jsonrpc: str = Field(default="2.0")
    id: Optional[str] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class MCPRequest(BaseModel):
    """MCP request model."""

    jsonrpc: str = Field(default="2.0")
    id: str
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""

    jsonrpc: str = Field(default="2.0")
    id: str
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class MCPError(BaseModel):
    """MCP error model."""

    code: int
    message: str
    data: Optional[Any] = None


class MCPProtocolHandler:
    """Handler for MCP protocol messages."""

    def __init__(self):
        """Initialize protocol handler."""
        self.handlers: Dict[str, Callable[..., Any]] = {}

    def register_handler(self, method: str, handler: Callable[..., Any]):
        """Register handler for MCP method."""
        self.handlers[method] = handler
        logger.info(f"Registered handler for MCP method: {method}")

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle MCP request."""
        method = request.method
        handler = self.handlers.get(method)

        if not handler:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            )

        try:
            params = request.params or {}
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**params)
            else:
                result = handler(**params)

            return MCPResponse(id=request.id, result=result)

        except Exception as e:
            logger.error(f"Error handling MCP request {method}: {str(e)}", exc_info=True)
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            )

    def parse_message(self, data: Dict[str, Any]) -> Optional[MCPRequest]:
        """Parse incoming message."""
        try:
            if "method" in data and "id" in data:
                return MCPRequest(**data)
            return None
        except Exception as e:
            logger.error(f"Failed to parse MCP message: {str(e)}")
            return None

