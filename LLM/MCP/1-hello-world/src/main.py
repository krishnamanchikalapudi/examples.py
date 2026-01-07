from mcp.server.fastmcp import FastMCP
from datetime import datetime, date
from starlette.requests import Request
from starlette.responses import Response
import logging

#app = FastMCP("hello-world", host="127.0.0.1", port=8000)
app = FastMCP("hello-world")

@app.custom_route("/", methods=["GET"])
async def indexPage(request: Request) -> Response:
    name = request.query_params.get("name")
    if name:
        logging.info("WEB: Processing indexPage with name")
        return Response(f"Hello {name}, current time is {str(datetime.now())}")
    
    logging.info("WEB: Processing indexPage")
    return Response("Hello World from MCP!")


@app.tool()
async def index() -> str:
    """ Index page """
    logging.info("API: Processing index")
    return "Hello World from MCP!"

@app.tool()
async def greeting(name: str) -> str:
    """ Greet the user """
    logging.info("API: Processing greeting")
    return f"Hello {name}, current time is {str(datetime.now())}"


import argparse
def main():
    """ Initialize and run the server """
    parser = argparse.ArgumentParser(description="Hello World MCP Server")
    parser.add_argument("--transport", default="sse", choices=["sse", "stdio"], help="Transport protocol to use")
    args = parser.parse_args()
    app.run(transport=args.transport)
    # app.run()

if __name__ == "__main__":
    main()
