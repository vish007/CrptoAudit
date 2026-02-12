"""Tenant management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.user import Tenant, User
from app.schemas.user import (
    TenantResponse,
    TenantCreate,
    TenantUpdate,
    UserResponse,
)

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_create: TenantCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new tenant.

    Args:
        tenant_create: Tenant creation data
        session: Database session

    Returns:
        Created tenant
    """
    tenant = Tenant(
        name=tenant_create.name,
        type=tenant_create.type,
        vara_license_number=tenant_create.vara_license_number,
        settings_json=tenant_create.settings_json or {},
        status="ACTIVE",
    )

    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return tenant


@router.get("", response_model=List[TenantResponse])
async def list_tenants(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List all tenants.

    Args:
        session: Database session
        skip: Number of records to skip
        limit: Max records to return

    Returns:
        List of tenants
    """
    stmt = select(Tenant).offset(skip).limit(limit)
    result = await session.execute(stmt)
    tenants = result.scalars().all()

    return tenants


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Get tenant by ID.

    Args:
        tenant_id: Tenant ID
        session: Database session

    Returns:
        Tenant details

    Raises:
        HTTPException: If tenant not found
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant_update: TenantUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update tenant.

    Args:
        tenant_id: Tenant ID
        tenant_update: Update data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated tenant
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    if tenant_update.name:
        tenant.name = tenant_update.name
    if tenant_update.settings_json:
        tenant.settings_json = tenant_update.settings_json

    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return tenant


@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete tenant.

    Args:
        tenant_id: Tenant ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    await session.delete(tenant)
    await session.commit()

    return {"message": "Tenant deleted successfully"}


@router.get("/{tenant_id}/members", response_model=List[UserResponse])
async def list_tenant_members(
    tenant_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List members of a tenant.

    Args:
        tenant_id: Tenant ID
        current_user: Current authenticated user
        session: Database session
        skip: Number of records to skip
        limit: Max records to return

    Returns:
        List of users in tenant

    Raises:
        HTTPException: If tenant not found
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    stmt = (
        select(User)
        .where(User.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()

    return users


@router.put("/{tenant_id}/settings", response_model=TenantResponse)
async def update_tenant_settings(
    tenant_id: str,
    settings: dict,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update tenant settings.

    Args:
        tenant_id: Tenant ID
        settings: New settings object
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated tenant
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    tenant.settings_json = settings
    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return tenant
