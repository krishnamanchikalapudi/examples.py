# https://hub.docker.com/_/python
FROM python:3.12-slim

# Copy the uv binary from the astral-sh/uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv lock && uv sync && uv pip install -e ".[dev]" 

# RUN tests
RUN uv run pytest tests/maintests.py -v

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application
# uv run src/main.py
CMD ["uv", "run", "src/main.py"]