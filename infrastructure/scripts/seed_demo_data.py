#!/usr/bin/env python3
"""
Demo data seeding script for SimplyFI POR Platform.

This script creates demo data for testing and development:
- Demo tenants and users
- Demo engagements
- Demo wallets and asset balances
- Demo customer liabilities
- Demo Merkle trees
- Demo reconciliation records
- Demo reserve ratios
"""
import asyncio
import logging
import sys
import random
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, '/app')

from app.core.config import settings
from app.models import (
    Tenant,
    User,
    UserRole,
    Role,
    Engagement,
    EngagementAsset,
    EngagementTimeline,
    WalletAddress,
    AssetBalance,
    CustomerLiability,
    ReserveRatio,
    ReconciliationRecord,
    MerkleTree,
    MerkleLeaf,
    CryptoAsset,
)
from app.core.security import get_password_hash

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def seed_demo_data():
    """Seed database with demo data."""
    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True,
        )

        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            # Create demo tenants
            logger.info("Creating demo tenants...")

            # Auditor tenant
            auditor_tenant = Tenant(
                name="SimplyFI Auditor",
                slug="simplyfi-auditor",
                description="Demo auditor firm",
                is_active=True,
            )
            session.add(auditor_tenant)
            await session.flush()

            # VASP tenant
            vasp_tenant = Tenant(
                name="Demo VASP Exchange",
                slug="demo-vasp-exchange",
                description="Demo crypto exchange",
                is_active=True,
            )
            session.add(vasp_tenant)
            await session.flush()

            logger.info(f"Tenants created: {auditor_tenant.name}, {vasp_tenant.name}")

            # Fetch roles
            from sqlalchemy import select
            role_stmt = select(Role).where(Role.slug.in_([
                "auditor", "vasp_admin", "vasp_finance", "customer"
            ]))
            role_result = await session.execute(role_stmt)
            roles_dict = {r.slug: r for r in role_result.scalars()}

            # Create demo users for auditor tenant
            logger.info("Creating demo users...")

            auditor_user = User(
                email="auditor@simplyfi.com",
                username="auditor",
                first_name="John",
                last_name="Auditor",
                hashed_password=get_password_hash("Demo123!@"),
                is_active=True,
                is_verified=True,
                tenant_id=auditor_tenant.id,
            )
            session.add(auditor_user)
            await session.flush()

            user_role = UserRole(
                user_id=auditor_user.id,
                role_id=roles_dict["auditor"].id,
                tenant_id=auditor_tenant.id,
            )
            session.add(user_role)

            # Create demo users for VASP tenant
            vasp_admin = User(
                email="admin@vasp.com",
                username="vasp_admin",
                first_name="Alice",
                last_name="Admin",
                hashed_password=get_password_hash("Demo123!@"),
                is_active=True,
                is_verified=True,
                tenant_id=vasp_tenant.id,
            )
            session.add(vasp_admin)
            await session.flush()

            user_role = UserRole(
                user_id=vasp_admin.id,
                role_id=roles_dict["vasp_admin"].id,
                tenant_id=vasp_tenant.id,
            )
            session.add(user_role)

            vasp_finance = User(
                email="finance@vasp.com",
                username="vasp_finance",
                first_name="Bob",
                last_name="Finance",
                hashed_password=get_password_hash("Demo123!@"),
                is_active=True,
                is_verified=True,
                tenant_id=vasp_tenant.id,
            )
            session.add(vasp_finance)
            await session.flush()

            user_role = UserRole(
                user_id=vasp_finance.id,
                role_id=roles_dict["vasp_finance"].id,
                tenant_id=vasp_tenant.id,
            )
            session.add(user_role)

            logger.info("Demo users created")

            # Create demo engagement
            logger.info("Creating demo engagement...")

            engagement = Engagement(
                name="Demo Exchange - Monthly Audit",
                description="Q1 2024 Proof of Reserves Audit",
                tenant_id=vasp_tenant.id,
                admin_id=vasp_admin.id,
                auditor_id=auditor_user.id,
                status="active",
                engagement_type="monthly",
                start_date=datetime.utcnow() - timedelta(days=30),
                end_date=datetime.utcnow() + timedelta(days=30),
            )
            session.add(engagement)
            await session.flush()

            # Get supported assets
            asset_stmt = select(CryptoAsset).where(
                CryptoAsset.symbol.in_(["BTC", "ETH", "USDT", "USDC"])
            )
            asset_result = await session.execute(asset_stmt)
            assets = asset_result.scalars().all()

            # Create engagement assets
            for asset in assets:
                eng_asset = EngagementAsset(
                    engagement_id=engagement.id,
                    asset_symbol=asset.symbol,
                    blockchain=asset.blockchain,
                    is_included=True,
                )
                session.add(eng_asset)

            # Create engagement timeline
            timeline = EngagementTimeline(
                engagement_id=engagement.id,
                phase="verification",
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=10),
                description="Wallet verification phase",
            )
            session.add(timeline)

            await session.flush()
            logger.info(f"Demo engagement created: {engagement.name}")

            # Create demo wallets
            logger.info("Creating demo wallets...")

            demo_wallets = [
                ("0x742d35Cc6634C0532925a3b844Bc9e7595f42bE7", "ethereum", "BTC"),
                ("0x8ba1f109551bD432803012645Ac136ddd64DBA72", "ethereum", "ETH"),
                ("0x1234567890123456789012345678901234567890", "ethereum", "USDT"),
                ("0x0987654321098765432109876543210987654321", "ethereum", "USDC"),
                ("3Nxwenay9Z8Lc9JBieeRqNSWXWAixpmEFv", "bitcoin", "BTC"),
            ]

            wallets = []
            for address, blockchain, asset_symbol in demo_wallets:
                wallet = WalletAddress(
                    engagement_id=engagement.id,
                    address=address,
                    blockchain=blockchain,
                    asset_symbol=asset_symbol,
                    description=f"Demo {blockchain} {asset_symbol} wallet",
                    is_verified=True,
                )
                session.add(wallet)
                wallets.append(wallet)

            await session.flush()
            logger.info(f"Created {len(wallets)} demo wallets")

            # Create asset balances
            logger.info("Creating asset balances...")

            balance_amounts = {
                "BTC": random.uniform(5, 50),
                "ETH": random.uniform(50, 500),
                "USDT": random.uniform(100000, 500000),
                "USDC": random.uniform(100000, 500000),
            }

            for wallet in wallets:
                balance = AssetBalance(
                    wallet_id=wallet.id,
                    asset_symbol=wallet.asset_symbol,
                    blockchain=wallet.blockchain,
                    on_chain_balance=balance_amounts.get(wallet.asset_symbol, 0),
                    off_chain_balance=0,
                    last_verified_at=datetime.utcnow(),
                    verification_status="verified",
                )
                session.add(balance)

            logger.info("Asset balances created")

            # Create demo customer liabilities
            logger.info("Creating demo customer liabilities...")

            customer_assets = ["BTC", "ETH", "USDT", "USDC"]

            for customer_id in range(1, 101):  # 100 customers
                for asset in customer_assets:
                    liability = CustomerLiability(
                        engagement_id=engagement.id,
                        customer_id=customer_id,
                        asset_symbol=asset,
                        amount=balance_amounts.get(asset, 0) / 100,
                        recorded_date=datetime.utcnow().date(),
                    )
                    session.add(liability)

            logger.info("Customer liabilities created (100 customers, 4 assets each)")

            # Create demo Merkle tree
            logger.info("Creating demo Merkle tree...")

            merkle_tree = MerkleTree(
                engagement_id=engagement.id,
                num_leaves=100,
                tree_depth=7,
                root_hash="0x" + "a" * 64,  # Demo hash
                created_at=datetime.utcnow(),
            )
            session.add(merkle_tree)
            await session.flush()

            # Create Merkle leaves
            for i in range(100):
                leaf = MerkleLeaf(
                    merkle_tree_id=merkle_tree.id,
                    customer_id=i + 1,
                    liability_amount=random.uniform(1, 100),
                    leaf_hash="0x" + str(uuid4().hex[:64]),
                    leaf_index=i,
                )
                session.add(leaf)

            logger.info("Merkle tree created with 100 leaves")

            # Create demo reserve ratios (30 days)
            logger.info("Creating demo reserve ratios...")

            total_assets = sum(balance_amounts.values())
            total_liabilities = total_assets / 1.2  # 120% reserve ratio

            for days_ago in range(30):
                record_date = (datetime.utcnow() - timedelta(days=days_ago)).date()

                # Daily variation
                assets_variation = total_assets * random.uniform(0.98, 1.02)
                liabilities_variation = total_liabilities * random.uniform(0.99, 1.01)
                ratio = assets_variation / liabilities_variation if liabilities_variation > 0 else 1

                reserve_ratio = ReserveRatio(
                    engagement_id=engagement.id,
                    recorded_date=record_date,
                    total_assets=assets_variation,
                    total_liabilities=liabilities_variation,
                    ratio=ratio,
                )
                session.add(reserve_ratio)

            logger.info("30 days of reserve ratio records created")

            # Create demo reconciliation records (30 days)
            logger.info("Creating demo reconciliation records...")

            for days_ago in range(30):
                record_date = (datetime.utcnow() - timedelta(days=days_ago)).date()

                assets_variation = total_assets * random.uniform(0.98, 1.02)
                liabilities_variation = total_liabilities * random.uniform(0.99, 1.01)
                ratio = assets_variation / liabilities_variation if liabilities_variation > 0 else 1

                reconciliation = ReconciliationRecord(
                    engagement_id=engagement.id,
                    recorded_date=record_date,
                    total_assets=assets_variation,
                    total_liabilities=liabilities_variation,
                    reserve_ratio=ratio,
                    status="completed",
                    reconciliation_notes=f"Automated daily reconciliation",
                )
                session.add(reconciliation)

            logger.info("30 days of reconciliation records created")

            # Commit all changes
            await session.commit()
            logger.info("=" * 60)
            logger.info("DEMO DATA SEEDING COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info("\nDemo Login Credentials:")
            logger.info("  Auditor: auditor@simplyfi.com / Demo123!@")
            logger.info("  VASP Admin: admin@vasp.com / Demo123!@")
            logger.info("  VASP Finance: finance@vasp.com / Demo123!@")
            logger.info("\nDemo Data Created:")
            logger.info(f"  - 2 Tenants")
            logger.info(f"  - 3 Demo Users")
            logger.info(f"  - 1 Engagement")
            logger.info(f"  - 5 Wallets")
            logger.info(f"  - 100 Customers with 4 assets each")
            logger.info(f"  - 1 Merkle Tree with 100 leaves")
            logger.info(f"  - 30 days of Reserve Ratio records")
            logger.info(f"  - 30 days of Reconciliation records")
            logger.info("=" * 60)

        await engine.dispose()

    except Exception as e:
        logger.error(f"Demo data seeding failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
