"""
Configuration management for the FastAPI application.
Uses Pydantic Settings for environment variable support.
"""
import json
from typing import Dict, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str = "SimplyFI Proof of Reserves Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/por_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # AWS S3
    S3_BUCKET: str = "simplyfi-por-reports"
    S3_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # JWT Configuration
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_SPECIAL: bool = True
    MFA_ENABLED_BY_DEFAULT: bool = True
    MFA_ISSUER: str = "SimplyFI"
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "https://app.simplyfi.com"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # AI/ML
    LLAMA_MODEL_PATH: str = "/models/llama-2-7b-chat.gguf"
    ENABLE_LOCAL_LLM: bool = False
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_TOKENS_PER_REQUEST: int = 4096

    # Blockchain APIs
    BLOCKCHAIN_API_KEYS: Dict[str, str] = {
        "ethereum": "",
        "polygon": "",
        "bitcoin": "",
        "litecoin": "",
        "ripple": "",
        "solana": "",
    }
    BLOCKCHAIN_API_TIMEOUT: int = 30

    # VARA Compliance
    VARA_LICENSE_NUMBER: str = "VARA-001-2024"
    VARA_COMPLIANCE_LEVEL: str = "LEVEL_3"
    VARA_AUDIT_RETENTION_YEARS: int = 7
    VARA_MIN_RESERVE_RATIO: float = 0.95  # 95%

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Email (for notifications)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@simplyfi.com"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
