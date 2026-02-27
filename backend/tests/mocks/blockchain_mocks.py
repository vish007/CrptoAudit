"""Mock blockchain API responses for testing."""
from decimal import Decimal
from typing import Dict, Any, List
from unittest.mock import AsyncMock


class EthereumMockResponses:
    """Mock responses for Ethereum blockchain API."""

    @staticmethod
    def balance_response(address: str, balance: float = 1000.5) -> Dict[str, Any]:
        """Mock Ethereum balance response."""
        return {
            "address": address,
            "balance": balance,
            "balance_wei": int(balance * 10**18),
            "token_transfers_in": 150,
            "token_transfers_out": 149,
            "transaction_count": 1000,
            "block_number": 19234567,
            "status": "1",
        }

    @staticmethod
    def erc20_balance_response(
        address: str,
        token_contract: str,
        balance: float = 5000.0,
    ) -> Dict[str, Any]:
        """Mock ERC20 token balance response."""
        return {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "blockNumber": "19234567",
                    "timeStamp": "1704067200",
                    "hash": "0x123abc",
                    "nonce": "0",
                    "blockHash": "0x456def",
                    "from": address,
                    "contractAddress": token_contract,
                    "to": "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
                    "value": str(int(balance * 10**18)),
                    "tokenName": "USDC",
                    "tokenSymbol": "USDC",
                    "tokenDecimal": "6",
                    "transactionIndex": "1",
                    "gas": "65000",
                    "gasPrice": "20000000000",
                    "gasUsed": "50000",
                    "cumulativeGasUsed": "5000000",
                    "input": "0x",
                    "confirmations": "100",
                }
            ],
        }

    @staticmethod
    def verification_response(
        address: str,
        is_valid: bool = True,
    ) -> Dict[str, Any]:
        """Mock address verification response."""
        return {
            "address": address,
            "is_valid": is_valid,
            "is_contract": False,
            "is_checksummed": True,
            "network": "ethereum",
        }


class BitcoinMockResponses:
    """Mock responses for Bitcoin blockchain API."""

    @staticmethod
    def balance_response(
        address: str,
        balance: float = 50.25,
    ) -> Dict[str, Any]:
        """Mock Bitcoin balance response."""
        return {
            "address": address,
            "balance": int(balance * 10**8),  # Satoshis
            "total_received": int(balance * 10**8 * 2),
            "total_sent": int(balance * 10**8),
            "unconfirmed_balance": 0,
            "unconfirmed_tx_count": 0,
            "tx_count": 150,
            "unspent_tx_count": 15,
        }

    @staticmethod
    def utxo_response(
        address: str,
        utxos: List[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """Mock Bitcoin UTXO response."""
        if utxos is None:
            utxos = [
                {
                    "txid": "abc1234567890def",
                    "vout": 0,
                    "value": int(25.125 * 10**8),
                    "script": "76a914abcdef",
                    "confirmations": 100,
                    "time": 1704067200,
                },
                {
                    "txid": "def7890123456abc",
                    "vout": 1,
                    "value": int(25.125 * 10**8),
                    "script": "76a914fedcba",
                    "confirmations": 50,
                    "time": 1704153600,
                },
            ]

        return utxos

    @staticmethod
    def verification_response(
        address: str,
        is_valid: bool = True,
    ) -> Dict[str, Any]:
        """Mock Bitcoin address verification response."""
        return {
            "address": address,
            "is_valid": is_valid,
            "address_type": "p2pkh",
            "network": "mainnet",
        }


class SolanaMockResponses:
    """Mock responses for Solana blockchain API."""

    @staticmethod
    def balance_response(
        address: str,
        balance: float = 100.0,
    ) -> Dict[str, Any]:
        """Mock Solana balance response."""
        return {
            "jsonrpc": "2.0",
            "result": {
                "context": {
                    "slot": 234234234,
                },
                "value": int(balance * 10**9),  # Lamports
            },
            "id": 1,
        }

    @staticmethod
    def verification_response(
        address: str,
        is_valid: bool = True,
    ) -> Dict[str, Any]:
        """Mock Solana address verification response."""
        return {
            "address": address,
            "is_valid": is_valid,
            "is_associated_token_account": False,
            "network": "mainnet",
        }

    @staticmethod
    def token_balance_response(
        address: str,
        token_mint: str,
        balance: float = 5000.0,
    ) -> Dict[str, Any]:
        """Mock Solana token balance response."""
        return {
            "jsonrpc": "2.0",
            "result": {
                "context": {
                    "slot": 234234234,
                },
                "value": {
                    "amount": str(int(balance * 10**6)),
                    "decimals": 6,
                    "owner": address,
                    "state": "initialized",
                    "uiAmount": balance,
                    "uiAmountString": str(balance),
                },
            },
            "id": 1,
        }


class DeFiMockResponses:
    """Mock responses for DeFi protocol APIs."""

    @staticmethod
    def aave_deposit_response(
        user_address: str,
        asset: str,
        balance: float = 1000.0,
    ) -> Dict[str, Any]:
        """Mock Aave deposit response."""
        return {
            "user_address": user_address,
            "asset": asset,
            "balance": balance,
            "apy": "3.45",
            "interest_earned": balance * Decimal("0.0345"),
            "collateral_enabled": True,
        }

    @staticmethod
    def uniswap_liquidity_response(
        pool_address: str,
        liquidity: float = 10000.0,
    ) -> Dict[str, Any]:
        """Mock Uniswap liquidity position response."""
        return {
            "pool": pool_address,
            "liquidity": liquidity,
            "amount0": liquidity / 2,
            "amount1": liquidity / 2,
            "fee_tier": 3000,
            "uncollected_fees": {
                "token0": "0.1",
                "token1": "0.05",
            },
        }

    @staticmethod
    def yearn_vault_response(
        vault_address: str,
        shares: float = 100.0,
    ) -> Dict[str, Any]:
        """Mock Yearn vault response."""
        return {
            "vault": vault_address,
            "shares": shares,
            "share_price": "1.05",
            "underlying_balance": shares * Decimal("1.05"),
            "apy": "8.5",
        }


class CustodianMockResponses:
    """Mock responses for custodian confirmations."""

    @staticmethod
    def custody_confirmation_response(
        confirmation_id: str,
        assets_confirmed: List[str],
        total_value: float = 100000.0,
    ) -> Dict[str, Any]:
        """Mock custodian confirmation response."""
        return {
            "confirmation_id": confirmation_id,
            "timestamp": "2024-02-27T10:00:00Z",
            "status": "confirmed",
            "assets": assets_confirmed,
            "total_value_usd": total_value,
            "custodian": "BitGo",
            "signature": "0xabcdef123456",
        }

    @staticmethod
    def segregation_confirmation_response(
        confirmation_id: str,
        segregated: bool = True,
    ) -> Dict[str, Any]:
        """Mock asset segregation confirmation response."""
        return {
            "confirmation_id": confirmation_id,
            "segregated": segregated,
            "customer_assets_account": "ACC-12345-CUST",
            "operational_assets_account": "ACC-12345-OPS",
            "timestamp": "2024-02-27T10:00:00Z",
            "confirmed_by": "Custodian Legal",
        }
