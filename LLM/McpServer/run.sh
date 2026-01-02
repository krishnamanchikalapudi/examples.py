#!/bin/bash
# Production run script for MCP Server

set -e

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the server
python -m src.main

