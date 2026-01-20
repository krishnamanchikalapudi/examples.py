rm -rf **/.pytest_cache
rm -rf **/.ruff_cache
rm -rf **/.venv
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "uv.lock" -delete