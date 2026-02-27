"""Test data factories for SimplyFI PoR Platform."""
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Dict, List, Optional

from faker import Faker

fake = Faker()


class UserFactory:
    """Factory for creating test User instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build a user dictionary without saving to database."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "email": kwargs.get("email", fake.email()),
            "full_name": kwargs.get("full_name", fake.name()),
            "hashed_password": kwargs.get(
                "hashed_password", "$2b$12$abcdefghijklmnopqrstuvwxyz"
            ),
            "is_active": kwargs.get("is_active", True),
            "is_superadmin": kwargs.get("is_superadmin", False),
            "tenant_id": kwargs.get("tenant_id", str(uuid.uuid4())),
            "mfa_enabled": kwargs.get("mfa_enabled", False),
            "mfa_secret": kwargs.get("mfa_secret", None),
            "last_login": kwargs.get("last_login", None),
            "last_ip": kwargs.get("last_ip", fake.ipv4()),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }

    @staticmethod
    def admin_build(**kwargs) -> Dict:
        """Build a superadmin user."""
        return UserFactory.build(is_superadmin=True, **kwargs)

    @staticmethod
    def inactive_build(**kwargs) -> Dict:
        """Build an inactive user."""
        return UserFactory.build(is_active=False, **kwargs)


class TenantFactory:
    """Factory for creating test Tenant instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build a tenant dictionary without saving to database."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "name": kwargs.get("name", fake.company()),
            "type": kwargs.get("type", "AUDITOR"),
            "vara_license_number": kwargs.get(
                "vara_license_number", f"VARA-{fake.bothify(text='??-######')}"
            ),
            "status": kwargs.get("status", "ACTIVE"),
            "settings_json": kwargs.get("settings_json", "{}"),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }

    @staticmethod
    def vasp_build(**kwargs) -> Dict:
        """Build a VASP tenant."""
        return TenantFactory.build(type="VASP", **kwargs)

    @staticmethod
    def auditor_build(**kwargs) -> Dict:
        """Build an auditor tenant."""
        return TenantFactory.build(type="AUDITOR", **kwargs)


class EngagementFactory:
    """Factory for creating test Engagement instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build an engagement dictionary without saving to database."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "title": kwargs.get("title", f"PoR Audit {fake.word()}"),
            "description": kwargs.get("description", fake.text(100)),
            "client_tenant_id": kwargs.get("client_tenant_id", str(uuid.uuid4())),
            "auditor_tenant_id": kwargs.get(
                "auditor_tenant_id", str(uuid.uuid4())
            ),
            "status": kwargs.get("status", "PLANNING"),
            "start_date": kwargs.get(
                "start_date", datetime.now(timezone.utc)
            ),
            "end_date": kwargs.get(
                "end_date",
                datetime.now(timezone.utc) + timedelta(days=30),
            ),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }

    @staticmethod
    def in_progress_build(**kwargs) -> Dict:
        """Build an in-progress engagement."""
        return EngagementFactory.build(status="VERIFICATION", **kwargs)


class AssetFactory:
    """Factory for creating test Asset instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build an asset dictionary without saving to database."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "engagement_id": kwargs.get("engagement_id", str(uuid.uuid4())),
            "asset_name": kwargs.get("asset_name", fake.word().upper()),
            "blockchain": kwargs.get("blockchain", "ethereum"),
            "total_balance": kwargs.get(
                "total_balance", float(fake.random_int(1000, 1000000))
            ),
            "wallet_count": kwargs.get("wallet_count", fake.random_int(1, 20)),
            "verification_status": kwargs.get(
                "verification_status", "PENDING"
            ),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }

    @staticmethod
    def ethereum_build(**kwargs) -> Dict:
        """Build an Ethereum asset."""
        return AssetFactory.build(asset_name="ETH", blockchain="ethereum", **kwargs)

    @staticmethod
    def bitcoin_build(**kwargs) -> Dict:
        """Build a Bitcoin asset."""
        return AssetFactory.build(asset_name="BTC", blockchain="bitcoin", **kwargs)


class WalletFactory:
    """Factory for creating test Wallet instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build a wallet dictionary without saving to database."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "asset_id": kwargs.get("asset_id", str(uuid.uuid4())),
            "wallet_address": kwargs.get(
                "wallet_address", f"0x{fake.bothify(text='#' * 40)}"
            ),
            "wallet_type": kwargs.get("wallet_type", "COLD"),
            "custody_type": kwargs.get("custody_type", "SELF_CUSTODY"),
            "balance": kwargs.get("balance", float(Decimal("1000.50"))),
            "verified": kwargs.get("verified", False),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }

    @staticmethod
    def verified_build(**kwargs) -> Dict:
        """Build a verified wallet."""
        return WalletFactory.build(verified=True, **kwargs)


class CustomerLiabilityFactory:
    """Factory for creating test Customer Liability instances."""

    @staticmethod
    def build(**kwargs) -> Dict:
        """Build a customer liability dictionary."""
        return {
            "id": kwargs.get("id", str(uuid.uuid4())),
            "engagement_id": kwargs.get("engagement_id", str(uuid.uuid4())),
            "customer_id": kwargs.get("customer_id", fake.bothify(text="CUST-#####")),
            "customer_name": kwargs.get("customer_name", fake.name()),
            "assets": kwargs.get("assets", {"ETH": 10.5, "USDC": 1000.0}),
            "total_liability": kwargs.get(
                "total_liability", float(Decimal("1010.50"))
            ),
            "created_at": kwargs.get(
                "created_at", datetime.now(timezone.utc)
            ),
            "updated_at": kwargs.get(
                "updated_at", datetime.now(timezone.utc)
            ),
        }


class TokenFactory:
    """Factory for creating test JWT tokens."""

    @staticmethod
    def build(**kwargs) -> str:
        """Build a JWT token."""
        from datetime import datetime, timezone, timedelta
        from jose import jwt
        from app.core.config import settings

        payload = {
            "sub": kwargs.get("user_id", str(uuid.uuid4())),
            "tenant_id": kwargs.get("tenant_id", str(uuid.uuid4())),
            "email": kwargs.get("email", fake.email()),
            "is_active": kwargs.get("is_active", True),
            "is_superadmin": kwargs.get("is_superadmin", False),
            "permissions": kwargs.get("permissions", []),
            "exp": datetime.now(timezone.utc) + timedelta(
                minutes=kwargs.get("expires_in_minutes", 30)
            ),
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def admin_build(**kwargs) -> str:
        """Build a token for a superadmin."""
        return TokenFactory.build(is_superadmin=True, **kwargs)

    @staticmethod
    def expired_build(**kwargs) -> str:
        """Build an expired token."""
        from datetime import datetime, timezone, timedelta
        from jose import jwt
        from app.core.config import settings

        payload = {
            "sub": str(uuid.uuid4()),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
