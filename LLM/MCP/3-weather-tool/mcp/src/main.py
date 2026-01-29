import argparse
import logging
from datetime import datetime

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import Response

# Weather MCP Server
app = FastMCP("weather-mcp")


@app.custom_route("/", methods=["GET"])
async def index_page(request: Request) -> Response:
    name = request.query_params.get("name")
    if name:
        logging.info("WEB: Processing index_page with name")
        return Response(f"Hello {name}, current time is {str(datetime.now())}")

    logging.info("WEB: Processing index_page")
    return Response("Weather MCP Server - Use MCP tools to get weather information")


@app.tool(description="Tell a programming joke")
async def tell_joke() -> str:
    return "Why do programmers prefer dark mode? Because light attracts bugs!"


@app.tool(description="Get the index message")
async def index() -> str:
    """Get the index message"""
    logging.info("API: Processing index")
    return "Hello World from MCP!"


@app.tool(description="Greet the user with a personalized message")
async def greeting(name: str) -> str:
    """Greet the user with a personalized message"""
    logging.info("API: Processing greeting")
    return f"Hello {name}, current time is {str(datetime.now())}"


@app.tool(description="Get the current weather for a given city")
async def get_weather(cityName: str) -> str:
    """Get the current weather for a given city"""
    logging.info("API: Processing get_weather")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"http://127.0.0.1:5000/city/{cityName}?format=j1")
            if response.status_code == 200:
                data = response.json()
                # API returns a normalized WeatherResponse; also support raw wttr.in data.
                if "temperature" in data or "description" in data:
                    temp_c = float(data.get("temperature", 0))
                    desc = data.get("description", "N/A")
                    icon = data.get("icon", "")
                else:
                    current = data.get("current_condition", [{}])[0]
                    temp_c = float(current.get("temp_C", 0))
                    desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
                    icon = current.get("weatherIconUrl", [{}])[0].get("value", "")
                return f"The weather in {cityName} is {desc} with a temperature of {temp_c}°C and icon {icon}"
            return f"Unable to fetch weather for {cityName}"
    except httpx.RequestError as exc:
        logging.error("API: Weather request failed: %s", exc)
        return f"Weather API request failed for {cityName}. Is the API running on 127.0.0.1:5000?"


@app.tool(description="Get information about the MCP server")
async def get_server_info() -> str:
    """Get information about the MCP server"""
    logging.info("API: Processing get_server_info")
    return "Weather API MCP Server v0.1.0"


def main():
    """Initialize and run the MCP server"""
    parser = argparse.ArgumentParser(description="Weather MCP Server")
    parser.add_argument(
        "--transport",
        default="sse",
        choices=["sse", "stdio"],
        help="Transport protocol to use",
    )
    args = parser.parse_args()
    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
