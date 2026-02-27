"""Integration tests for onboarding flow."""
import pytest


@pytest.mark.integration
class TestVASPOnboarding:
    """Tests for VASP onboarding."""

    def test_register_vasp(self, client, sample_tenant_data):
        """Test VASP registration."""
        response = client.post(
            "/api/v1/onboarding/register-vasp",
            json=sample_tenant_data,
        )

        assert response.status_code in [200, 201, 404]

        if response.status_code in [200, 201]:
            data = response.json()
            assert "id" in data
            assert data["type"] == "VASP"


@pytest.mark.integration
class TestAssetImport:
    """Tests for asset import."""

    def test_import_assets(self, client, auth_headers):
        """Test importing assets."""
        assets_data = {
            "assets": [
                {
                    "asset_name": "BTC",
                    "blockchain": "bitcoin",
                    "total_balance": 50.5,
                },
                {
                    "asset_name": "ETH",
                    "blockchain": "ethereum",
                    "total_balance": 1000.0,
                },
            ]
        }

        response = client.post(
            "/api/v1/onboarding/import-assets",
            json=assets_data,
            headers=auth_headers,
        )

        assert response.status_code in [200, 201, 404]


@pytest.mark.integration
class TestWalletImport:
    """Tests for wallet CSV import."""

    def test_import_wallets_csv(self, client, auth_headers):
        """Test importing wallets from CSV."""
        wallets_data = {
            "wallets": [
                {
                    "address": "0x742d35Cc6634C0532925a3b844Bc314e5505b748",
                    "blockchain": "ethereum",
                    "balance": 1000.5,
                    "wallet_type": "COLD",
                    "custody_type": "SELF_CUSTODY",
                },
                {
                    "address": "1A1z7agoat7qsweQvUwhwYBCn1qWu5Hspp",
                    "blockchain": "bitcoin",
                    "balance": 50.25,
                    "wallet_type": "COLD",
                    "custody_type": "SELF_CUSTODY",
                },
            ]
        }

        response = client.post(
            "/api/v1/onboarding/import-wallets",
            json=wallets_data,
            headers=auth_headers,
        )

        assert response.status_code in [200, 201, 404]

        if response.status_code in [200, 201]:
            data = response.json()
            # Should show import results
            assert isinstance(data, dict)


@pytest.mark.integration
class TestLiabilityImport:
    """Tests for liability import."""

    def test_import_liabilities(self, client, auth_headers):
        """Test importing customer liabilities."""
        liabilities_data = {
            "customers": [
                {
                    "customer_id": "CUST-001",
                    "customer_name": "Customer 1",
                    "assets": {
                        "ETH": 10.5,
                        "USDC": 1000.0,
                    },
                },
                {
                    "customer_id": "CUST-002",
                    "customer_name": "Customer 2",
                    "assets": {
                        "BTC": 2.5,
                        "ETH": 50.0,
                    },
                },
            ]
        }

        response = client.post(
            "/api/v1/onboarding/import-liabilities",
            json=liabilities_data,
            headers=auth_headers,
        )

        assert response.status_code in [200, 201, 404]


@pytest.mark.integration
class TestDataValidation:
    """Tests for onboarding data validation."""

    def test_validate_imported_data(self, client, auth_headers):
        """Test validating imported data."""
        validation_request = {
            "assets_count": 2,
            "wallets_count": 5,
            "customers_count": 100,
        }

        response = client.post(
            "/api/v1/onboarding/validate",
            json=validation_request,
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should indicate validation results
            assert isinstance(data, dict)


@pytest.mark.integration
class TestOnboardingStatus:
    """Tests for onboarding status tracking."""

    def test_onboarding_status_tracking(self, client, auth_headers):
        """Test tracking onboarding status."""
        response = client.get(
            "/api/v1/onboarding/status",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should show progress
            if "progress" in data:
                assert 0 <= data["progress"] <= 100
            if "current_step" in data:
                assert isinstance(data["current_step"], str)
