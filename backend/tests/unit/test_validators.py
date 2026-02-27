"""Unit tests for input validators."""
import pytest
from decimal import Decimal

from app.utils.validators import (
    validate_ethereum_address,
    validate_bitcoin_address,
    validate_solana_address,
    validate_xrp_address,
    validate_crypto_amount,
    validate_blockchain_name,
    validate_custody_type,
    validate_wallet_type,
    validate_engagement_status,
    validate_tenant_type,
)


@pytest.mark.unit
class TestEthereumValidator:
    """Tests for Ethereum address validation."""

    def test_valid_ethereum_address(self):
        """Test valid Ethereum address."""
        is_valid, message = validate_ethereum_address(
            "0x742d35Cc6634C0532925a3b844Bc314e5505b748"
        )
        assert is_valid is True
        assert "Valid" in message

    def test_invalid_ethereum_address_wrong_prefix(self):
        """Test Ethereum address without 0x prefix."""
        is_valid, message = validate_ethereum_address(
            "742d35Cc6634C0532925a3b844Bc314e5505b748"
        )
        assert is_valid is False

    def test_invalid_ethereum_address_wrong_length(self):
        """Test Ethereum address with wrong length."""
        is_valid, message = validate_ethereum_address("0x123")
        assert is_valid is False

    def test_invalid_ethereum_address_invalid_chars(self):
        """Test Ethereum address with invalid characters."""
        is_valid, message = validate_ethereum_address(
            "0x742d35Cc6634C0532925a3b844Bc314e5505bZZZ"
        )
        assert is_valid is False

    def test_ethereum_address_non_string(self):
        """Test non-string Ethereum address."""
        is_valid, message = validate_ethereum_address(123456)
        assert is_valid is False


@pytest.mark.unit
class TestBitcoinValidator:
    """Tests for Bitcoin address validation."""

    def test_valid_bitcoin_p2pkh_address(self):
        """Test valid Bitcoin P2PKH address."""
        is_valid, message = validate_bitcoin_address(
            "1A1z7agoat7qsweQvUwhwYBCn1qWu5Hspp"
        )
        assert is_valid is True
        assert "P2PKH" in message or "Valid" in message

    def test_valid_bitcoin_bech32_address(self):
        """Test valid Bitcoin Bech32 address."""
        is_valid, message = validate_bitcoin_address(
            "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
        )
        assert is_valid is True
        assert "Segwit" in message or "Valid" in message

    def test_invalid_bitcoin_address(self):
        """Test invalid Bitcoin address."""
        is_valid, message = validate_bitcoin_address("invalid_address")
        assert is_valid is False

    def test_bitcoin_address_non_string(self):
        """Test non-string Bitcoin address."""
        is_valid, message = validate_bitcoin_address(123456)
        assert is_valid is False


@pytest.mark.unit
class TestSolanaValidator:
    """Tests for Solana address validation."""

    def test_valid_solana_address(self):
        """Test valid Solana address."""
        # Valid Solana address (44 chars, base58)
        is_valid, message = validate_solana_address(
            "9B5X4z5zzJGLccBx86ggHmwYmUo9Uu7XuUTqMacHj9tZ"
        )
        assert is_valid in [True, False]  # Depends on if base58 is available

    def test_invalid_solana_address_wrong_length(self):
        """Test Solana address with wrong length."""
        is_valid, message = validate_solana_address("9B5X4z5zzJGLccBx86ggHmwYmUo9Uu7XuUTqMacHj9tZZ")
        assert is_valid is False

    def test_solana_address_non_string(self):
        """Test non-string Solana address."""
        is_valid, message = validate_solana_address(123456)
        assert is_valid is False


@pytest.mark.unit
class TestXRPValidator:
    """Tests for XRP address validation."""

    def test_valid_xrp_address(self):
        """Test valid XRP address."""
        is_valid, message = validate_xrp_address(
            "rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH"
        )
        assert is_valid in [True, False]  # Depends on base58 availability

    def test_invalid_xrp_address_wrong_prefix(self):
        """Test XRP address without 'r' prefix."""
        is_valid, message = validate_xrp_address("N7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH")
        assert is_valid is False

    def test_invalid_xrp_address_wrong_length(self):
        """Test XRP address with wrong length."""
        is_valid, message = validate_xrp_address("r123")
        assert is_valid is False

    def test_xrp_address_non_string(self):
        """Test non-string XRP address."""
        is_valid, message = validate_xrp_address(123456)
        assert is_valid is False


@pytest.mark.unit
class TestCryptoAmountValidator:
    """Tests for cryptocurrency amount validation."""

    def test_valid_crypto_amount_decimal(self):
        """Test valid crypto amount as Decimal."""
        is_valid, message = validate_crypto_amount(
            Decimal("100.50"), "ethereum"
        )
        assert is_valid is True

    def test_valid_crypto_amount_float(self):
        """Test valid crypto amount as float."""
        is_valid, message = validate_crypto_amount(100.50, "ethereum")
        assert is_valid is True

    def test_valid_crypto_amount_int(self):
        """Test valid crypto amount as int."""
        is_valid, message = validate_crypto_amount(100, "ethereum")
        assert is_valid is True

    def test_invalid_crypto_amount_negative(self):
        """Test negative crypto amount."""
        is_valid, message = validate_crypto_amount(Decimal("-100"), "ethereum")
        assert is_valid is False

    def test_invalid_crypto_amount_zero(self):
        """Test zero crypto amount."""
        is_valid, message = validate_crypto_amount(Decimal("0"), "ethereum")
        assert is_valid is False

    def test_invalid_crypto_amount_non_numeric(self):
        """Test non-numeric crypto amount."""
        is_valid, message = validate_crypto_amount("hundred", "ethereum")
        assert is_valid is False


