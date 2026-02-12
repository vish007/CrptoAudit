#!/usr/bin/env python3
"""
Database initialization script for SimplyFI POR Platform.

This script initializes the database with:
- All necessary tables (via SQLAlchemy models)
- Default system roles and permissions
- Default superadmin user
- Supported cryptocurrencies and blockchains
"""
import asyncio
import logging
import sys
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, '/app')

from app.core.config import settings
from app.core.database import Base
from app.models import (
    User,
    Tenant,
    Role,
    Permission,
    UserRole,
    CryptoAsset,
)
from app.core.security import get_password_hash

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def init_database():
    """Initialize the database with schema and seed data."""
    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True,
        )

        # Create all tables
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

        # Create async session
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            # Create default tenant
            logger.info("Creating default tenant...")
            default_tenant = await session.execute(
                "SELECT * FROM tenant WHERE slug = 'simplyfi' LIMIT 1"
            )
            if not default_tenant:
                default_tenant = Tenant(
                    name="SimplyFI",
                    slug="simplyfi",
                    description="Default SimplyFI Auditor Tenant",
                    is_active=True,
                )
                session.add(default_tenant)
                await session.flush()
                logger.info(f"Default tenant created: {default_tenant.name}")

            # Create system roles
            logger.info("Creating system roles...")
            roles_to_create = [
                {
                    "name": "SuperAdmin",
                    "slug": "superadmin",
                    "description": "Super administrator with full access",
                },
                {
                    "name": "Auditor",
                    "slug": "auditor",
                    "description": "Audit firm auditor",
                },
                {
                    "name": "VASPAdmin",
                    "slug": "vasp_admin",
                    "description": "VASP (crypto exchange) administrator",
                },
                {
                    "name": "VASPFinance",
                    "slug": "vasp_finance",
                    "description": "VASP Finance Officer",
                },
                {
                    "name": "VASPCompliance",
                    "slug": "vasp_compliance",
                    "description": "VASP Compliance Officer",
                },
                {
                    "name": "Customer",
                    "slug": "customer",
                    "description": "Customer with read-only access",
                },
                {
                    "name": "Regulator",
                    "slug": "regulator",
                    "description": "Financial regulator",
                },
            ]

            roles = {}
            for role_data in roles_to_create:
                role = Role(
                    name=role_data["name"],
                    slug=role_data["slug"],
                    description=role_data["description"],
                    tenant_id=1,  # Assuming first tenant ID is 1
                    is_system_role=True,
                )
                session.add(role)
                await session.flush()
                roles[role_data["slug"]] = role
                logger.info(f"Role created: {role.name}")

            # Create permissions
            logger.info("Creating system permissions...")
            permissions_list = [
                # User management
                ("users:create", "Create users"),
                ("users:read", "Read users"),
                ("users:update", "Update users"),
                ("users:delete", "Delete users"),
                # Engagement management
                ("engagements:create", "Create engagements"),
                ("engagements:read", "Read engagements"),
                ("engagements:update", "Update engagements"),
                ("engagements:delete", "Delete engagements"),
                # Report generation
                ("reports:generate", "Generate reports"),
                ("reports:read", "Read reports"),
                ("reports:export", "Export reports"),
                # Asset verification
                ("assets:verify", "Verify assets"),
                ("assets:reconcile", "Reconcile assets"),
                # VARA compliance
                ("compliance:read", "Read compliance data"),
                ("compliance:audit", "Audit compliance"),
                # Admin functions
                ("admin:settings", "Manage system settings"),
                ("admin:tenants", "Manage tenants"),
                ("admin:audit_logs", "View audit logs"),
            ]

            permissions = {}
            for perm_slug, perm_name in permissions_list:
                permission = Permission(
                    slug=perm_slug,
                    name=perm_name,
                    is_system_permission=True,
                )
                session.add(permission)
                await session.flush()
                permissions[perm_slug] = permission
                logger.info(f"Permission created: {perm_slug}")

            # Assign permissions to roles
            logger.info("Assigning permissions to roles...")
            role_permissions = {
                "superadmin": [p for p in permissions.values()],
                "auditor": [
                    permissions["engagements:read"],
                    permissions["assets:verify"],
                    permissions["assets:reconcile"],
                    permissions["reports:generate"],
                    permissions["reports:read"],
                    permissions["reports:export"],
                    permissions["compliance:read"],
                    permissions["compliance:audit"],
                ],
                "vasp_admin": [
                    permissions["engagements:read"],
                    permissions["engagements:update"],
                    permissions["users:create"],
                    permissions["users:read"],
                    permissions["users:update"],
                    permissions["reports:read"],
                ],
                "vasp_finance": [
                    permissions["assets:reconcile"],
                    permissions["reports:read"],
                    permissions["engagements:read"],
                ],
                "vasp_compliance": [
                    permissions["compliance:read"],
                    permissions["reports:read"],
                    permissions["engagements:read"],
                ],
                "customer": [
                    permissions["reports:read"],
                    permissions["engagements:read"],
                ],
                "regulator": [
                    permissions["engagements:read"],
                    permissions["compliance:read"],
                    permissions["reports:read"],
                    permissions["admin:audit_logs"],
                ],
            }

            for role_slug, role_perms in role_permissions.items():
                role = roles[role_slug]
                for perm in role_perms:
                    role.permissions.append(perm)
                logger.info(f"Assigned {len(role_perms)} permissions to {role_slug}")

            # Create default superadmin user
            logger.info("Creating default superadmin user...")
            superadmin = User(
                email="admin@simplyfi.com",
                username="admin",
                first_name="Super",
                last_name="Admin",
                hashed_password=get_password_hash("ChangeMe123!@"),
                is_active=True,
                is_superuser=True,
                is_verified=True,
                tenant_id=1,
                mfa_enabled=False,
            )
            session.add(superadmin)
            await session.flush()

            # Assign superadmin role
            user_role = UserRole(
                user_id=superadmin.id,
                role_id=roles["superadmin"].id,
                tenant_id=1,
            )
            session.add(user_role)
            logger.info("Default superadmin user created: admin@simplyfi.com")
            logger.info("Default password: ChangeMe123!@ (CHANGE ON FIRST LOGIN)")

            # Create supported cryptocurrencies
            logger.info("Creating supported cryptocurrencies...")
            cryptocurrencies = [
                # Top 153 cryptocurrencies - showing top 50
                ("BTC", "Bitcoin", "ethereum", 1, "0x0000000000000000000000000000000000000000"),
                ("ETH", "Ethereum", "ethereum", 18, "0x0000000000000000000000000000000000000000"),
                ("USDT", "Tether", "ethereum", 6, "0xdac17f958d2ee523a2206206994597c13d831ec7"),
                ("USDC", "USD Coin", "ethereum", 6, "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
                ("BNB", "Binance Coin", "bsc", 18, "0x0000000000000000000000000000000000000000"),
                ("XRP", "Ripple", "ripple", 6, "0x0000000000000000000000000000000000000000"),
                ("ADA", "Cardano", "cardano", 6, "0x0000000000000000000000000000000000000000"),
                ("SOL", "Solana", "solana", 9, "0x0000000000000000000000000000000000000000"),
                ("DOGE", "Dogecoin", "dogecoin", 8, "0x0000000000000000000000000000000000000000"),
                ("MATIC", "Polygon", "polygon", 18, "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"),
                ("DOT", "Polkadot", "polkadot", 10, "0x0000000000000000000000000000000000000000"),
                ("LTC", "Litecoin", "litecoin", 8, "0x0000000000000000000000000000000000000000"),
                ("LINK", "Chainlink", "ethereum", 18, "0x514910771af9ca656af840dff83e8264ecf986ca"),
                ("BCH", "Bitcoin Cash", "bitcoincash", 8, "0x0000000000000000000000000000000000000000"),
                ("AVAX", "Avalanche", "avalanche", 18, "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7"),
                ("SHIB", "Shiba Inu", "ethereum", 18, "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"),
                ("CRO", "Cronos", "ethereum", 8, "0xa0b73e1ff0b83f00986d7c38413397583ad33a98"),
                ("UNI", "Uniswap", "ethereum", 18, "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"),
                ("WBTC", "Wrapped Bitcoin", "ethereum", 8, "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"),
                ("ARB", "Arbitrum", "ethereum", 18, "0x912ce59144191c1204e64559fe8253a0e49e8992"),
                ("OP", "Optimism", "ethereum", 18, "0x4200000000000000000000000000000000000042"),
                ("AAVE", "Aave", "ethereum", 18, "0x7fc66500c84a76ad7e9c93437e434122a1aa0fa"),
                ("MKR", "Maker", "ethereum", 18, "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2"),
                ("GRT", "The Graph", "ethereum", 18, "0xc944e90b891c6e269bbb25971a0beb6f4667d305"),
                ("SUSHI", "Sushiswap", "ethereum", 18, "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2"),
                ("LDO", "Lido DAO", "ethereum", 18, "0x5a98fcbea516cf06857215779fd812ca3bef1b32"),
                ("ENS", "Ethereum Name Service", "ethereum", 18, "0xc18360217d8f7ab5e7c516566761ea12ce7f460"),
                ("RPL", "Rocket Pool", "ethereum", 18, "0xd33526068d116ce69f19a9ee46f0bd304f21a51f"),
                ("CVX", "Convex Finance", "ethereum", 18, "0x4e3fbd56cd56c3e3d3c5be140067288297636884"),
                ("CRV", "Curve", "ethereum", 18, "0xd533a949740bb3306d119cc777fa900ba034cd52"),
                ("FXS", "Frax Share", "ethereum", 18, "0x3432b6a60d23ca0dfca7761b7ab56b8a3b680e71"),
                ("BLUR", "Blur", "ethereum", 18, "0x5283d291dbcf85c868b150b3b6fb2820c7eeba4c"),
                ("PEPE", "Pepe", "ethereum", 18, "0x6982508145454ce894acdc3d16e4a07b5e02e1ba"),
                ("DYDX", "dYdX", "ethereum", 18, "0x92d6c1e31e14520e676a687f0a93788b716bff5c"),
                ("GMX", "GMX", "ethereum", 18, "0xfc5a1a6eb076a20758f8fb4ba4c39a6ca53646ca"),
                ("RNDR", "Render", "ethereum", 18, "0x6de037ef9ad2725eb8735660cbf048ccd7b32b63"),
                ("AGLD", "Adventure Gold", "ethereum", 18, "0x32353a6c91143bfa6c6388726aeab87e463a1833"),
                ("STG", "Stargate Finance", "ethereum", 18, "0xaf5191b0de278c7286d6c7cc246f992d50d68a9f"),
                ("USDA", "USDA Stablecoin", "ethereum", 18, "0x0000000000000000000000000000000000000000"),
                ("FRAX", "Frax", "ethereum", 18, "0x853d955acef822db058eb8505911ed77f175b999"),
                ("BUSD", "Binance USD", "ethereum", 18, "0x4fabb145d64652a948d72533023f6e7a623c7c53"),
            ]

            for symbol, name, blockchain, decimals, contract_address in cryptocurrencies:
                asset = CryptoAsset(
                    symbol=symbol,
                    name=name,
                    blockchain=blockchain,
                    decimals=decimals,
                    contract_address=contract_address,
                    is_supported=True,
                    created_at=datetime.utcnow(),
                )
                session.add(asset)

            logger.info(f"Created {len(cryptocurrencies)} supported cryptocurrencies")

            # Commit all changes
            await session.commit()
            logger.info("Database initialization completed successfully!")

        await engine.dispose()

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_database())
