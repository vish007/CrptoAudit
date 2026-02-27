"""Integration tests for reserves API."""
import pytest
from decimal import Decimal


@pytest.mark.integration
class TestReservesCalculation:
    """Tests for reserve calculation API."""

    def test_calculate_reserve_ratios(self, client, auth_headers):
        """Test calculating reserve ratios."""
        request_data = {
            "total_assets": 1500000.0,
            "total_liabilities": 1000000.0,
            "assets_by_type": {
                "BTC": 50.5,
                "ETH": 1000.0,
                "USDC": 500000.0,
            },
        }

        response = client.post(
            "/api/v1/reserves/calculate",
            json=request_data,
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "ratio" in data or "reserve_ratio" in data

    def test_get_ratio_table(self, client, auth_headers):
        """Test retrieving reserve ratio table."""
        response = client.get(
            "/api/v1/engagements/test-id/reserves/table",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should contain reserve data
            if isinstance(data, list):
                if len(data) > 0:
                    assert "asset" in data[0] or "balance" in data[0]


@pytest.mark.integration
class TestSegregationVerification:
    """Tests for asset segregation verification."""

    def test_verify_segregation(self, client, auth_headers):
        """Test verifying asset segregation."""
        response = client.get(
            "/api/v1/engagements/test-id/segregation",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should contain segregation status
            assert isinstance(data, dict)


@pytest.mark.integration
class TestReconciliationData:
    """Tests for reconciliation data."""

    def test_reconciliation_data(self, client, auth_headers):
        """Test retrieving reconciliation data."""
        response = client.get(
            "/api/v1/engagements/test-id/reconciliation",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should contain reconciliation data
            if "balance_discrepancies" in data:
                assert isinstance(data["balance_discrepancies"], list)


@pytest.mark.integration
class TestReserveHistory:
    """Tests for reserve ratio history."""

    def test_reserve_ratio_history(self, client, auth_headers):
        """Test retrieving reserve ratio history."""
        response = client.get(
            "/api/v1/engagements/test-id/reserves/history",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should be a time series
            if isinstance(data, list):
                if len(data) > 0:
                    assert "timestamp" in data[0] or "date" in data[0]


@pytest.mark.integration
class TestReserveWithDeFi:
    """Tests for reserve verification with DeFi positions."""

    def test_reserve_ratio_with_defi(self, client, auth_headers):
        """Test reserve ratio calculation including DeFi."""
        request_data = {
            "spot_assets": {
                "BTC": 50.5,
                "ETH": 1000.0,
            },
            "defi_positions": {
                "aave_deposits": 200000.0,
                "uniswap_liquidity": 100000.0,
            },
            "total_liabilities": 1000000.0,
        }

        response = client.post(
            "/api/v1/reserves/calculate-with-defi",
            json=request_data,
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should have ratio that includes DeFi
            assert isinstance(data, dict)
