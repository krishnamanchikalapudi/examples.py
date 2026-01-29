#!/bin/bash
arg=${1:-"START"}

prereq(){
    uv lock 
    uv pip install -e ".[dev]" && uv sync 
    ruff check src/  # Lint all files in the current directory.
    ruff format src/  # Format all files in the current directory.
    uv run pytest tests/maintests.py -v
}
start(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Starting Hello World - MCP Inspector ... "
    printf "\n ----------------------------------------------------------------  \n "
    npx @modelcontextprotocol/inspector uv run src/main.py --transport stdio & 
    sleep 5
    curl -N http://127.0.0.1:8000/sse & 
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping Hello World - MCP Inspector Application ... "
    printf "\n ----------------------------------------------------------------  \n "

    # uv stop
    kill -9 $(lsof -ti tcp:8000)
    kill -9 $(lsof -ti tcp:6274)
    kill -9 $(lsof -ti tcp:6277)
    kill -9 $(lsof -ti tcp:5173)
    exit 0
}
test-apis(){
    printf "\n\n ---- API: method: initialize ---- \n"
    export session_id="11cd9b9b65e54ab4a4a1bb2f16b1dc2f"

    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{  "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": { "protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": { "name": "curl-client", "version": "1.0" }  } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - index ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": { "name": "index", "arguments": {} } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - index with param ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": { "name": "greeting", "arguments": { "name": "Krishna" } } }'
}

if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"

    case $arg in
        START)
            prereq
            sleep 2
            start
            ;;
        TEST)
            test-apis
            ;;
        STOP)
            stop
            ;;
        *)
            echo "Invalid argument: $arg"
            echo "Usage: ./mcp.sh <start | stop>"
            ;;
    esac
fi