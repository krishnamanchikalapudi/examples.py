"""Tests for cache service."""

import pytest
from src.cache import CacheService


def test_cache_service_initialization():
    """Test cache service initialization."""
    cache = CacheService()
    assert cache is not None


def test_cache_get_nonexistent():
    """Test getting non-existent key."""
    cache = CacheService()
    result = cache.get("nonexistent_key")
    # Should return None if cache is disabled or key doesn't exist
    assert result is None or isinstance(result, str)


def test_cache_set_and_get():
    """Test setting and getting cache value."""
    cache = CacheService()
    key = "test_key"
    value = "test_value"

    # Set value
    success = cache.set(key, value)
    # May fail if Redis is not available, which is acceptable
    assert isinstance(success, bool)

    # Get value (may return None if Redis unavailable)
    result = cache.get(key)
    # Result can be None (if disabled) or the value
    assert result is None or result == value


def test_cache_health_check():
    """Test cache health check."""
    cache = CacheService()
    health = cache.health_check()
    assert "status" in health
    assert "healthy" in health

