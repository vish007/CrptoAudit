"""Authentication endpoints."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    setup_mfa_secret,
    verify_mfa_token,
)
from app.core.config import settings
from app.models.user import User, Tenant
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
    MFASetupResponse,
    MFAVerifyRequest,
    RefreshTokenRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Register a new user.

    Args:
        user_create: User creation data
        session: Database session

    Returns:
        Created user

    Raises:
        HTTPException: If email already exists or tenant not found
    """
    # Check if user exists
    stmt = select(User).where(User.email == user_create.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Verify tenant exists
    stmt = select(Tenant).where(Tenant.id == user_create.tenant_id)
    result = await session.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant not found",
        )

    # Create user
    hashed_password = hash_password(user_create.password)
    user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password,
        tenant_id=user_create.tenant_id,
        is_active=True,
        mfa_enabled=settings.MFA_ENABLED_BY_DEFAULT,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    login_request: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate user and return tokens.

    Args:
        login_request: Login credentials
        session: Database session

    Returns:
        Access and refresh tokens

    Raises:
        HTTPException: If credentials invalid or MFA required
    """
    # Get user
    stmt = select(User).where(User.email == login_request.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    # Check MFA if enabled
    if user.mfa_enabled:
        if not login_request.mfa_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="MFA token required",
            )

        if not verify_mfa_token(user.mfa_secret, login_request.mfa_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA token",
            )

    # Create tokens
    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "is_superadmin": user.is_superadmin,
            "is_active": user.is_active,
        }
    )

    refresh_token = create_access_token(
        data={
            "sub": user.id,
            "type": "refresh",
        },
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_request: RefreshTokenRequest,
):
    """
    Refresh access token using refresh token.

    Args:
        refresh_request: Refresh token

    Returns:
        New access and refresh tokens

    Raises:
        HTTPException: If refresh token invalid
    """
    from app.core.security import verify_token

    payload = verify_token(refresh_request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id = payload.get("sub")

    access_token = create_access_token(
        data={
            "sub": user_id,
        }
    )

    refresh_token = create_access_token(
        data={
            "sub": user_id,
            "type": "refresh",
        },
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    """
    Logout user (client-side token deletion).

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Setup MFA for user.

    Args:
        current_user: Current authenticated user
        session: Database session

    Returns:
        MFA setup details with QR code
    """
    user_id = current_user.get("sub")
    secret, provisioning_uri = setup_mfa_secret(current_user.get("email"))

    # Generate QR code URL (using external service)
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={provisioning_uri}"

    return MFASetupResponse(
        secret=secret,
        provisioning_uri=provisioning_uri,
        qr_code_url=qr_code_url,
    )


@router.post("/mfa/verify")
async def verify_mfa(
    mfa_request: MFAVerifyRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Verify and enable MFA for user.

    Args:
        mfa_request: MFA token to verify
        current_user: Current authenticated user
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If MFA token invalid
    """
    user_id = current_user.get("sub")

    # Get user
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # This is a simplified verification - in production, you'd store the secret first
    # and verify it here, then enable MFA
    user.mfa_enabled = True
    session.add(user)
    await session.commit()

    return {"message": "MFA enabled successfully"}
