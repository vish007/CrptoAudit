"""Validators for crypto addresses and data."""
import re
from typing import Tuple
from decimal import Decimal


def validate_ethereum_address(address: str) -> Tuple[bool, str]:
    """
    Validate Ethereum address format.

    Args:
        address: Ethereum address to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(address, str):
        return False, "Address must be a string"

    if not address.startswith("0x"):
        return False, "Address must start with 0x"

    if len(address) != 42:
        return False, "Address must be 42 characters long"

    if not re.match(r"^0x[0-9a-fA-F]{40}$", address):
        return False, "Address contains invalid characters"

    return True, "Valid"


def validate_bitcoin_address(address: str) -> Tuple[bool, str]:
    """
    Validate Bitcoin address format.

    Args:
        address: Bitcoin address to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(address, str):
        return False, "Address must be a string"

    # P2PKH (legacy)
    if address.startswith("1") and len(address) in [26, 35]:
        if re.match(r"^1[a-km-zA-HJ-NP-Z1-9]{25,34}$", address):
            return True, "Valid P2PKH address"

    # P2SH
    if address.startswith("3") and len(address) in [26, 35]:
        if re.match(r"^3[a-km-zA-HJ-NP-Z1-9]{25,34}$", address):
            return True, "Valid P2SH address"

    # P2WPKH (Segwit)
    if address.startswith("bc1") and len(address) in [42, 62]:
        if re.match(r"^bc1[a-z0-9]{39,59}$", address):
            return True, "Valid Segwit address"

    return False, "Invalid Bitcoin address format"


def validate_solana_address(address: str) -> Tuple[bool, str]:
    """
    Validate Solana address format.

    Args:
        address: Solana address to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(address, str):
        return False, "Address must be a string"

    if len(address) != 44:
        return False, "Solana address must be 44 characters"

    # Base58 validation
    import base58
    try:
        decoded = base58.b58decode(address)
        if len(decoded) == 32:
            return True, "Valid"
    except Exception:
        pass

    return False, "Invalid Solana address format"


def validate_xrp_address(address: str) -> Tuple[bool, str]:
    """
    Validate XRP Ledger address format.

    Args:
        address: XRP address to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(address, str):
        return False, "Address must be a string"

    if not address.startswith("r"):
        return False, "XRP address must start with 'r'"

    if len(address) < 25 or len(address) > 34:
        return False, "XRP address has invalid length"

    # Base58 validation
    import base58
    try:
        base58.b58decode(address)
        return True, "Valid"
    except Exception:
        return False, "Invalid XRP address format"


def validate_crypto_amount(
    amount: Decimal,
    asset_type: str,
) -> Tuple[bool, str]:
    """
    Validate cryptocurrency amount.

    Args:
        amount: Amount to validate
        asset_type: Type of asset (token, coin, etc.)

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(amount, (int, float, Decimal)):
        return False, "Amount must be numeric"

    if isinstance(amount, (int, float)):
        amount = Decimal(str(amount))

    if amount < 0:
        return False, "Amount cannot be negative"

    if amount == 0:
        return False, "Amount must be greater than zero"

    return True, "Valid"


def validate_blockchain_name(blockchain: str) -> Tuple[bool, str]:
    """
    Validate blockchain name.

    Args:
        blockchain: Blockchain name to validate

    Returns:
        Tuple of (is_valid, message)
    """
    valid_blockchains = {
        "ethereum",
        "polygon",
        "bitcoin",
        "litecoin",
        "solana",
        "ripple",
        "cardano",
        "algorand",
        "polkadot",
        "avalanche",
        "arbitrum",
        "optimism",
    }

    if blockchain.lower() not in valid_blockchains:
        return False, f"Invalid blockchain. Must be one of: {', '.join(valid_blockchains)}"

    return True, "Valid"


def validate_custody_type(custody_type: str) -> Tuple[bool, str]:
    """
    Validate custody type.

    Args:
        custody_type: Custody type to validate

    Returns:
        Tuple of (is_valid, message)
    """
    valid_types = {
        "SELF_CUSTODY",
        "THIRD_PARTY_CUSTODIAN",
        "DEFI_CONTRACT",
    }

    if custody_type not in valid_types:
        return False, f"Invalid custody type. Must be one of: {', '.join(valid_types)}"

    return True, "Valid"


def validate_wallet_type(wallet_type: str) -> Tuple[bool, str]:
    """
    Validate wallet type.

    Args:
        wallet_type: Wallet type to validate

    Returns:
        Tuple of (is_valid, message)
    """
    valid_types = {
        "HOT",
        "WARM",
        "COLD",
        "HARDWARE",
        "MPC",
    }

    if wallet_type not in valid_types:
        return False, f"Invalid wallet type. Must be one of: {', '.join(valid_types)}"

    return True, "Valid"


def validate_engagement_status(status: str) -> Tuple[bool, str]:
    """
    Validate engagement status.

    Args:
        status: Status to validate

    Returns:
        Tuple of (is_valid, message)
    """
    valid_statuses = {
        "PLANNING",
        "DATA_COLLECTION",
        "VERIFICATION",
        "REPORTING",
        "COMPLETED",
    }

    if status not in valid_statuses:
        return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

    return True, "Valid"


def validate_tenant_type(tenant_type: str) -> Tuple[bool, str]:
    """
    Validate tenant type.

    Args:
        tenant_type: Tenant type to validate

    Returns:
        Tuple of (is_valid, message)
    """
    valid_types = {
        "AUDITOR",
        "VASP",
        "REGULATOR",
        "CUSTOMER",
    }

    if tenant_type not in valid_types:
        return False, f"Invalid tenant type. Must be one of: {', '.join(valid_types)}"

    return True, "Valid"
