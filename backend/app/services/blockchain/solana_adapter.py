"""Solana blockchain adapter."""

import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
import aiohttp
from solders.publickey import PublicKey
from solders.signature import Signature
from solders.transaction import Transaction as SolanaTransaction

from .base_adapter import (
    AddressInfo,
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
    Transaction,
)

logger = logging.getLogger(__name__)


class SolanaAdapter(BaseBlockchainAdapter):
    """Solana blockchain adapter."""

    # Known token mints
    SOLANA_TOKENS = {
        "EPjFWaJwT2KeW5B7GtZCvEL5qb9d5PchppyMHrVWKF7j": {
            "symbol": "USDC",
            "decimals": 6,
            "name": "USD Coin",
        },
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenEsl": {
            "symbol": "USDT",
            "decimals": 6,
            "name": "Tether USD",
        },
        "MangoCzJ36AjZyKwVj3VnYU4GTonjfVEnJmvvWaxLac": {
            "symbol": "MNGO",
            "decimals": 6,
            "name": "Mango",
        },
    }

    # Staking program ID
    SOLANA_STAKE_PROGRAM = "Stake11111111111111111111111111111111111111"

    def __init__(
        self,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        **kwargs,
    ):
        """Initialize Solana adapter.

        Args:
            rpc_url: Solana RPC endpoint
            **kwargs: Additional arguments
        """
        super().__init__(
            chain=ChainType.SOLANA,
            rpc_url=rpc_url,
            **kwargs,
        )
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _make_rpc_call(self, method: str, params: List[Any]) -> Dict[str, Any]:
        """Make JSON-RPC call to Solana.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            RPC response
        """
        session = await self._get_session()

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        async with session.post(
            self.rpc_url,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            if resp.status != 200:
                raise RuntimeError(f"RPC error: {resp.status}")

            data = await resp.json()

            if "error" in data:
                raise RuntimeError(f"RPC error: {data['error']}")

            return data.get("result")

    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for a Solana address.

        Args:
            address: Solana address (base58)
            asset: SPL token mint address (optional)

        Returns:
            BlockchainResponse with Balance data
        """
        try:
            if not self._validate_address(address):
                return self._create_response(
                    success=False,
                    error="Invalid Solana address",
                )

            if asset is None:
                # Get SOL balance
                return await self._get_sol_balance(address)
            else:
                # Get SPL token balance
                return await self._get_token_balance(address, asset)

        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_sol_balance(self, address: str) -> BlockchainResponse:
        """Get SOL balance."""
        try:
            balance_lamports = await self._make_rpc_call(
                "getBalance",
                [address],
            )

            balance = Balance(
                asset="SOL",
                symbol="SOL",
                amount=Decimal(balance_lamports) / Decimal(10 ** 9),
                decimals=9,
                chain="solana",
            )

            return self._create_response(
                success=True,
                data=[balance],
            )
        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_token_balance(
        self,
        address: str,
        mint: str,
    ) -> BlockchainResponse:
        """Get SPL token balance."""
        try:
            # Get token accounts for this wallet
            accounts = await self._make_rpc_call(
                "getTokenAccountsByOwner",
                [
                    address,
                    {"mint": mint},
                    {"encoding": "jsonParsed"},
                ],
            )

            if not accounts.get("value"):
                return self._create_response(
                    success=True,
                    data=[],
                )

            balances = []
            for account_info in accounts.get("value", []):
                parsed = account_info.get("account", {}).get("data", {}).get("parsed", {})
                token_info = parsed.get("info", {})

                amount = Decimal(token_info.get("tokenAmount", {}).get("amount", 0))
                decimals = token_info.get("tokenAmount", {}).get("decimals", 0)

                token_data = self.SOLANA_TOKENS.get(mint, {})

                balance = Balance(
                    asset=mint,
                    symbol=token_data.get("symbol", "UNKNOWN"),
                    amount=amount / Decimal(10 ** decimals),
                    decimals=decimals,
                    contract_address=mint,
                    chain="solana",
                )

                balances.append(balance)

            return self._create_response(
                success=True,
                data=balances,
            )

        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def verify_transaction(
        self,
        tx_hash: str,
        min_confirmations: int = 0,
    ) -> BlockchainResponse:
        """Verify a Solana transaction.

        Args:
            tx_hash: Transaction signature
            min_confirmations: Minimum confirmations required

        Returns:
            BlockchainResponse with Transaction data
        """
        try:
            # Get transaction
            tx_data = await self._make_rpc_call(
                "getTransaction",
                [tx_hash, {"encoding": "jsonParsed"}],
            )

            if not tx_data:
                return self._create_response(
                    success=False,
                    error="Transaction not found",
                )

            # Get slot and confirmations
            slot = tx_data.get("slot")

            current_slot = await self._make_rpc_call("getSlot", [])
            confirmations = current_slot - slot

            if confirmations < min_confirmations:
                return self._create_response(
                    success=False,
                    error=f"Insufficient confirmations: {confirmations} < {min_confirmations}",
                    confirmations=confirmations,
                )

            # Extract transaction data
            message = tx_data.get("transaction", {}).get("message", {})
            instructions = message.get("instructions", [])

            transaction = Transaction(
                tx_hash=tx_hash,
                from_address=message.get("accountKeys", [{}])[0] if message.get("accountKeys") else "unknown",
                to_address=message.get("accountKeys", [{}, {}])[1] if len(message.get("accountKeys", [])) > 1 else "unknown",
                value=Decimal(0),  # Would need to parse instruction data
                asset="SOL",
                confirmations=confirmations,
                block_height=slot,
                timestamp=datetime.fromtimestamp(tx_data.get("blockTime", 0)) if tx_data.get("blockTime") else None,
                status="confirmed" if tx_data.get("meta", {}).get("err") is None else "failed",
            )

            return self._create_response(
                success=True,
                data=transaction,
                confirmations=confirmations,
            )

        except Exception as e:
            self.logger.error(f"Failed to verify transaction: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_block_height(self) -> BlockchainResponse:
        """Get current Solana slot (block height).

        Returns:
            BlockchainResponse with slot number
        """
        try:
            slot = await self._make_rpc_call("getSlot", [])

            return self._create_response(
                success=True,
                data=slot,
                block_height=slot,
            )

        except Exception as e:
            self.logger.error(f"Failed to get block height: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_address_info(self, address: str) -> BlockchainResponse:
        """Get comprehensive Solana address information.

        Args:
            address: Solana address

        Returns:
            BlockchainResponse with AddressInfo data
        """
        try:
            if not self._validate_address(address):
                return self._create_response(
                    success=False,
                    error="Invalid Solana address",
                )

            # Get SOL balance
            balance_lamports = await self._make_rpc_call(
                "getBalance",
                [address],
            )

            balances = [
                Balance(
                    asset="SOL",
                    symbol="SOL",
                    amount=Decimal(balance_lamports) / Decimal(10 ** 9),
                    decimals=9,
                    chain="solana",
                )
            ]

            # Get account info
            account_info = await self._make_rpc_call(
                "getAccountInfo",
                [address, {"encoding": "jsonParsed"}],
            )

            address_info = AddressInfo(
                address=address,
                chain="solana",
                balances=balances,
                transaction_count=0,  # Would need to scan history
                is_contract=False,
            )

            return self._create_response(
                success=True,
                data=address_info,
            )

        except Exception as e:
            self.logger.error(f"Failed to get address info: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def verify_signed_message(
        self,
        address: str,
        message: str,
        signature: str,
    ) -> BlockchainResponse:
        """Verify a Solana signed message.

        Args:
            address: Solana address
            message: Original message
            signature: Message signature (base58)

        Returns:
            BlockchainResponse with verification result
        """
        try:
            # Decode signature and public key
            try:
                sig_bytes = bytes.fromhex(signature)
            except:
                import base58
                sig_bytes = base58.b58decode(signature)

            pub_key = PublicKey(address)
            sig = Signature(sig_bytes)

            # Verify signature
            message_bytes = message.encode()

            pub_key.verify(sig, message_bytes)

            return self._create_response(
                success=True,
                data={
                    "valid": True,
                    "address": address,
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to verify message: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_staking_info(self, address: str) -> BlockchainResponse:
        """Get Solana staking information.

        Args:
            address: Solana address

        Returns:
            BlockchainResponse with staking data
        """
        try:
            # Get stake accounts
            stake_accounts = await self._make_rpc_call(
                "getProgramAccounts",
                [
                    self.SOLANA_STAKE_PROGRAM,
                    {
                        "filters": [
                            {
                                "memcmp": {
                                    "offset": 12,
                                    "bytes": address,
                                }
                            }
                        ],
                        "encoding": "jsonParsed",
                    },
                ],
            )

            total_staked = Decimal(0)
            stake_accounts_list = []

            for account in stake_accounts:
                try:
                    parsed = account.get("account", {}).get("data", {}).get("parsed", {})
                    stake = parsed.get("info", {}).get("stake", {})
                    delegation = stake.get("delegation", {})

                    amount = Decimal(stake.get("lamports", 0)) / Decimal(10 ** 9)
                    total_staked += amount

                    stake_accounts_list.append({
                        "pubkey": account.get("pubkey"),
                        "amount_sol": float(amount),
                        "delegated_to": delegation.get("voter"),
                    })
                except:
                    continue

            return self._create_response(
                success=True,
                data={
                    "total_staked_sol": float(total_staked),
                    "stake_accounts": stake_accounts_list,
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to get staking info: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    def _validate_address(self, address: str) -> bool:
        """Validate Solana address format.

        Args:
            address: Solana address

        Returns:
            True if valid, False otherwise
        """
        try:
            PublicKey(address)
            return True
        except:
            return False

    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
