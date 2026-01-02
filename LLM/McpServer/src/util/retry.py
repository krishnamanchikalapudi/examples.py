"""Retry utilities with exponential backoff."""

import asyncio
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.config.config import get_settings
from src.config.logger import logger

settings = get_settings()

T = TypeVar("T")


def retry_with_backoff(
    max_retries: int = None,
    backoff_factor: float = None,
    exceptions: tuple = (Exception,),
):
    """Decorator for retrying with exponential backoff."""
    max_retries = max_retries or settings.max_retries
    backoff_factor = backoff_factor or settings.retry_backoff_factor

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {str(e)}"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} retry attempts failed")
            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {str(e)}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} retry attempts failed")
            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


# Tenacity-based retry decorator (more feature-rich)
def retry_with_tenacity(
    max_attempts: int = None,
    wait_multiplier: float = 1.0,
    exceptions: tuple = (Exception,),
):
    """Retry decorator using tenacity library."""
    max_attempts = max_attempts or settings.max_retries

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=wait_multiplier),
        retry=retry_if_exception_type(exceptions),
        reraise=True,
    )

