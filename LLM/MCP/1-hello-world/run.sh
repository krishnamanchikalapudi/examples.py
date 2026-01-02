#!/bin/bash


uv sync

uv run pytest tests/maintests.py

uv run src/main.py

open http://127.0.0.1:8000