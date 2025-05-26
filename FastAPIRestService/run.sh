#!/bin/bash

# install dependencies
pip install -r requirements.txt

# compule source code
python3 -m compileall -l ./src/

# pkill -f Python && 
# kill -9 (lsof -i :8000|grep LISTEN) &

# fastapi dev src/index.py & 
uvicorn src.index:app --reload --host 0.0.0.0 --port 8000 &


# fastapi dev src/index.py
# Note: The host is set to 127.0.0, which is a loopback address.

# open -a "Google Chrome" "http://127.0.0.1:8000/124"

curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/
echo "\n\n"
curl -H "Content-Type: application/json" http://127.0.0.1:8000/1243

# pkill -f uvicorn &