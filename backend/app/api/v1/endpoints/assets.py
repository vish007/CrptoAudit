"""Asset management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.asset import CryptoAsset, WalletAddress
from app.schemas.asset import (
    CryptoAssetResponse,
    CryptoAssetCreate,
    WalletAddressResponse,
    WalletAddressCreate,
    BalanceVerificationRequest,
    BalanceVerificationResponse,
)

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("", response_model=CryptoAssetResponse)
async def create_crypto_asset(
    asset_create: CryptoAssetCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create new crypto asset.

    Args:
        asset_create: Asset creation data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created asset
    """
    user_id = current_user.get("sub")

    # Check if asset already exists
    stmt = select(CryptoAsset).where(CryptoAsset.symbol == asset_create.symbol)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset with this symbol already exists",
        )

    asset = CryptoAsset(
        symbol=asset_create.symbol,
        name=asset_create.name,
        asset_type=asset_create.asset_type,
        blockchains_json=asset_create.blockchains_json or [],
        contract_addresses_json=asset_create.contract_addresses_json or {},
        decimals=asset_create.decimals,
        is_active=True,
        created_by=user_id,
    )

    session.add(asset)
    await session.commit()
    await session.refresh(asset)

    return asset


@router.get("", response_model=List[CryptoAssetResponse])
async def list_crypto_assets(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    asset_type: str = Query(None),
    is_active: bool = Query(True),
):
    """
    List crypto assets.

    Args:
        session: Database session
        skip: Number of records to skip
        limit: Max records to return
        asset_type: Filter by asset type
        is_active: Filter by active status

    Returns:
        List of assets
    """
    query = select(CryptoAsset).where(CryptoAsset.is_active == is_active)

    if asset_type:
        query = query.where(CryptoAsset.asset_type == asset_type)

    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    assets = result.scalars().all()

    return assets


@router.get("/{asset_id}", response_model=CryptoAssetResponse)
async def get_crypto_asset(
    asset_id: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Get crypto asset by ID.

    Args:
        asset_id: Asset ID
        session: Database session

    Returns:
        Asset details

    Raises:
        HTTPException: If asset not found
    """
    stmt = select(CryptoAsset).where(CryptoAsset.id == asset_id)
    result = await session.execute(stmt)
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return asset


@router.get("/{asset_id}/wallets", response_model=List[WalletAddressResponse])
async def list_asset_wallets(
    asset_id: str,
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    List wallets holding an asset.

    Args:
        asset_id: Asset ID
        engagement_id: Engagement ID filter
        current_user: Current authenticated user
        session: Database session

    Returns:
        List of wallet addresses
    """
    tenant_id = extract_tenant_id(current_user)

    # Verify engagement access
    from app.models.engagement import Engagement
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

    stmt = select(WalletAddress).where(
        and_(
            WalletAddress.asset_id == asset_id,
            WalletAddress.engagement_id == engagement_id,
        )
    )
    result = await session.execute(stmt)
    wallets = result.scalars().all()

    return wallets


@router.post("/{asset_id}/wallets", response_model=WalletAddressResponse)
async def add_wallet_address(
    asset_id: str,
    engagement_id: str,
    wallet_create: WalletAddressCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Add wallet address for asset.

    Args:
        asset_id: Asset ID
        engagement_id: Engagement ID
        wallet_create: Wallet creation data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created wallet address
    """
    tenant_id = extract_tenant_id(current_user)
    user_id = current_user.get("sub")

    # Verify engagement access
    from app.models.engagement import Engagement
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
            detail="Only auditor can add wallets",
        )

    wallet = WalletAddress(
        engagement_id=engagement_id,
        asset_id=asset_id,
        address=wallet_create.address,
        blockchain=wallet_create.blockchain,
        custody_type=wallet_create.custody_type,
        custodian_name=wallet_create.custodian_name,
        wallet_type=wallet_create.wallet_type,
        created_by=user_id,
    )

    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)

    return wallet


@router.post("/{asset_id}/verify-balance", response_model=BalanceVerificationResponse)
async def verify_asset_balance(
    asset_id: str,
    verification_request: BalanceVerificationRequest,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Verify asset balance on blockchain.

    Args:
        asset_id: Asset ID
        verification_request: Address and blockchain info
        current_user: Current authenticated user
        session: Database session

    Returns:
        Verification result

    Raises:
        HTTPException: If verification fails
    """
    from datetime import datetime, timezone

    # In production, this would call actual blockchain APIs
    # For now, return mock data
    return BalanceVerificationResponse(
        address=verification_request.wallet_address,
        blockchain=verification_request.blockchain,
        asset=verification_request.asset_symbol,
        verified_balance=0,
        block_height="0",
        verified_at=datetime.now(timezone.utc),
        status="PENDING",
    )


@router.post("/bulk-import")
async def bulk_import_assets(
    assets: List[CryptoAssetCreate],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Bulk import crypto assets.

    Args:
        assets: List of assets to import
        current_user: Current authenticated user
        session: Database session

    Returns:
        Import results
    """
    user_id = current_user.get("sub")
    imported_count = 0
    failed_count = 0
    errors = []

    for asset_data in assets:
        try:
            # Check if already exists
            stmt = select(CryptoAsset).where(CryptoAsset.symbol == asset_data.symbol)
            result = await session.execute(stmt)
            if result.scalar_one_or_none():
                failed_count += 1
                errors.append(
                    {
                        "symbol": asset_data.symbol,
                        "error": "Asset already exists",
                    }
                )
                continue

            asset = CryptoAsset(
                symbol=asset_data.symbol,
                name=asset_data.name,
                asset_type=asset_data.asset_type,
                blockchains_json=asset_data.blockchains_json or [],
                contract_addresses_json=asset_data.contract_addresses_json or {},
                decimals=asset_data.decimals,
                is_active=True,
                created_by=user_id,
            )
            session.add(asset)
            imported_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(
                {
                    "symbol": asset_data.symbol,
                    "error": str(e),
                }
            )

    await session.commit()

    return {
        "imported_count": imported_count,
        "failed_count": failed_count,
        "errors": errors,
    }
