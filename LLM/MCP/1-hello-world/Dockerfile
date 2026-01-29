# https://hub.docker.com/_/python
FROM python:3.12-slim

# Copy the uv binary from the astral-sh/uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y  curl git gnupg && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs && npm install -g npm@latest && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the project into the image
COPY ./ /app/

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv lock && uv sync --frozen && uv pip install -e ".[dev]" 

# Expose the port
EXPOSE 8000

# Run the application
# uv run src/main.py
CMD ["uv", "run", "src/main.py"]