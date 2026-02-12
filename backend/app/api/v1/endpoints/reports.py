"""Report generation endpoints."""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.engagement import Engagement

router = APIRouter(prefix="/engagements", tags=["reports"])


@router.post("/{engagement_id}/reports/por")
async def generate_por_report(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate Proof of Reserves report.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Report metadata

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

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can generate reports",
        )

    import uuid
    from datetime import datetime, timezone

    report_id = str(uuid.uuid4())

    return {
        "report_id": report_id,
        "engagement_id": engagement_id,
        "type": "PROOF_OF_RESERVES",
        "status": "GENERATING",
        "created_at": datetime.now(timezone.utc),
        "file_path": f"s3://simplyfi-por-reports/por/{report_id}.pdf",
    }


@router.post("/{engagement_id}/reports/assurance")
async def generate_assurance_report(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate audit assurance report.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Report metadata
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
            detail="Only auditor can generate reports",
        )

    import uuid
    from datetime import datetime, timezone

    report_id = str(uuid.uuid4())

    return {
        "report_id": report_id,
        "engagement_id": engagement_id,
        "type": "ASSURANCE",
        "status": "GENERATING",
        "created_at": datetime.now(timezone.utc),
        "file_path": f"s3://simplyfi-por-reports/assurance/{report_id}.pdf",
    }


@router.post("/{engagement_id}/reports/management-letter")
async def generate_management_letter(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate management letter.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Report metadata
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
            detail="Only auditor can generate reports",
        )

    import uuid
    from datetime import datetime, timezone

    report_id = str(uuid.uuid4())

    return {
        "report_id": report_id,
        "engagement_id": engagement_id,
        "type": "MANAGEMENT_LETTER",
        "status": "GENERATING",
        "created_at": datetime.now(timezone.utc),
        "file_path": f"s3://simplyfi-por-reports/letters/{report_id}.pdf",
    }


@router.post("/{engagement_id}/reports/customer-summary")
async def generate_customer_summary(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate customer-facing summary report.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Report metadata
    """
    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    import uuid
    from datetime import datetime, timezone

    report_id = str(uuid.uuid4())

    return {
        "report_id": report_id,
        "engagement_id": engagement_id,
        "type": "CUSTOMER_SUMMARY",
        "status": "GENERATING",
        "created_at": datetime.now(timezone.utc),
        "file_path": f"s3://simplyfi-por-reports/customer/{report_id}.pdf",
    }


@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: str,
    current_user=Depends(get_current_active_user),
):
    """
    Download report file.

    Args:
        report_id: Report ID
        current_user: Current authenticated user

    Returns:
        Pre-signed S3 URL for download
    """
    # In production, generate pre-signed S3 URL
    return {
        "report_id": report_id,
        "download_url": f"https://s3.amazonaws.com/simplyfi-por-reports/{report_id}.pdf",
        "expires_in": 3600,
    }
