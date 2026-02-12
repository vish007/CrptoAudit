"""Admin endpoints for system administration."""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.user import Role, Permission, AuditLog, User, Tenant
from app.schemas.user import (
    RoleResponse,
    RoleCreate,
    RoleUpdate,
    PermissionResponse,
    PermissionCreate,
    AuditLogResponse,
)

router = APIRouter(prefix="/admin", tags=["admin"])


def check_superadmin(current_user):
    """Check if user is superadmin."""
    if not current_user.get("is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superadmin access required",
        )


@router.get("/dashboard")
async def get_admin_dashboard(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get admin dashboard statistics.

    Args:
        current_user: Current authenticated user
        session: Database session

    Returns:
        Dashboard data

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    from sqlalchemy import func

    # Count stats
    stmt = select(func.count()).select_from(User)
    result = await session.execute(stmt)
    user_count = result.scalar()

    stmt = select(func.count()).select_from(Tenant)
    result = await session.execute(stmt)
    tenant_count = result.scalar()

    stmt = select(func.count()).select_from(AuditLog)
    result = await session.execute(stmt)
    audit_count = result.scalar()

    from app.models.engagement import Engagement
    stmt = select(func.count()).select_from(Engagement)
    result = await session.execute(stmt)
    engagement_count = result.scalar()

    return {
        "total_users": user_count,
        "total_tenants": tenant_count,
        "total_engagements": engagement_count,
        "audit_logs": audit_count,
        "system_health": "OK",
    }


@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_create: RoleCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create custom role.

    Args:
        role_create: Role data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created role

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    user_id = current_user.get("sub")

    role = Role(
        name=role_create.name,
        description=role_create.description,
        is_system_role=False,
        permissions_json=role_create.permissions_json or [],
        created_by=user_id,
    )

    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List all roles.

    Args:
        current_user: Current authenticated user
        session: Database session
        skip: Number of records to skip
        limit: Max records to return

    Returns:
        List of roles

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Role).offset(skip).limit(limit)
    result = await session.execute(stmt)
    roles = result.scalars().all()

    return roles


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get role by ID.

    Args:
        role_id: Role ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Role details

    Raises:
        HTTPException: If not found or not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Role).where(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    return role


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str,
    role_update: RoleUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update role.

    Args:
        role_id: Role ID
        role_update: Update data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated role

    Raises:
        HTTPException: If not found or not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Role).where(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role_update.name:
        role.name = role_update.name
    if role_update.description is not None:
        role.description = role_update.description
    if role_update.permissions_json is not None:
        role.permissions_json = role_update.permissions_json

    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role


@router.put("/roles/{role_id}/permissions")
async def update_role_permissions(
    role_id: str,
    permissions: List[str],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update role permissions (custom role builder).

    Args:
        role_id: Role ID
        permissions: List of permission IDs
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated role

    Raises:
        HTTPException: If not found or not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Role).where(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    role.permissions_json = permissions
    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete role.

    Args:
        role_id: Role ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If not found or not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Role).where(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system roles",
        )

    await session.delete(role)
    await session.commit()

    return {"message": "Role deleted successfully"}


@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_create: PermissionCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create new permission.

    Args:
        permission_create: Permission data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created permission

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    user_id = current_user.get("sub")

    permission = Permission(
        resource=permission_create.resource,
        action=permission_create.action,
        description=permission_create.description,
        field_restrictions_json=permission_create.field_restrictions_json or {},
        created_by=user_id,
    )

    session.add(permission)
    await session.commit()
    await session.refresh(permission)

    return permission


@router.get("/permissions", response_model=List[PermissionResponse])
async def list_permissions(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    List all permissions.

    Args:
        current_user: Current authenticated user
        session: Database session

    Returns:
        List of permissions

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    stmt = select(Permission)
    result = await session.execute(stmt)
    permissions = result.scalars().all()

    return permissions


@router.get("/audit-log", response_model=List[AuditLogResponse])
async def get_audit_log(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    resource: str = Query(None),
    user_id: str = Query(None),
):
    """
    Get audit log entries.

    Args:
        current_user: Current authenticated user
        session: Database session
        skip: Number of records to skip
        limit: Max records to return
        resource: Filter by resource type
        user_id: Filter by user ID

    Returns:
        Audit log entries

    Raises:
        HTTPException: If not superadmin
    """
    check_superadmin(current_user)

    query = select(AuditLog)

    if resource:
        query = query.where(AuditLog.resource == resource)
    if user_id:
        query = query.where(AuditLog.user_id == user_id)

    query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)

    result = await session.execute(query)
    logs = result.scalars().all()

    return logs
