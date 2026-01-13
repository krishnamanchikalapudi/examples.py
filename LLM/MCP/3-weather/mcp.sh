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
    printf "\n Starting MCP: Weather service using HTTP transport ... "
    printf "\n ----------------------------------------------------------------  \n "
    uv run src/main.py & 
    sleep 5
    curl -N http://127.0.0.1:8000/sse & 
}
build(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Building Docker Image for Weather MCP Application using HTTP transport ... "
    printf "\n ----------------------------------------------------------------  \n "
    docker build -f ./Dockerfile -t mcp-hello-world:latest .
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping MCP: Weather service  ... "
    printf "\n ----------------------------------------------------------------  \n "

    # uv stop
    # Kill all processes on port 8000, skip if error (no process running)
    pids=$(lsof -ti tcp:8000 2>/dev/null)
    if [ -n "$pids" ]; then
        # Handle multiple PIDs - kill can accept multiple PIDs at once
        echo "Killing processes: $pids"
        # Convert newlines to spaces and kill all at once
        kill -9 $(echo "$pids" | tr '\n' ' ') 2>/dev/null || true
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
    # Check if server is running
    if ! curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
        printf "\n\n ERROR: Server is not running on http://127.0.0.1:8000\n"
        printf " Please start the server first with: ./mcp.sh START\n"
        return 1
    fi
    
    printf "\n\n ---- WEB: Index Page ---- \n"
    curl -s http://127.0.0.1:8000
    printf "\n"

    sleep 2
    printf "\n\n ---- WEB: Index Page with Parameter ---- \n"
    curl -s http://127.0.0.1:8000?name=Krishna
    printf "\n"
}
get-session-id(){
    # Connect to SSE endpoint and extract session_id from endpoint event
    # The SSE stream will contain an event like: event: endpoint\ndata: /messages/?session_id=...
    local sse_output=""
    local session_id=""
    
    # Try to get SSE output with timeout (portable method)
    if command -v timeout >/dev/null 2>&1; then
        sse_output=$(timeout 5 curl -s -N http://127.0.0.1:8000/sse 2>/dev/null | head -20)
    else
        # macOS doesn't have timeout by default, use curl's --max-time instead
        sse_output=$(curl -s -N --max-time 5 http://127.0.0.1:8000/sse 2>/dev/null | head -20)
    fi
    
    # Try to extract session_id from the endpoint event
    # Format can be: data: /messages/?session_id=abc123 or data: {"url": "/messages/?session_id=abc123"}
    
    # Method 1: Extract from URL format (data: /messages/?session_id=...)
    if echo "$sse_output" | grep -q "session_id="; then
        session_id=$(echo "$sse_output" | sed -n 's/.*session_id=\([^"& ]*\).*/\1/p' | head -1)
    fi
    
    # Method 2: Extract from JSON format (data: {"url": "/messages/?session_id=..."})
    if [ -z "$session_id" ] && echo "$sse_output" | grep -q '"url"'; then
        session_id=$(echo "$sse_output" | sed -n 's/.*"url"[^"]*session_id=\([^"&]*\).*/\1/p' | head -1)
    fi
    
    # Last resort: generate a random session_id (server will accept any valid UUID format)
    if [ -z "$session_id" ]; then
        if command -v uuidgen >/dev/null 2>&1; then
            session_id=$(uuidgen | tr -d '-' | cut -c1-32)
        elif command -v openssl >/dev/null 2>&1; then
            session_id=$(openssl rand -hex 16)
        else
            # Fallback: use date and random number
            session_id="test-$(date +%s)-$$"
        fi
    fi
    
    echo "$session_id"
}

test-apis(){
    # Check if server is running
    if ! curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
        printf "\n\n ERROR: Server is not running on http://127.0.0.1:8000\n"
        printf " Please start the server first with: ./mcp.sh START\n"
        return 1
    fi
    
    # Get dynamic session_id from MCP server SSE endpoint
    printf "\n Getting session_id from MCP server...\n"
    export session_id="1a1e6d0299d94522966ade8e7f0b67f9" # $(get-session-id)
    printf " Using session_id: %s\n" "$session_id"
    
    printf "\n\n ---- API: method: initialize ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{  "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": { "protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": { "name": "curl-client", "version": "1.0" }  } }'
    printf "\n"
    sleep 2

    printf "\n\n ---- API: method: tools/list ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }'
    printf "\n"
    sleep 2

    printf "\n\n ---- API: method: tools/call - index ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": { "name": "index", "arguments": {} } }'
    printf "\n"
    sleep 2

    printf "\n\n ---- API: method: tools/call - greeting with param ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": { "name": "greeting", "arguments": { "name": "Krishna" } } }'
    printf "\n"
    sleep 2

    printf "\n\n ---- API: method: tools/call - weather tool ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=${session_id}" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": { "name": "weather", "arguments": { "city": "San Francisco" } } }'
    printf "\n"
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
        TEST-APIS)
            test-apis
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