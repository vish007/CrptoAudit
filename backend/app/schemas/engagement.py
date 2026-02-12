"""Pydantic schemas for engagement operations."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class EngagementAssetBase(BaseModel):
    """Base engagement asset schema."""

    asset_symbol: str = Field(..., min_length=1, max_length=20)
    asset_name: str = Field(..., min_length=1, max_length=255)
    tier: int = Field(default=1, ge=1, le=3)
    contract_addresses_json: Optional[Dict[str, Any]] = {}
    blockchains_json: Optional[List[str]] = []


class EngagementAssetCreate(EngagementAssetBase):
    """Create engagement asset request."""

    pass


class EngagementAssetResponse(EngagementAssetBase):
    """Engagement asset response."""

    id: str
    engagement_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EngagementTimelineBase(BaseModel):
    """Base timeline schema."""

    phase: str = Field(..., min_length=1, max_length=100)
    start_date: datetime
    end_date: Optional[datetime] = None


class EngagementTimelineCreate(EngagementTimelineBase):
    """Create timeline request."""

    pass


class EngagementTimelineResponse(EngagementTimelineBase):
    """Timeline response."""

    id: str
    engagement_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EngagementBase(BaseModel):
    """Base engagement schema."""

    name: str = Field(..., min_length=1, max_length=255)
    reporting_date: datetime
    settings_json: Optional[Dict[str, Any]] = {}


class EngagementCreate(EngagementBase):
    """Create engagement request."""

    client_tenant_id: str
    auditor_tenant_id: str


class EngagementUpdate(BaseModel):
    """Update engagement request."""

    name: Optional[str] = None
    reporting_date: Optional[datetime] = None
    settings_json: Optional[Dict[str, Any]] = None


class EngagementStatusUpdate(BaseModel):
    """Update engagement status."""

    status: str = Field(..., pattern="^(PLANNING|DATA_COLLECTION|VERIFICATION|REPORTING|COMPLETED)$")


class EngagementResponse(EngagementBase):
    """Engagement response."""

    id: str
    client_tenant_id: str
    auditor_tenant_id: str
    status: str
    asset_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EngagementDetailResponse(EngagementResponse):
    """Engagement detail response with related data."""

    assets: List[EngagementAssetResponse] = []
    timelines: List[EngagementTimelineResponse] = []


class EngagementSummaryResponse(BaseModel):
    """Engagement summary for dashboard."""

    id: str
    name: str
    status: str
    client_name: str
    auditor_name: str
    asset_count: int
    total_assets_usd: Optional[float] = None
    total_liabilities_usd: Optional[float] = None
    reserve_ratio: Optional[float] = None
    meets_vara_requirement: Optional[bool] = None
    last_updated: datetime
    reporting_date: datetime


class BulkAssetImportRequest(BaseModel):
    """Bulk asset import request."""

    assets: List[EngagementAssetCreate]


class BulkAssetImportResponse(BaseModel):
    """Bulk asset import response."""

    imported_count: int
    failed_count: int
    errors: List[Dict[str, Any]] = []
