from mcp.server.fastmcp import FastMCP
from datetime import datetime, date
from starlette.requests import Request
from starlette.responses import Response
import logging

app = FastMCP("hello-world", host="127.0.0.1", port=8000)

@app.custom_route("/", methods=["GET"])
async def indexPage(request: Request) -> Response:
    name = request.query_params.get("name")
    if name:
        logging.info("Processing indexPage with name")
        return Response(f"Hello {name}, current time is {str(datetime.now())}")
    
    logging.info("Processing indexPage")
    return Response("Hello World from MCP!")


@app.tool()
async def index() -> str:
    """ Index page """
    logging.info("Processing index")
    return "Hello World from MCP!"

@app.tool()
async def greeting(name: str) -> str:
    """ Greet the user """
    logging.info("Processing greeting")
    return f"Hello {name}, current time is {str(datetime.now())}"


def main():
    """ Initialize and run the server """
    app.run(transport='sse')


if __name__ == "__main__":
    main()
