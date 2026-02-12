"""Main API router combining all endpoints."""
from fastapi import APIRouter

# Import all endpoint routers
from app.api.v1.endpoints import (
    auth,
    users,
    tenants,
    engagements,
    assets,
    reserves,
    merkle,
    blockchain,
    reports,
    ai,
    admin,
    onboarding,
)

# Create main router
api_router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tenants.router)
api_router.include_router(engagements.router)
api_router.include_router(assets.router)
api_router.include_router(reserves.router)
api_router.include_router(merkle.router)
api_router.include_router(blockchain.router)
api_router.include_router(reports.router)
api_router.include_router(ai.router)
api_router.include_router(admin.router)
api_router.include_router(onboarding.router)
