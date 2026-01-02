"""Configuration management with environment variable support."""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    # Server Configuration
    app_name: str = Field(default="MCP Server", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")
    allowed_origins: list[str] = Field(
        default=["*"], env="ALLOWED_ORIGINS"
    )

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")

    # Redis Configuration
    redis_enabled: bool = Field(default=False, env="REDIS_ENABLED")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_ttl: int = Field(default=3600, env="REDIS_TTL")

    # Observability
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    enable_tracing: bool = Field(default=True, env="ENABLE_TRACING")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")

    # External Services
    tracing_endpoint: Optional[str] = Field(default=None, env="TRACING_ENDPOINT")
    metrics_endpoint: Optional[str] = Field(default=None, env="METRICS_ENDPOINT")

    # Circuit Breaker
    circuit_breaker_failure_threshold: int = Field(
        default=5, env="CIRCUIT_BREAKER_FAILURE_THRESHOLD"
    )
    circuit_breaker_timeout: int = Field(
        default=60, env="CIRCUIT_BREAKER_TIMEOUT"
    )

    # Retry Configuration
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    retry_backoff_factor: float = Field(default=1.0, env="RETRY_BACKOFF_FACTOR")

    # Health Check
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse allowed origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

