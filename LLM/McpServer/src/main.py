"""Application entry point."""

import uvicorn

from src.config.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "src.server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
        log_level=settings.log_level.lower(),
    )

