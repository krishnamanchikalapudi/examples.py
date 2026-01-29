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
    printf "\n Starting Weather MCP Application ... "
    printf "\n ----------------------------------------------------------------  \n "
    uv run src/main.py --transport sse & 
    sleep 5
    curl -N http://127.0.0.1:8000/sse & 
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping Weather MCP Application ... "
    printf "\n ----------------------------------------------------------------  \n "

    kill_port(){
        local port=$1
        local pids
        pids=$(lsof -ti tcp:${port} 2>/dev/null)
        if [ -n "$pids" ]; then
            echo "Killing processes on port ${port}: $pids"
            kill -9 $(echo "$pids" | tr '\n' ' ') 2>/dev/null || true
        fi
    }

    kill_port 8000
    kill_port 6274
    kill_port 6277
    kill_port 5173
}
test-web(){
    printf "\n\n ---- WEB: Index Page ---- \n"
    curl http://127.0.0.1:8000

    sleep 2
    printf "\n\n ---- WEB: Index Page with Parameter ---- \n"
    curl http://127.0.0.1:8000?name=Krishna

}
test-apis(){
    export session_id="d8146709f22349c6a35349999ce944a7"

    printf "\n\n ---- API: method: initialize ---- \n"
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


    printf "\n\n ---- API: method: tools/list - get_weather: San Francisco ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": { "name": "get_weather", "arguments": { "cityName": "San Francisco" } } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - get_weather: New York ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": { "name": "get_weather", "arguments": { "cityName": "New York" } } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - get_weather: London ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": { "name": "get_weather", "arguments": { "cityName": "London" } } }'
}

if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"

    case $arg in
        START)
            stop
            prereq
            sleep 2
            start
            ;;
        TEST)
            test-web
            sleep 2
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