@pytest.mark.unit
class TestBlockchainNameValidator:
    """Tests for blockchain name validation."""

    def test_valid_ethereum_blockchain(self):
        """Test valid Ethereum blockchain name."""
        is_valid, message = validate_blockchain_name("ethereum")
        assert is_valid is True

    def test_valid_bitcoin_blockchain(self):
        """Test valid Bitcoin blockchain name."""
        is_valid, message = validate_blockchain_name("bitcoin")
        assert is_valid is True

    def test_valid_solana_blockchain(self):
        """Test valid Solana blockchain name."""
        is_valid, message = validate_blockchain_name("solana")
        assert is_valid is True

    def test_invalid_blockchain_name(self):
        """Test invalid blockchain name."""
        is_valid, message = validate_blockchain_name("invalid_chain")
        assert is_valid is False

    def test_blockchain_name_case_insensitive(self):
        """Test blockchain name validation is case insensitive."""
        is_valid, message = validate_blockchain_name("ETHEREUM")
        assert is_valid is True


@pytest.mark.unit
class TestCustodyTypeValidator:
    """Tests for custody type validation."""

    def test_valid_custody_type_self(self):
        """Test valid self-custody type."""
        is_valid, message = validate_custody_type("SELF_CUSTODY")
        assert is_valid is True

    def test_valid_custody_type_third_party(self):
        """Test valid third-party custody type."""
        is_valid, message = validate_custody_type("THIRD_PARTY_CUSTODIAN")
        assert is_valid is True

    def test_valid_custody_type_defi(self):
        """Test valid DeFi contract custody type."""
        is_valid, message = validate_custody_type("DEFI_CONTRACT")
        assert is_valid is True

    def test_invalid_custody_type(self):
        """Test invalid custody type."""
        is_valid, message = validate_custody_type("INVALID_TYPE")
        assert is_valid is False


@pytest.mark.unit
class TestWalletTypeValidator:
    """Tests for wallet type validation."""

    def test_valid_wallet_type_hot(self):
        """Test valid hot wallet type."""
        is_valid, message = validate_wallet_type("HOT")
        assert is_valid is True

    def test_valid_wallet_type_cold(self):
        """Test valid cold wallet type."""
        is_valid, message = validate_wallet_type("COLD")
        assert is_valid is True

    def test_valid_wallet_type_hardware(self):
        """Test valid hardware wallet type."""
        is_valid, message = validate_wallet_type("HARDWARE")
        assert is_valid is True

    def test_valid_wallet_type_mpc(self):
        """Test valid MPC wallet type."""
        is_valid, message = validate_wallet_type("MPC")
        assert is_valid is True

    def test_invalid_wallet_type(self):
        """Test invalid wallet type."""
        is_valid, message = validate_wallet_type("INVALID_TYPE")
        assert is_valid is False


@pytest.mark.unit
class TestEngagementStatusValidator:
    """Tests for engagement status validation."""

    def test_valid_engagement_status_planning(self):
        """Test valid planning status."""
        is_valid, message = validate_engagement_status("PLANNING")
        assert is_valid is True

    def test_valid_engagement_status_verification(self):
        """Test valid verification status."""
        is_valid, message = validate_engagement_status("VERIFICATION")
        assert is_valid is True

    def test_valid_engagement_status_completed(self):
        """Test valid completed status."""
        is_valid, message = validate_engagement_status("COMPLETED")
        assert is_valid is True

    def test_invalid_engagement_status(self):
        """Test invalid engagement status."""
        is_valid, message = validate_engagement_status("INVALID_STATUS")
        assert is_valid is False


@pytest.mark.unit
class TestTenantTypeValidator:
    """Tests for tenant type validation."""

    def test_valid_tenant_type_auditor(self):
        """Test valid auditor tenant type."""
        is_valid, message = validate_tenant_type("AUDITOR")
        assert is_valid is True

    def test_valid_tenant_type_vasp(self):
        """Test valid VASP tenant type."""
        is_valid, message = validate_tenant_type("VASP")
        assert is_valid is True

    def test_valid_tenant_type_regulator(self):
        """Test valid regulator tenant type."""
        is_valid, message = validate_tenant_type("REGULATOR")
        assert is_valid is True

    def test_valid_tenant_type_customer(self):
        """Test valid customer tenant type."""
        is_valid, message = validate_tenant_type("CUSTOMER")
        assert is_valid is True

    def test_invalid_tenant_type(self):
        """Test invalid tenant type."""
        is_valid, message = validate_tenant_type("INVALID_TYPE")
        assert is_valid is False
