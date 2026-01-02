"""Main FastAPI application with MCP server endpoints."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.config.cache import cache_service
from src.config.config import get_settings
from src.config.logger import logger
from src.mcp.handlers import MCPHandlers
from src.mcp.protocol import MCPProtocolHandler, MCPRequest
from src.util.middleware import (
    CorrelationIDMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    SecurityHeadersMiddleware,
)
from src.config.security import limiter

settings = get_settings()

# Initialize MCP protocol handler
mcp_handler = MCPProtocolHandler()

# Register MCP method handlers
mcp_handler.register_handler("initialize", MCPHandlers.initialize)
mcp_handler.register_handler("tools/list", MCPHandlers.tools_list)
mcp_handler.register_handler("tools/call", MCPHandlers.tools_call)
mcp_handler.register_handler("resources/list", MCPHandlers.resources_list)
mcp_handler.register_handler("resources/read", MCPHandlers.resources_read)
mcp_handler.register_handler("prompts/list", MCPHandlers.prompts_list)
mcp_handler.register_handler("prompts/get", MCPHandlers.prompts_get)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {'development' if settings.debug else 'production'}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade MCP (Model Context Protocol) Server",
    lifespan=lifespan,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware (order matters)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    cache_health = cache_service.health_check()

    return {
        "status": "healthy",
        "cache": cache_health,
        "version": settings.app_version,
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Check critical dependencies
    cache_health = cache_service.health_check()

    if not cache_health.get("healthy", True) and settings.redis_enabled:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "cache unavailable"},
        )

    return {"status": "ready"}


@app.post("/mcp")
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def mcp_endpoint(request: Request):
    """Main MCP protocol endpoint."""
    try:
        data = await request.json()
        mcp_request = mcp_handler.parse_message(data)

        if not mcp_request:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Invalid MCP request"},
            )

        response = await mcp_handler.handle_request(mcp_request)
        return response.dict()

    except Exception as e:
        logger.error(f"MCP endpoint error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error", "detail": str(e)},
        )


@app.get("/metrics")
async def metrics():
    """Metrics endpoint (Prometheus format)."""
    # In production, integrate with Prometheus client
    return {
        "requests_total": 0,
        "requests_per_second": 0,
        "error_rate": 0,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )

