#!/bin/bash
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

arg=${1:-"START"}

start(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Starting FastAPI: Weather API ... "
    printf "\n ----------------------------------------------------------------  \n "
    pip install -r requirements.txt

    python3 -m compileall -l ./src/
    
    # Start the server in background using uvicorn (more reliable than fastapi dev)
    uvicorn src.WeatherApi:app --host 127.0.0.1 --port 5000 --reload > /tmp/weather-api.log 2>&1 &
    SERVER_PID=$!
    
    # Wait for server to be ready
    echo "Waiting for server to start..."
    max_attempts=30
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://127.0.0.1:5000/ > /dev/null 2>&1; then
            echo "Server is ready!"
            break
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    if [ $attempt -eq $max_attempts ]; then
        echo "ERROR: Server failed to start after $max_attempts seconds"
        echo "Check logs: /tmp/weather-api.log"
        return 1
    fi
    
    sleep 2
    test
}
stop(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Stopping FastAPI: Weather API ... "
    printf "\n ----------------------------------------------------------------  \n "
    pids=$(lsof -ti tcp:5000 2>/dev/null)
    if [ -n "$pids" ]; then
        # Handle multiple PIDs - kill can accept multiple PIDs at once
        echo "Killing processes: $pids"
        # Convert newlines to spaces and kill all at once
        kill -9 $(echo "$pids" | tr '\n' ' ') 2>/dev/null || true
    fi
    pkill -f uv && pkill -f uvicorn && pkill -f fastapi
    pkill -f python && pkill -f python3 && pkill -f pip
}
test(){
    printf "\n ----------------------------------------------------------------  "
    printf "\n Testing FastAPI: Weather API ... "
    printf "\n ----------------------------------------------------------------  \n "
    
    # Check if server is running
    if ! lsof -ti tcp:5000 > /dev/null 2>&1; then
        echo "ERROR: Server is not running on port 5000"
        echo "Please run './api.sh START' first to start the server"
        return 1
    fi
    
    echo "Testing /city/San%20Francisco endpoint..."
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "http://127.0.0.1:5000/city/San%20Francisco")
    http_code=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
    body=$(echo "$response" | sed '/HTTP_STATUS/d')
    
    if [ "$http_code" = "200" ]; then
        echo "✓ Success! Status: $http_code"
    else
        echo "✗ Failed! Status: $http_code"
    fi
    echo "$body" | python3 -m json.tool 2>/dev/null 
    
    echo " "
    echo "Testing /city/New%20York endpoint..."
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "http://127.0.0.1:5000/city/New%20York")
    http_code=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
    body=$(echo "$response" | sed '/HTTP_STATUS/d')

    if [ "$http_code" = "200" ]; then
        echo "✓ Success! Status: $http_code"
    else
        echo "✗ Failed! Status: $http_code" 
    fi
     echo "$body" | python3 -m json.tool 2>/dev/null 

    
    echo ""
    echo "API Documentation available at: http://127.0.0.1:5000/docs"
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
            start
            ;;
        TEST)
            test
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