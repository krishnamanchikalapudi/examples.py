import argparse
import logging
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import Response

# MCP Inspector Server
app = FastMCP("weather-api")


@app.custom_route("/", methods=["GET"])
async def indexPage(request: Request) -> Response:
    name = request.query_params.get("name")
    if name:
        logging.info("WEB: Processing indexPage with name")
        return Response(f"Hello {name}, current time is {str(datetime.now())}")

    logging.info("WEB: Processing indexPage")
    return Response(
        "Weather API MCP Server to interact with this server"
    )


@app.tool(description="Get the index message")
async def index() -> str:
    """Get the index message"""
    logging.info("API: Processing index")
    return "Weather API to interact with this server"


@app.tool(description="Greet the user with a personalized message")
async def greeting(name: str) -> str:
    """Greet the user with a personalized message"""
    logging.info("API: Processing greeting")
    return f"Hello {name}, current time is {str(datetime.now())}"


@app.tool(description="Get information about the MCP server")
async def get_server_info() -> str:
    """Get information about the MCP server"""
    logging.info("API: Processing get_server_info")
    return "Weather API MCP Server v0.1.0"


def main():
    """Initialize and run the MCP server"""
    parser = argparse.ArgumentParser(description="Weather API MCP Server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["sse", "stdio"],
        help="Transport protocol to use (stdio is required forWeather API)",
    )
    args = parser.parse_args()
    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
