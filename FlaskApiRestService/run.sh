#!/bin/bash

# install dependencies
pip install -r requirements.txt

# compule source code
python -m compileall -l ./src/

pkill -f uvicorn &

#run the Flask application
export FLASK_APP=src/index.py
export FLASK_ENV=development
fastapi dev src/index.py & 

# fastapi dev src/index.py
# Note: The host is set to 127.0.0, which is a loopback address.

curl -H "Content-Type: application/json" http://127.0.0.1:5000/
echo "\n\n"

curl -H "Content-Type: application/json" http://127.0.0.1:5000/1243

# open -a "Google Chrome" "http://127.0.0.1:5000/124"
