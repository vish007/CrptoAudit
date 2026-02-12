"""Pydantic schemas for asset and reserve operations."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class CryptoAssetBase(BaseModel):
    """Base crypto asset schema."""

    symbol: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    asset_type: str = Field(..., pattern="^(COIN|TOKEN|STABLECOIN|NFT)$")
    blockchains_json: Optional[List[str]] = []
    contract_addresses_json: Optional[Dict[str, Any]] = {}
    decimals: int = Field(default=18, ge=0, le=30)


class CryptoAssetCreate(CryptoAssetBase):
    """Create crypto asset request."""

    pass


class CryptoAssetResponse(CryptoAssetBase):
    """Crypto asset response."""

    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WalletAddressBase(BaseModel):
    """Base wallet address schema."""

    address: str = Field(..., min_length=1, max_length=255)
    blockchain: str = Field(..., min_length=1, max_length=50)
    custody_type: str = Field(
        ...,
        pattern="^(SELF_CUSTODY|THIRD_PARTY_CUSTODIAN|DEFI_CONTRACT)$",
    )
    custodian_name: Optional[str] = None
    wallet_type: str = Field(..., pattern="^(HOT|WARM|COLD|HARDWARE|MPC)$")


class WalletAddressCreate(WalletAddressBase):
    """Create wallet address request."""

    asset_id: Optional[str] = None


class WalletAddressResponse(WalletAddressBase):
    """Wallet address response."""

    id: str
    engagement_id: str
    asset_id: Optional[str]
    verified_at: Optional[datetime]
    control_verified: bool
    control_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssetBalanceBase(BaseModel):
    """Base asset balance schema."""

    reported_balance: Decimal = Field(..., decimal_places=18)
    verified_balance: Optional[Decimal] = None
    verification_method: Optional[str] = None


class AssetBalanceCreate(AssetBalanceBase):
    """Create asset balance request."""

    asset_id: str
    wallet_id: str


class AssetBalanceResponse(AssetBalanceBase):
    """Asset balance response."""

    id: str
    engagement_id: str
    asset_id: str
    wallet_id: str
    verified_at: Optional[datetime]
    status: str
    block_height: Optional[str]
    tx_hash: Optional[str]
    variance_pct: Optional[Decimal]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerLiabilityBase(BaseModel):
    """Base customer liability schema."""

    anonymized_user_id: str
    balance: Decimal = Field(..., decimal_places=18)
    account_type: str = Field(..., pattern="^(SPOT|MARGIN|EARN|STAKING)$")


class CustomerLiabilityCreate(CustomerLiabilityBase):
    """Create customer liability request."""

    asset_id: str


class CustomerLiabilityResponse(CustomerLiabilityBase):
    """Customer liability response."""

    id: str
    engagement_id: str
    asset_id: str
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReserveRatioBase(BaseModel):
    """Base reserve ratio schema."""

    total_assets: Decimal = Field(..., decimal_places=18)
    total_liabilities: Decimal = Field(..., decimal_places=18)
    ratio_percentage: Decimal = Field(..., decimal_places=4)
    meets_vara_requirement: bool
    verification_notes: Optional[str] = None


class ReserveRatioResponse(ReserveRatioBase):
    """Reserve ratio response."""

    id: str
    engagement_id: str
    asset_id: str
    calculated_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DeFiPositionBase(BaseModel):
    """Base DeFi position schema."""

    protocol_name: str = Field(..., min_length=1, max_length=255)
    contract_address: str = Field(..., min_length=1, max_length=255)
    blockchain: str = Field(..., min_length=1, max_length=50)
    position_type: str
    principal: Decimal = Field(..., decimal_places=18)
    rewards: Decimal = Field(default=Decimal(0), decimal_places=18)
    lock_status: Optional[str] = None
    risk_score: Optional[Decimal] = Field(None, decimal_places=2)


class DeFiPositionCreate(DeFiPositionBase):
    """Create DeFi position request."""

    asset_id: str


class DeFiPositionResponse(DeFiPositionBase):
    """DeFi position response."""

    id: str
    engagement_id: str
    asset_id: str
    lock_end_date: Optional[datetime]
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReconciliationRecordBase(BaseModel):
    """Base reconciliation record schema."""

    date: datetime
    opening_balance: Decimal = Field(..., decimal_places=18)
    closing_balance: Decimal = Field(..., decimal_places=18)
    notes: Optional[str] = None


class ReconciliationRecordCreate(ReconciliationRecordBase):
    """Create reconciliation record request."""

    asset_id: str


class ReconciliationRecordResponse(ReconciliationRecordBase):
    """Reconciliation record response."""

    id: str
    engagement_id: str
    asset_id: str
    variance: Decimal
    variance_pct: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BalanceVerificationRequest(BaseModel):
    """Verify balance request."""

    wallet_address: str
    blockchain: str
    asset_symbol: str


class BalanceVerificationResponse(BaseModel):
    """Balance verification response."""

    address: str
    blockchain: str
    asset: str
    verified_balance: Decimal
    block_height: str
    verified_at: datetime
    status: str


class ReserveSummaryResponse(BaseModel):
    """Reserve summary response."""

    engagement_id: str
    total_assets_usd: float
    total_liabilities_usd: float
    overall_ratio_pct: float
    meets_requirement: bool
    by_asset: List[ReserveRatioResponse]
    last_updated: datetime
