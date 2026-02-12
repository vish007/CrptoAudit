"""Reserve verification and reporting endpoints."""
from typing import List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.engagement import Engagement
from app.models.asset import (
    ReserveRatio,
    AssetBalance,
    CustomerLiability,
    ReconciliationRecord,
)
from app.schemas.asset import (
    ReserveRatioResponse,
    ReconciliationRecordResponse,
    ReserveSummaryResponse,
)

router = APIRouter(prefix="/engagements", tags=["reserves"])


@router.get("/{engagement_id}/reserves", response_model=ReserveSummaryResponse)
async def get_reserves(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get reserve summary for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Reserve summary with ratios by asset

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

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    stmt = select(ReserveRatio).where(ReserveRatio.engagement_id == engagement_id)
    result = await session.execute(stmt)
    ratios = result.scalars().all()

    total_assets = sum(Decimal(r.total_assets) for r in ratios)
    total_liabilities = sum(Decimal(r.total_liabilities) for r in ratios)
    overall_ratio = (
        (total_assets / total_liabilities * 100) if total_liabilities > 0 else 0
    )

    return ReserveSummaryResponse(
        engagement_id=engagement_id,
        total_assets_usd=float(total_assets),
        total_liabilities_usd=float(total_liabilities),
        overall_ratio_pct=float(overall_ratio),
        meets_requirement=overall_ratio >= 95.0,
        by_asset=ratios,
        last_updated=engagement.updated_at,
    )


@router.post("/{engagement_id}/reserves/calculate")
async def calculate_reserves(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Calculate reserve ratios for all assets.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Calculation results

    Raises:
        HTTPException: If engagement not found
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
            detail="Only auditor can calculate reserves",
        )

    from datetime import datetime, timezone
    from app.core.config import settings

    calculated_count = 0

    # Get all assets in engagement
    from app.models.engagement import EngagementAsset
    stmt = select(EngagementAsset).where(EngagementAsset.engagement_id == engagement_id)
    result = await session.execute(stmt)
    assets = result.scalars().all()

    for asset in assets:
        # Calculate total assets
        stmt = select(func.sum(AssetBalance.verified_balance)).where(
            and_(
                AssetBalance.engagement_id == engagement_id,
                AssetBalance.asset_id == asset.id,
            )
        )
        result = await session.execute(stmt)
        total_assets = result.scalar() or Decimal(0)

        # Calculate total liabilities
        stmt = select(func.sum(CustomerLiability.balance)).where(
            and_(
                CustomerLiability.engagement_id == engagement_id,
                CustomerLiability.asset_id == asset.id,
            )
        )
        result = await session.execute(stmt)
        total_liabilities = result.scalar() or Decimal(0)

        # Calculate ratio
        if total_liabilities > 0:
            ratio = (total_assets / total_liabilities) * 100
        else:
            ratio = Decimal(0)

        reserve_ratio = ReserveRatio(
            engagement_id=engagement_id,
            asset_id=asset.id,
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            ratio_percentage=ratio,
            meets_vara_requirement=ratio >= settings.VARA_MIN_RESERVE_RATIO * 100,
            calculated_at=datetime.now(timezone.utc),
            created_by=user_id,
        )

        session.add(reserve_ratio)
        calculated_count += 1

    await session.commit()

    return {
        "message": "Reserves calculated",
        "calculated_count": calculated_count,
    }


@router.get("/{engagement_id}/reserves/ratio-table", response_model=List[ReserveRatioResponse])
async def get_reserve_ratio_table(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get reserve ratio table for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        List of reserve ratios
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

    stmt = select(ReserveRatio).where(ReserveRatio.engagement_id == engagement_id)
    result = await session.execute(stmt)
    ratios = result.scalars().all()

    return ratios


@router.post("/{engagement_id}/reserves/verify-segregation")
async def verify_customer_segregation(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Verify customer assets are properly segregated.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Verification results
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
            detail="Only auditor can verify segregation",
        )

    # Verify all customer liabilities are accounted for in wallets
    stmt = select(func.sum(CustomerLiability.balance)).where(
        CustomerLiability.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    total_liabilities = result.scalar() or Decimal(0)

    stmt = select(func.sum(AssetBalance.verified_balance)).where(
        AssetBalance.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    total_assets = result.scalar() or Decimal(0)

    variance = abs(total_assets - total_liabilities)
    segregation_valid = variance == 0 or (variance / total_liabilities * 100) < 1

    return {
        "total_liabilities": float(total_liabilities),
        "total_assets": float(total_assets),
        "variance": float(variance),
        "variance_pct": float((variance / total_liabilities * 100) if total_liabilities > 0 else 0),
        "segregation_valid": segregation_valid,
    }


@router.get("/{engagement_id}/reconciliation", response_model=List[ReconciliationRecordResponse])
async def get_reconciliation_records(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get reconciliation records for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        List of reconciliation records
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

    stmt = select(ReconciliationRecord).where(
        ReconciliationRecord.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    records = result.scalars().all()

    return records
