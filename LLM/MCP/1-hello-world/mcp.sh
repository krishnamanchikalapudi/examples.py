#!/bin/bash
arg=${1:-"START"}

prereq(){
    uv lock && uv sync && uv pip install -e ".[dev]" 
    uv pip install -e ".[dev]" && uv sync 
    ruff check src/ --fix --statistics # Lint all files in the current directory.
    ruff format src/  # Format all files in the current directory.
    uv run pytest tests/maintests.py -v
}
start(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Starting MCP: Hello World service using SSE transport ... "
    printf "\n ----------------------------------------------------------------  \n "
    uv run src/main.py & 
    sleep 5
    curl -N http://127.0.0.1:8000/sse & 
}
build(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Building Docker Image for Hello World MCP Application ... "
    printf "\n ----------------------------------------------------------------  \n "
    docker build -f ./Dockerfile -t mcp-hello-world:latest .
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping MCP: Hello World service using SSE transport ... "
    printf "\n ----------------------------------------------------------------  \n "

    # uv stop
    # kill -9 $(lsof -ti tcp:8000) &
    # Kill process on port 8000, skip if error (no process running)
    pid=$(lsof -ti tcp:8000 2>/dev/null)
    if [ -n "$pid" ]; then
        kill -9 "$pid" 2>/dev/null || true
    fi
}
test(){
    test-web
    sleep 2
    test-apis
    sleep 1
    exit 0
}
test-web(){
    printf "\n\n ---- WEB: Index Page ---- \n"
    curl http://127.0.0.1:8000

    sleep 2
    printf "\n\n ---- WEB: Index Page with Parameter ---- \n"
    curl http://127.0.0.1:8000?name=Krishna

}
test-apis(){
    export session_id="8fd47d2220274c389cd0d579b5c1a38c"
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
}

if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"

    case $arg in
        START)
            stop
            sleep 2
            prereq
            sleep 2
            start
            ;;
        TEST)
            test
            ;;
        BUILD)
            build
            ;;
        STOP)
            stop
            exit 0
            ;;
        *)
            echo "Invalid argument: $arg"
            echo "Usage: ./mcp.sh <start | stop>"
            ;;
    esac
fi