"""Caching layer with Redis support for performance optimization."""

from typing import Any, Optional

from src.config.config import get_settings
from src.config.logger import logger

settings = get_settings()

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Caching will be disabled.")


class CacheService:
    """Cache service with Redis backend."""

    def __init__(self):
        """Initialize cache service."""
        self.client: Optional[Any] = None
        self.enabled = settings.redis_enabled and REDIS_AVAILABLE

        if self.enabled:
            try:
                self.client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    password=settings.redis_password,
                    db=settings.redis_db,
                    decode_responses=True,
                    socket_connect_timeout=5,
                )
                # Test connection
                self.client.ping()
                logger.info("Redis cache initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Redis: {str(e)}")
                self.enabled = False
                self.client = None

    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if not self.enabled or not self.client:
            return None

        try:
            return self.client.get(key)
        except Exception as e:
            logger.warning(f"Cache get error: {str(e)}")
            return None

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        if not self.enabled or not self.client:
            return False

        try:
            ttl = ttl or settings.redis_ttl
            self.client.setex(key, ttl, value)
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.enabled or not self.client:
            return False

        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.enabled or not self.client:
            return False

        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.warning(f"Cache exists error: {str(e)}")
            return False

    def health_check(self) -> dict:
        """Check cache health."""
        if not self.enabled:
            return {"status": "disabled", "healthy": True}

        try:
            if self.client:
                self.client.ping()
                return {"status": "enabled", "healthy": True}
            return {"status": "enabled", "healthy": False}
        except Exception as e:
            logger.error(f"Cache health check failed: {str(e)}")
            return {"status": "enabled", "healthy": False, "error": str(e)}


# Global cache instance
cache_service = CacheService()

def get_cache_service() -> CacheService:
    """Get cache service instance."""
    return cache_service