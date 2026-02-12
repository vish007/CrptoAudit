"""Engagement management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.engagement import Engagement, EngagementAsset, EngagementTimeline
from app.schemas.engagement import (
    EngagementResponse,
    EngagementDetailResponse,
    EngagementCreate,
    EngagementUpdate,
    EngagementStatusUpdate,
    EngagementSummaryResponse,
    BulkAssetImportRequest,
    BulkAssetImportResponse,
    EngagementAssetResponse,
    EngagementTimelineResponse,
)

router = APIRouter(prefix="/engagements", tags=["engagements"])


@router.post("", response_model=EngagementResponse)
async def create_engagement(
    engagement_create: EngagementCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create new engagement.

    Args:
        engagement_create: Engagement creation data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created engagement
    """
    user_id = current_user.get("sub")

    engagement = Engagement(
        name=engagement_create.name,
        client_tenant_id=engagement_create.client_tenant_id,
        auditor_tenant_id=engagement_create.auditor_tenant_id,
        reporting_date=engagement_create.reporting_date,
        status="PLANNING",
        settings_json=engagement_create.settings_json or {},
        created_by=user_id,
    )

    session.add(engagement)
    await session.commit()
    await session.refresh(engagement)

    return engagement


@router.get("", response_model=List[EngagementSummaryResponse])
async def list_engagements(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: str = Query(None),
):
    """
    List engagements for current tenant.

    Args:
        current_user: Current authenticated user
        session: Database session
        skip: Number of records to skip
        limit: Max records to return
        status_filter: Filter by engagement status

    Returns:
        List of engagements
    """
    tenant_id = extract_tenant_id(current_user)

    query = select(Engagement).where(
        or_(
            Engagement.client_tenant_id == tenant_id,
            Engagement.auditor_tenant_id == tenant_id,
        )
    )

    if status_filter:
        query = query.where(Engagement.status == status_filter)

    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    engagements = result.scalars().all()

    return engagements


@router.get("/{engagement_id}", response_model=EngagementDetailResponse)
async def get_engagement(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get engagement by ID.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Engagement details

    Raises:
        HTTPException: If engagement not found
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    # Check tenant access
    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return engagement


@router.put("/{engagement_id}", response_model=EngagementResponse)
async def update_engagement(
    engagement_id: str,
    engagement_update: EngagementUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update engagement.

    Args:
        engagement_id: Engagement ID
        engagement_update: Update data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated engagement
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can update engagement",
        )

    if engagement_update.name:
        engagement.name = engagement_update.name
    if engagement_update.reporting_date:
        engagement.reporting_date = engagement_update.reporting_date
    if engagement_update.settings_json:
        engagement.settings_json = engagement_update.settings_json

    session.add(engagement)
    await session.commit()
    await session.refresh(engagement)

    return engagement


@router.put("/{engagement_id}/status", response_model=EngagementResponse)
async def update_engagement_status(
    engagement_id: str,
    status_update: EngagementStatusUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update engagement status.

    Args:
        engagement_id: Engagement ID
        status_update: New status
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated engagement
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can update status",
        )

    engagement.status = status_update.status
    session.add(engagement)
    await session.commit()
    await session.refresh(engagement)

    return engagement


@router.delete("/{engagement_id}")
async def delete_engagement(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can delete",
        )

    await session.delete(engagement)
    await session.commit()

    return {"message": "Engagement deleted successfully"}


@router.post("/{engagement_id}/assets", response_model=BulkAssetImportResponse)
async def bulk_add_assets(
    engagement_id: str,
    bulk_import: BulkAssetImportRequest,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Bulk add assets to engagement.

    Args:
        engagement_id: Engagement ID
        bulk_import: List of assets to add
        current_user: Current authenticated user
        session: Database session

    Returns:
        Import results
    """
    tenant_id = extract_tenant_id(current_user)
    user_id = current_user.get("sub")

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can add assets",
        )

    imported_count = 0
    failed_count = 0
    errors = []

    for asset_data in bulk_import.assets:
        try:
            asset = EngagementAsset(
                engagement_id=engagement_id,
                asset_symbol=asset_data.asset_symbol,
                asset_name=asset_data.asset_name,
                tier=asset_data.tier,
                contract_addresses_json=asset_data.contract_addresses_json or {},
                blockchains_json=asset_data.blockchains_json or [],
                created_by=user_id,
            )
            session.add(asset)
            imported_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(
                {
                    "symbol": asset_data.asset_symbol,
                    "error": str(e),
                }
            )

    engagement.asset_count = imported_count
    session.add(engagement)
    await session.commit()

    return BulkAssetImportResponse(
        imported_count=imported_count,
        failed_count=failed_count,
        errors=errors,
    )


@router.get("/{engagement_id}/timeline", response_model=List[EngagementTimelineResponse])
async def get_engagement_timeline(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get engagement timeline.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Timeline phases
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    stmt = select(EngagementTimeline).where(
        EngagementTimeline.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    timelines = result.scalars().all()

    return timelines


@router.post("/{engagement_id}/timeline", response_model=EngagementTimelineResponse)
async def create_timeline_phase(
    engagement_id: str,
    timeline_create,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Add timeline phase to engagement.

    Args:
        engagement_id: Engagement ID
        timeline_create: Timeline data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created timeline phase
    """
    tenant_id = extract_tenant_id(current_user)
    user_id = current_user.get("sub")

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can manage timeline",
        )

    timeline = EngagementTimeline(
        engagement_id=engagement_id,
        phase=timeline_create.phase,
        start_date=timeline_create.start_date,
        end_date=timeline_create.end_date,
        status="PENDING",
        created_by=user_id,
    )

    session.add(timeline)
    await session.commit()
    await session.refresh(timeline)

    return timeline


from sqlalchemy import or_
