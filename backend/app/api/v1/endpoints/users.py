"""User management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.user import User, Role, UserRole
from app.schemas.user import (
    UserResponse,
    UserDetailResponse,
    UserUpdate,
    UserChangePassword,
    UserRoleAssignment,
)
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_profile(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user
        session: Database session

    Returns:
        User profile with roles
    """
    user_id = current_user.get("sub")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update current user profile.

    Args:
        user_update: User update data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated user
    """
    user_id = current_user.get("sub")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.post("/me/change-password")
async def change_password(
    password_change: UserChangePassword,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Change user password.

    Args:
        password_change: Current and new password
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If current password invalid
    """
    user_id = current_user.get("sub")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(password_change.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    user.hashed_password = hash_password(password_change.new_password)
    session.add(user)
    await session.commit()

    return {"message": "Password changed successfully"}


@router.get("", response_model=List[UserResponse])
async def list_users(
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List users in current tenant.

    Args:
        current_user: Current authenticated user
        session: Database session
        skip: Number of records to skip
        limit: Max records to return

    Returns:
        List of users
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = (
        select(User)
        .where(User.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get user by ID.

    Args:
        user_id: User ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        User details

    Raises:
        HTTPException: If user not found
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(User).where(
        and_(User.id == user_id, User.tenant_id == tenant_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update user.

    Args:
        user_id: User ID
        user_update: Update data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated user
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(User).where(
        and_(User.id == user_id, User.tenant_id == tenant_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete user.

    Args:
        user_id: User ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(User).where(
        and_(User.id == user_id, User.tenant_id == tenant_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await session.delete(user)
    await session.commit()

    return {"message": "User deleted successfully"}


@router.post("/{user_id}/roles", response_model=UserResponse)
async def assign_role(
    user_id: str,
    role_assignment: UserRoleAssignment,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Assign role to user.

    Args:
        user_id: User ID
        role_assignment: Role and optional engagement scope
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated user

    Raises:
        HTTPException: If user or role not found
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(User).where(
        and_(User.id == user_id, User.tenant_id == tenant_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stmt = select(Role).where(Role.id == role_assignment.role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    user_role = UserRole(
        user_id=user_id,
        role_id=role_assignment.role_id,
        engagement_id=role_assignment.engagement_id,
    )
    session.add(user_role)
    await session.commit()

    return user
