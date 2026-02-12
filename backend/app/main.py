"""
FastAPI application for SimplyFI Proof of Reserves Platform.

Production-grade backend with:
- Multi-tenant SaaS architecture
- Comprehensive RBAC
- Blockchain integration
- Merkle tree proofs
- AI-powered analytics
- Audit compliance
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import init_db, close_db
from app.middleware.audit_log import AuditLogMiddleware
from app.middleware.tenant import TenantIsolationMiddleware
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan - startup and shutdown events.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    logger.info("Starting SimplyFI POR Platform")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down SimplyFI POR Platform")
    try:
        await close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Proof of Reserves auditing platform for crypto digital assets",
    openapi_url="/api/v1/openapi.json" if not settings.DEBUG else "/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Add tenant isolation middleware
app.add_middleware(TenantIsolationMiddleware)

# Add audit logging middleware
app.add_middleware(AuditLogMiddleware)

# Rate limiting
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"},
    )


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """
    Readiness check for load balancers.

    Returns:
        Readiness status
    """
    try:
        # In production, would check database connectivity here
        return {"ready": True}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False},
        )


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs",
        "api": "/api/v1",
    }


# Include API routers
app.include_router(api_router)


# Startup event for additional initialization
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL}")


# Shutdown event for cleanup
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
