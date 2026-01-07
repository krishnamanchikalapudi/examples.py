#!/bin/bash
arg=${1:-"START"}

prereq(){
    uv lock && uv sync
    uv run pytest tests/maintests.py -v
}
start(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Starting Hello World MCP Application ... "
    printf "\n ----------------------------------------------------------------  \n "
    uv run src/main.py & 
    sleep 5
    curl -N http://127.0.0.1:8000/sse & 
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping Hello World MCP Application ... "
    printf "\n ----------------------------------------------------------------  \n "

    # uv stop
    lsof -ti:8000 | xargs kill -9
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
    printf "\n\n ---- API: method: initialize ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=987cdc59979546c582a91edee874b83e" -H "Content-Type: application/json" -d '{  "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": { "protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": { "name": "curl-client", "version": "1.0" }  } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=987cdc59979546c582a91edee874b83e" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - index ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=987cdc59979546c582a91edee874b83e" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": { "name": "index", "arguments": {} } }'
    sleep 2

    printf "\n\n ---- API: method: tools/list - index with param ---- \n"
    curl -X POST "http://127.0.0.1:8000/messages/?session_id=987cdc59979546c582a91edee874b83e" -H "Content-Type: application/json" -d '{ "jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": { "name": "greeting", "arguments": { "name": "Krishna" } } }'
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