"""Setup script for MCP Server package.

This setup.py is kept for backward compatibility.
The primary build configuration is in pyproject.toml.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-server",
    version="1.0.0",
    author="Krishna Manchikalapudi",
    description="Production-grade Model Context Protocol server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-jose[cryptography]>=3.3.0",
        "slowapi>=0.1.9",
        "redis>=5.0.1",
        "tenacity>=8.2.3",
        "prometheus-client>=0.19.0",
        "opentelemetry-api>=1.21.0",
        "opentelemetry-sdk>=1.21.0",
        "opentelemetry-instrumentation-fastapi>=0.42b0",
        "opentelemetry-exporter-otlp>=1.21.0",
        "httpx>=0.25.2",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.6",
            "black>=23.11.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-server=src.main:main",
        ],
    },
)
