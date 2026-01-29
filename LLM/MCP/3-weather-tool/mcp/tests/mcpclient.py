import asyncio
import os
import sys
from contextlib import AsyncExitStack
from typing import Any, List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def connect_to_server(self, server_script_path: str):
    """Connect to an MCP server"""
    if not server_script_path.endswith(".py"):
        raise ValueError("Server script must be a Python file with .py extension")

    print(f"Starting the MCP server: {server_script_path}...")

    # Use environment variables for server process
    env = os.environ.copy()

    # Start the server as a subprocess
    server_params = StdioServerParameters(
        command="python3", args=[server_script_path], env=env
    )

    stdio_transport = await self.exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    self.stdio, self.write = stdio_transport
    self.session = await self.exit_stack.enter_async_context(
        ClientSession(self.stdio, self.write)
    )

    # Initialize the session
    await self.session.initialize()

    # List available tools
    response = await self.session.list_tools()
    print("\nConnected to server with tools:", [tool.name for tool in response.tools])
    return response.tools


async def cleanup(self):
    """Clean up resources"""
    await self.exit_stack.aclose()
    print("\nShutting down and cleaning up resources...")



# Main function
async def main():
    try:
        server_script_path = "src/main.py"
        exit_stack = AsyncExitStack()
        # Connect to the MCP server and get available tools
        available_tools = await connect_to_server(exit_stack, server_script_path)
        print("\nAvailable tools:", [tool.name for tool in available_tools])
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up resources
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
