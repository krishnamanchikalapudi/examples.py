"""Security utilities: authentication, authorization, rate limiting."""

import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.config.config import get_settings
from src.config.logger import logger

settings = get_settings()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# API Key security
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


class SecurityService:
    """Security service for authentication and authorization."""

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            return payload
        except JWTError as e:
            logger.warning(f"Token verification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

    @staticmethod
    def verify_api_key(api_key: str) -> bool:
        """Verify API key (implement your own logic)."""
        # In production, validate against database or secret store
        # This is a placeholder implementation
        expected_key_hash = hashlib.sha256(settings.secret_key.encode()).hexdigest()
        provided_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        return hmac.compare_digest(expected_key_hash, provided_key_hash)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()


async def get_api_key(request: Request, api_key: Optional[str] = Depends(api_key_header)) -> str:
    """Dependency to get and validate API key."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )

    security_service = SecurityService()
    if not security_service.verify_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return api_key


async def get_current_user(request: Request) -> dict:
    """Dependency to get current authenticated user."""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token = authorization.split(" ")[1]
    security_service = SecurityService()
    payload = security_service.verify_token(token)
    return payload

