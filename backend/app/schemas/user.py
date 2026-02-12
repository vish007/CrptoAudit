"""Pydantic schemas for user, tenant, and role operations."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TenantBase(BaseModel):
    """Base tenant schema."""

    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., pattern="^(AUDITOR|VASP|REGULATOR|CUSTOMER)$")
    vara_license_number: Optional[str] = None
    settings_json: Optional[Dict[str, Any]] = {}


class TenantCreate(TenantBase):
    """Create tenant request."""

    pass


class TenantUpdate(BaseModel):
    """Update tenant request."""

    name: Optional[str] = None
    settings_json: Optional[Dict[str, Any]] = None


class TenantResponse(TenantBase):
    """Tenant response."""

    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    """Base permission schema."""

    resource: str = Field(..., min_length=1, max_length=100)
    action: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    field_restrictions_json: Optional[Dict[str, Any]] = {}


class PermissionCreate(PermissionBase):
    """Create permission request."""

    pass


class PermissionResponse(PermissionBase):
    """Permission response."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """Base role schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    permissions_json: Optional[List[str]] = []


class RoleCreate(RoleBase):
    """Create role request."""

    pass


class RoleUpdate(BaseModel):
    """Update role request."""

    name: Optional[str] = None
    description: Optional[str] = None
    permissions_json: Optional[List[str]] = None


class RoleResponse(RoleBase):
    """Role response."""

    id: str
    is_system_role: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Create user request."""

    password: str = Field(..., min_length=12)
    tenant_id: str


class UserUpdate(BaseModel):
    """Update user request."""

    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserChangePassword(BaseModel):
    """Change password request."""

    current_password: str
    new_password: str = Field(..., min_length=12)


class UserResponse(UserBase):
    """User response."""

    id: str
    is_active: bool
    is_superadmin: bool
    mfa_enabled: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """User detail response with roles."""

    roles: List[RoleResponse] = []
    tenant: TenantResponse


class LoginRequest(BaseModel):
    """Login request."""

    email: EmailStr
    password: str
    mfa_token: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class MFASetupResponse(BaseModel):
    """MFA setup response."""

    secret: str
    provisioning_uri: str
    qr_code_url: str


class MFAVerifyRequest(BaseModel):
    """MFA verify request."""

    token: str = Field(..., min_length=6, max_length=6)


class UserRoleAssignment(BaseModel):
    """Assign role to user."""

    role_id: str
    engagement_id: Optional[str] = None


class AuditLogResponse(BaseModel):
    """Audit log response."""

    id: str
    user_id: Optional[str]
    action: str
    resource: str
    resource_id: str
    old_value: Optional[str]
    new_value: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
