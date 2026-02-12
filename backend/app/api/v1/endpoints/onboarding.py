"""Onboarding endpoints for new VASPs."""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.user import Tenant
from app.models.engagement import Engagement, EngagementAsset
from app.models.asset import WalletAddress, CustomerLiability, CryptoAsset
from app.schemas.engagement import BulkAssetImportResponse
from app.schemas.asset import WalletAddressCreate, CustomerLiabilityCreate

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("/vasp")
async def register_vasp(
    vasp_data: Dict[str, Any],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Register new VASP (Virtual Asset Service Provider).

    Args:
        vasp_data: VASP registration data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Created VASP tenant
    """
    user_id = current_user.get("sub")

    # Check superadmin access for onboarding
    if not current_user.get("is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can onboard VASPs",
        )

    tenant = Tenant(
        name=vasp_data.get("name"),
        type="VASP",
        vara_license_number=vasp_data.get("vara_license_number"),
        status="ACTIVE",
        settings_json=vasp_data.get("settings", {}),
        created_by=user_id,
    )

    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return {
        "id": tenant.id,
        "name": tenant.name,
        "type": tenant.type,
        "vara_license_number": tenant.vara_license_number,
        "status": tenant.status,
        "created_at": tenant.created_at,
    }


@router.post("/{engagement_id}/import-assets", response_model=BulkAssetImportResponse)
async def import_assets(
    engagement_id: str,
    assets: List[Dict[str, Any]],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Bulk import crypto assets for engagement.

    Args:
        engagement_id: Engagement ID
        assets: List of assets
        current_user: Current authenticated user
        session: Database session

    Returns:
        Import results
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
            detail="Only auditor can import assets",
        )

    imported_count = 0
    failed_count = 0
    errors = []

    for asset_data in assets:
        try:
            # Get or create crypto asset
            stmt = select(CryptoAsset).where(
                CryptoAsset.symbol == asset_data.get("symbol")
            )
            result = await session.execute(stmt)
            crypto_asset = result.scalar_one_or_none()

            if not crypto_asset:
                crypto_asset = CryptoAsset(
                    symbol=asset_data.get("symbol"),
                    name=asset_data.get("name"),
                    asset_type=asset_data.get("asset_type", "COIN"),
                    blockchains_json=asset_data.get("blockchains", []),
                    contract_addresses_json=asset_data.get("contract_addresses", {}),
                    decimals=asset_data.get("decimals", 18),
                    is_active=True,
                    created_by=user_id,
                )
                session.add(crypto_asset)
                await session.flush()

            # Create engagement asset
            eng_asset = EngagementAsset(
                engagement_id=engagement_id,
                asset_symbol=asset_data.get("symbol"),
                asset_name=asset_data.get("name"),
                tier=asset_data.get("tier", 1),
                contract_addresses_json=asset_data.get("contract_addresses", {}),
                blockchains_json=asset_data.get("blockchains", []),
                created_by=user_id,
            )
            session.add(eng_asset)
            imported_count += 1

        except Exception as e:
            failed_count += 1
            errors.append(
                {
                    "symbol": asset_data.get("symbol"),
                    "error": str(e),
                }
            )

    engagement.asset_count = imported_count
    session.add(engagement)
    await session.commit()

    return BulkAssetImportResponse(
        imported_count=imported_count,
        failed_count=failed_count,
        errors=errors,
    )


@router.post("/{engagement_id}/import-wallets")
async def import_wallets(
    engagement_id: str,
    wallets: List[Dict[str, Any]],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Bulk import wallet addresses for engagement.

    Args:
        engagement_id: Engagement ID
        wallets: List of wallet data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Import results
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
            detail="Only auditor can import wallets",
        )

    imported_count = 0
    failed_count = 0
    errors = []

    for wallet_data in wallets:
        try:
            # Get asset
            stmt = select(CryptoAsset).where(
                CryptoAsset.symbol == wallet_data.get("asset_symbol")
            )
            result = await session.execute(stmt)
            asset = result.scalar_one_or_none()

            if not asset:
                failed_count += 1
                errors.append(
                    {
                        "address": wallet_data.get("address"),
                        "error": "Asset not found",
                    }
                )
                continue

            wallet = WalletAddress(
                engagement_id=engagement_id,
                asset_id=asset.id,
                address=wallet_data.get("address"),
                blockchain=wallet_data.get("blockchain"),
                custody_type=wallet_data.get("custody_type", "THIRD_PARTY_CUSTODIAN"),
                custodian_name=wallet_data.get("custodian_name"),
                wallet_type=wallet_data.get("wallet_type", "COLD"),
                created_by=user_id,
            )
            session.add(wallet)
            imported_count += 1

        except Exception as e:
            failed_count += 1
            errors.append(
                {
                    "address": wallet_data.get("address"),
                    "error": str(e),
                }
            )

    await session.commit()

    return {
        "imported_count": imported_count,
        "failed_count": failed_count,
        "errors": errors,
    }


@router.post("/{engagement_id}/import-liabilities")
async def import_liabilities(
    engagement_id: str,
    liabilities: List[Dict[str, Any]],
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Bulk import customer liabilities.

    Args:
        engagement_id: Engagement ID
        liabilities: List of liability data
        current_user: Current authenticated user
        session: Database session

    Returns:
        Import results
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
            detail="Only auditor can import liabilities",
        )

    imported_count = 0
    failed_count = 0
    errors = []

    for liability_data in liabilities:
        try:
            # Get asset
            stmt = select(CryptoAsset).where(
                CryptoAsset.symbol == liability_data.get("asset_symbol")
            )
            result = await session.execute(stmt)
            asset = result.scalar_one_or_none()

            if not asset:
                failed_count += 1
                errors.append(
                    {
                        "user_id": liability_data.get("anonymized_user_id"),
                        "error": "Asset not found",
                    }
                )
                continue

            from decimal import Decimal
            liability = CustomerLiability(
                engagement_id=engagement_id,
                asset_id=asset.id,
                anonymized_user_id=liability_data.get("anonymized_user_id"),
                balance=Decimal(str(liability_data.get("balance", 0))),
                account_type=liability_data.get("account_type", "SPOT"),
                created_by=user_id,
            )
            session.add(liability)
            imported_count += 1

        except Exception as e:
            failed_count += 1
            errors.append(
                {
                    "user_id": liability_data.get("anonymized_user_id"),
                    "error": str(e),
                }
            )

    await session.commit()

    return {
        "imported_count": imported_count,
        "failed_count": failed_count,
        "errors": errors,
    }


@router.get("/{engagement_id}/status")
async def get_onboarding_status(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get onboarding status for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Onboarding status
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

    from sqlalchemy import func
    from app.models.asset import WalletAddress, CustomerLiability

    stmt = select(func.count()).select_from(EngagementAsset).where(
        EngagementAsset.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    asset_count = result.scalar()

    stmt = select(func.count()).select_from(WalletAddress).where(
        WalletAddress.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    wallet_count = result.scalar()

    stmt = select(func.count()).select_from(CustomerLiability).where(
        CustomerLiability.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    liability_count = result.scalar()

    return {
        "engagement_id": engagement_id,
        "assets_imported": asset_count > 0,
        "assets_count": asset_count,
        "wallets_imported": wallet_count > 0,
        "wallets_count": wallet_count,
        "liabilities_imported": liability_count > 0,
        "liabilities_count": liability_count,
        "onboarding_complete": (
            asset_count > 0 and wallet_count > 0 and liability_count > 0
        ),
    }


@router.post("/{engagement_id}/validate")
async def validate_imported_data(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Validate imported data for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Validation results
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
            detail="Only auditor can validate",
        )

    issues = []
    warnings = []

    # Validate assets exist
    from sqlalchemy import func
    stmt = select(func.count()).select_from(EngagementAsset).where(
        EngagementAsset.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    asset_count = result.scalar()

    if asset_count == 0:
        issues.append("No assets imported")

    # Validate wallets exist
    from app.models.asset import WalletAddress
    stmt = select(func.count()).select_from(WalletAddress).where(
        WalletAddress.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    wallet_count = result.scalar()

    if wallet_count == 0:
        issues.append("No wallets imported")

    # Validate liabilities exist
    from app.models.asset import CustomerLiability
    stmt = select(func.count()).select_from(CustomerLiability).where(
        CustomerLiability.engagement_id == engagement_id
    )
    result = await session.execute(stmt)
    liability_count = result.scalar()

    if liability_count == 0:
        issues.append("No customer liabilities imported")

    if asset_count > 0 and liability_count == 0:
        warnings.append("No customer liabilities - reserve ratio cannot be calculated")

    return {
        "engagement_id": engagement_id,
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "ready_for_verification": len(issues) == 0,
    }
