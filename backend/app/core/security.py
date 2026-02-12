"""
Security utilities for authentication, authorization, and token management.
Includes password hashing, JWT token operations, and permission decorators.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from functools import wraps

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp

from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)

# HTTP Bearer security scheme
security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: The plaintext password to hash

    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: The plaintext password
        hashed_password: The hashed password to verify against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode
        expires_delta: Optional custom expiration delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Dependency to extract and verify current user from Bearer token.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        User claims from token

    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )

    return payload


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Dependency to ensure user is active.

    Args:
        current_user: Current user from token

    Returns:
        Current user data

    Raises:
        HTTPException: If user is not active
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return current_user


def require_permission(resource: str, action: str):
    """
    Decorator to require specific resource and action permissions.

    Args:
        resource: The resource being accessed
        action: The action being performed (read, write, delete, etc.)

    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(
            current_user: Dict[str, Any] = Depends(get_current_active_user),
            *args,
            **kwargs
        ):
            # Check if user is superadmin (bypass all checks)
            if current_user.get("is_superadmin", False):
                return await func(current_user=current_user, *args, **kwargs)

            # Check if user has required permission
            user_permissions = current_user.get("permissions", [])
            required_permission = f"{resource}:{action}"

            if required_permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {required_permission}",
                )

            return await func(current_user=current_user, *args, **kwargs)

        return wrapper
    return decorator


def verify_api_key(api_key: str) -> bool:
    """
    Verify an API key.

    Args:
        api_key: The API key to verify

    Returns:
        True if valid, False otherwise
    """
    # This would typically check against a database of valid API keys
    # For now, returns False as a placeholder
    return False


def setup_mfa_secret(email: str) -> str:
    """
    Generate a new MFA secret for a user.

    Args:
        email: User's email address

    Returns:
        Base32 encoded secret and provisioning URI
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=email,
        issuer_name=settings.MFA_ISSUER,
    )

    return secret, provisioning_uri


def verify_mfa_token(secret: str, token: str) -> bool:
    """
    Verify an MFA token against a secret.

    Args:
        secret: The MFA secret
        token: The 6-digit token to verify

    Returns:
        True if token is valid, False otherwise
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)


def extract_tenant_id(current_user: Dict[str, Any]) -> str:
    """
    Extract tenant ID from current user claims.

    Args:
        current_user: Current user claims

    Returns:
        Tenant ID

    Raises:
        HTTPException: If tenant_id not found
    """
    tenant_id = current_user.get("tenant_id")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no associated tenant",
        )
    return tenant_id


def extract_user_id(current_user: Dict[str, Any]) -> str:
    """
    Extract user ID from current user claims.

    Args:
        current_user: Current user claims

    Returns:
        User ID

    Raises:
        HTTPException: If user_id not found
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user token",
        )
    return user_id
