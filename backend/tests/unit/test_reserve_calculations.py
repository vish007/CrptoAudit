"""Unit tests for reserve ratio calculations."""
import pytest
from decimal import Decimal


@pytest.mark.unit
class TestReserveRatioCalculation:
    """Tests for reserve ratio calculations."""

    def test_reserve_ratio_100_percent(self):
        """Test reserve ratio at 100%."""
        total_assets = Decimal("1000")
        total_liabilities = Decimal("1000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio == Decimal("100")

    def test_reserve_ratio_over_100_percent(self):
        """Test reserve ratio over 100%."""
        total_assets = Decimal("1500")
        total_liabilities = Decimal("1000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio == Decimal("150")

    def test_reserve_ratio_under_100_percent(self):
        """Test reserve ratio under 100%."""
        total_assets = Decimal("800")
        total_liabilities = Decimal("1000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio == Decimal("80")

    def test_reserve_ratio_zero_liabilities(self):
        """Test reserve ratio with zero liabilities."""
        total_assets = Decimal("1000")
        total_liabilities = Decimal("0")

        with pytest.raises(ZeroDivisionError):
            ratio = (total_assets / total_liabilities) * 100

    def test_reserve_ratio_zero_assets(self):
        """Test reserve ratio with zero assets."""
        total_assets = Decimal("0")
        total_liabilities = Decimal("1000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio == Decimal("0")

    def test_reserve_ratio_precision(self):
        """Test reserve ratio with decimal precision."""
        total_assets = Decimal("1000.5555")
        total_liabilities = Decimal("1000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio > Decimal("100")
        assert ratio < Decimal("101")


@pytest.mark.unit
class TestMultiAssetReserves:
    """Tests for reserve calculations with multiple assets."""

    def test_reserve_with_multiple_assets(self):
        """Test reserve ratio with multiple assets."""
        assets = {
            "BTC": Decimal("10"),
            "ETH": Decimal("100"),
            "USDC": Decimal("50000"),
        }

        # Assume prices: BTC=40000, ETH=2000, USDC=1
        prices = {"BTC": Decimal("40000"), "ETH": Decimal("2000"), "USDC": Decimal("1")}

        total_assets = sum(
            assets[asset] * prices[asset] for asset in assets
        )

        total_liabilities = Decimal("500000")
        ratio = (total_assets / total_liabilities) * 100

        assert ratio > Decimal("90")

    def test_reserve_with_different_currencies(self):
        """Test reserve calculation with different currency values."""
        eth_balance = Decimal("100")
        eth_price = Decimal("2000")
        eth_value = eth_balance * eth_price

        usdc_balance = Decimal("50000")
        usdc_price = Decimal("1")
        usdc_value = usdc_balance * usdc_price

        total_assets = eth_value + usdc_value
        total_liabilities = Decimal("250000")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio >= Decimal("80")


@pytest.mark.unit
class TestVARACompliance:
    """Tests for VARA compliance checking."""

    def test_vara_compliance_check_passing(self):
        """Test VARA compliance check passes."""
        total_assets = Decimal("1050")  # 105% of liabilities
        total_liabilities = Decimal("1000")
        required_ratio = Decimal("100")

        actual_ratio = (total_assets / total_liabilities) * 100

        is_compliant = actual_ratio >= required_ratio

        assert is_compliant is True

    def test_vara_compliance_check_failing(self):
        """Test VARA compliance check fails."""
        total_assets = Decimal("950")  # 95% of liabilities
        total_liabilities = Decimal("1000")
        required_ratio = Decimal("100")

        actual_ratio = (total_assets / total_liabilities) * 100

        is_compliant = actual_ratio >= required_ratio

        assert is_compliant is False

    def test_vara_compliance_marginal(self):
        """Test VARA compliance at exact threshold."""
        total_assets = Decimal("1000")
        total_liabilities = Decimal("1000")
        required_ratio = Decimal("100")

        actual_ratio = (total_assets / total_liabilities) * 100

        is_compliant = actual_ratio >= required_ratio

        assert is_compliant is True


@pytest.mark.unit
class TestVarianceCalculation:
    """Tests for variance calculations in reserve tracking."""

    def test_variance_calculation_positive(self):
        """Test positive variance calculation."""
        previous_balance = Decimal("1000")
        current_balance = Decimal("1050")

        variance = ((current_balance - previous_balance) / previous_balance) * 100

        assert variance == Decimal("5")

    def test_variance_calculation_negative(self):
        """Test negative variance calculation."""
        previous_balance = Decimal("1000")
        current_balance = Decimal("950")

        variance = ((current_balance - previous_balance) / previous_balance) * 100

        assert variance == Decimal("-5")

    def test_variance_calculation_zero(self):
        """Test zero variance calculation."""
        previous_balance = Decimal("1000")
        current_balance = Decimal("1000")

        variance = ((current_balance - previous_balance) / previous_balance) * 100

        assert variance == Decimal("0")

    def test_variance_threshold_0_5_percent(self):
        """Test variance threshold detection."""
        previous_balance = Decimal("1000")
        current_balance = Decimal("1006")
        threshold = Decimal("0.5")

        variance = abs(
            ((current_balance - previous_balance) / previous_balance) * 100
        )

        exceeds_threshold = variance > threshold

        assert exceeds_threshold is True

    def test_variance_below_threshold(self):
        """Test variance below threshold."""
        previous_balance = Decimal("1000")
        current_balance = Decimal("1003")
        threshold = Decimal("0.5")

        variance = abs(
            ((current_balance - previous_balance) / previous_balance) * 100
        )

        exceeds_threshold = variance > threshold

        assert exceeds_threshold is False


@pytest.mark.unit
class TestAggregateReserves:
    """Tests for aggregating reserves across wallets."""

    def test_aggregate_reserve_across_wallets(self):
        """Test aggregating reserves across multiple wallets."""
        wallets = {
            "wallet_1": Decimal("100"),
            "wallet_2": Decimal("200"),
            "wallet_3": Decimal("150"),
        }

        total = sum(wallets.values())

        assert total == Decimal("450")

    def test_aggregate_with_different_blockchains(self):
        """Test aggregating reserves across blockchains."""
        reserves = {
            "ethereum": Decimal("500"),
            "bitcoin": Decimal("250"),
            "solana": Decimal("100"),
        }

        total = sum(reserves.values())

        assert total == Decimal("850")

    def test_aggregate_with_defi_positions(self):
        """Test aggregating reserves including DeFi positions."""
        spot_reserves = Decimal("1000")
        defi_positions = {
            "aave_deposits": Decimal("500"),
            "uniswap_liquidity": Decimal("300"),
        }

        total_defi = sum(defi_positions.values())
        total_reserves = spot_reserves + total_defi

        assert total_reserves == Decimal("1800")


@pytest.mark.unit
class TestReserveWithDeFi:
    """Tests for reserves calculation with DeFi positions."""

    def test_reserve_with_defi_positions(self):
        """Test reserve ratio including DeFi positions."""
        spot_assets = Decimal("500")
        aave_deposits = Decimal("200")
        uniswap_liquidity = Decimal("100")

        total_assets = spot_assets + aave_deposits + uniswap_liquidity
        total_liabilities = Decimal("750")

        ratio = (total_assets / total_liabilities) * 100

        assert ratio >= Decimal("100")

    def test_defi_position_verification(self):
        """Test verification of DeFi position value."""
        collateral_amount = Decimal("100")
        collateral_price = Decimal("2000")
        collateral_value = collateral_amount * collateral_price

        assert collateral_value == Decimal("200000")

    def test_defi_with_lending_protocol(self):
        """Test reserves with lending protocol deposits."""
        deposited_amount = Decimal("500")
        apy_percent = Decimal("5")

        interest_earned = (deposited_amount * apy_percent) / Decimal("100")
        total_value = deposited_amount + interest_earned

        assert total_value == Decimal("525")


@pytest.mark.unit
class TestReserveSeparation:
    """Tests for reserve segregation compliance."""

    def test_customer_liabilities_vs_operational_reserves(self):
        """Test separation of customer liabilities from operational reserves."""
        customer_liabilities = Decimal("1000")
        operational_reserves = Decimal("100")

        total_liabilities = customer_liabilities
        total_assets = customer_liabilities + operational_reserves

        ratio = (total_assets / total_liabilities) * 100

        # Assets should cover customer liabilities plus operational buffer
        assert ratio >= Decimal("110")

    def test_segregation_compliance_check(self):
        """Test compliance with asset segregation requirements."""
        customer_assets = Decimal("1050")
        operational_assets = Decimal("50")
        customer_liabilities = Decimal("1000")

        # Customer assets must cover customer liabilities
        customer_coverage = (customer_assets / customer_liabilities) * 100

        assert customer_coverage >= Decimal("100")

    def test_collateral_segregation(self):
        """Test segregation of collateral from general reserves."""
        collateral_reserves = Decimal("500")
        general_reserves = Decimal("500")

        total_reserves = collateral_reserves + general_reserves

        assert total_reserves == Decimal("1000")
        assert collateral_reserves == general_reserves
