"""MCP protocol method handlers."""

from typing import Any, Dict, List

from src.config.cache import cache_service
from src.config.circuit_breaker import get_circuit_breaker
from src.config.logger import logger
from src.util.retry import retry_with_backoff


class MCPHandlers:
    """MCP method handlers implementation."""

    @staticmethod
    async def initialize(params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize MCP connection."""
        logger.info("MCP connection initialized", extra={"params": params})
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "mcp-server",
                "version": "1.0.0",
            },
            "capabilities": {
                "tools": {},
                "resources": {},
            },
        }

    @staticmethod
    async def tools_list(params: Dict[str, Any] = None) -> Dict[str, Any]:
        """List available tools."""
        logger.info("Listing available tools")
        return {
            "tools": [
                {
                    "name": "echo",
                    "description": "Echo a message back",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo",
                            }
                        },
                        "required": ["message"],
                    },
                }
            ]
        }

    @staticmethod
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    async def tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        logger.info(f"Calling tool: {tool_name}", extra={"arguments": arguments})

        # Use circuit breaker for external calls
        circuit_breaker = get_circuit_breaker(f"tool_{tool_name}")

        def execute_tool():
            if tool_name == "echo":
                message = arguments.get("message", "")
                return {"content": [{"type": "text", "text": f"Echo: {message}"}]}
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            result = circuit_breaker.call(execute_tool)
            return {"content": result.get("content", [])}
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            raise

    @staticmethod
    async def resources_list(params: Dict[str, Any] = None) -> Dict[str, Any]:
        """List available resources."""
        logger.info("Listing available resources")
        return {"resources": []}

    @staticmethod
    async def resources_read(params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a resource."""
        resource_uri = params.get("uri")
        logger.info(f"Reading resource: {resource_uri}")

        # Check cache first
        cache_key = f"resource:{resource_uri}"
        cached = cache_service.get(cache_key)
        if cached:
            logger.info(f"Resource cache hit: {resource_uri}")
            return {"contents": [{"uri": resource_uri, "mimeType": "text/plain", "text": cached}]}

        # In production, fetch from actual resource store
        result = {"contents": [{"uri": resource_uri, "mimeType": "text/plain", "text": ""}]}

        # Cache the result
        cache_service.set(cache_key, result["contents"][0]["text"])

        return result

    @staticmethod
    async def prompts_list(params: Dict[str, Any] = None) -> Dict[str, Any]:
        """List available prompts."""
        logger.info("Listing available prompts")
        return {"prompts": []}

    @staticmethod
    async def prompts_get(params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a prompt."""
        prompt_name = params.get("name")
        logger.info(f"Getting prompt: {prompt_name}")
        return {"description": "", "arguments": []}

