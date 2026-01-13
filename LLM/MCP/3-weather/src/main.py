import argparse
import logging
import ssl
from datetime import datetime

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import Response

# app = FastMCP("hello-world", host="127.0.0.1", port=8000)
app = FastMCP("weather")


@app.custom_route("/", methods=["GET"])
async def indexPage(request: Request) -> Response:
    name = request.query_params.get("name")
    if name:
        logging.info("WEB: Processing indexPage with name")
        return Response(f"Hello {name}, current time is {str(datetime.now())}")

    logging.info("WEB: Processing indexPage")
    return Response("Weather tool from MCP!")


@app.tool()
async def index() -> str:
    """Index page"""
    logging.info("API: Processing index")
    # Make HTTP request to get current time from external service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Using worldtimeapi.org as a simple HTTP request example
            response = await client.get("http://worldtimeapi.org/api/timezone/UTC")
            if response.status_code == 200:
                data = response.json()
                current_time = data.get("datetime", str(datetime.now()))
                return f"Weather tool from MCP! Current UTC time from API: {current_time}"
            return "Weather tool from MCP!"
    except Exception as e:
        logging.warning("HTTP request failed: %s", e)
        return "Weather tool from MCP!"


@app.tool()
async def greeting(name: str) -> str:
    """Greet the user"""
    logging.info("API: Processing greeting")
    # Make HTTP request to get current time
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://worldtimeapi.org/api/timezone/UTC")
            if response.status_code == 200:
                data = response.json()
                current_time = data.get("datetime", str(datetime.now()))
                return f"Hello {name}, current UTC time from API: {current_time}"
            return f"Hello {name}, current time is {str(datetime.now())}"
    except Exception as e:
        logging.warning("HTTP request failed: %s", e)
        return f"Hello {name}, current time is {str(datetime.now())}"


@app.tool()
async def weather(city: str = "London") -> str:
    """Get weather information for a city using HTTP request"""
    logging.info("API: Processing weather request for %s", city)
    try:
        # Disable SSL verification for wttr.in to avoid certificate issues
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            # Using wttr.in as a free weather API
            url = f"https://wttr.in/{city}?format=j1"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_condition", [{}])[0]
                temp_c = current.get("temp_C", "N/A")
                desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
                return f"Weather in {city}: {temp_c}°C, {desc}"
            return f"Unable to fetch weather for {city}"
    except ssl.SSLError as e:
        logging.error("Weather SSL error: %s", e)
        return f"SSL error fetching weather for {city}: {str(e)}"
    except Exception as e:
        logging.error("Weather HTTP request failed: %s", e)
        return f"Error fetching weather for {city}: {str(e)}"


def main():
    """Initialize and run the server"""
    parser = argparse.ArgumentParser(description="Weather tool MCP Server")
    parser.add_argument("--transport", default="sse", choices=["sse", "stdio"], help="Transport protocol to use")
    args = parser.parse_args()
    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
