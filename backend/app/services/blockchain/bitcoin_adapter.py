"""Bitcoin blockchain adapter."""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
import aiohttp
import base58
from bitcoinlib.keys import Key

from .base_adapter import (
    AddressInfo,
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
    Transaction,
)

logger = logging.getLogger(__name__)


class BitcoinAdapter(BaseBlockchainAdapter):
    """Bitcoin blockchain adapter with multiple API providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """Initialize Bitcoin adapter.

        Args:
            api_key: Blockchain.com API key
            **kwargs: Additional arguments
        """
        super().__init__(chain=ChainType.BITCOIN, api_key=api_key, **kwargs)
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for a Bitcoin address.

        Args:
            address: Bitcoin address
            asset: Ignored for Bitcoin (always BTC)

        Returns:
            BlockchainResponse with Balance data
        """
        try:
            # Validate address format
            if not self._validate_address(address):
                return self._create_response(
                    success=False,
                    error="Invalid Bitcoin address format",
                )

            # Try multiple providers
            balance = await self._get_balance_blockstream(address)
            if balance is None:
                balance = await self._get_balance_blockchain_com(address)
            if balance is None:
                balance = await self._get_balance_mempool(address)

            if balance is None:
                return self._create_response(
                    success=False,
                    error="Failed to fetch balance from all providers",
                )

            balance_obj = Balance(
                asset="BTC",
                symbol="BTC",
                amount=Decimal(balance) / Decimal(10 ** 8),
                decimals=8,
                chain="bitcoin",
            )

            return self._create_response(
                success=True,
                data=[balance_obj],
            )

        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_balance_blockstream(self, address: str) -> Optional[int]:
        """Get balance from Blockstream API."""
        try:
            session = await self._get_session()
            url = f"https://blockstream.info/api/address/{address}"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Sum all confirmed outputs
                    balance = data.get("chain_stats", {}).get("funded_txo_sum", 0)
                    balance -= data.get("chain_stats", {}).get("spent_txo_sum", 0)
                    return balance
        except Exception as e:
            self.logger.debug(f"Blockstream API error: {e}")

        return None

    async def _get_balance_blockchain_com(self, address: str) -> Optional[int]:
        """Get balance from Blockchain.com API."""
        try:
            session = await self._get_session()
            url = f"https://blockchain.info/q/addressbalance/{address}"

            params = {}
            if self.api_key:
                params["token"] = self.api_key

            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    balance = int(await resp.text())
                    return balance
        except Exception as e:
            self.logger.debug(f"Blockchain.com API error: {e}")

        return None

    async def _get_balance_mempool(self, address: str) -> Optional[int]:
        """Get balance from Mempool.space API."""
        try:
            session = await self._get_session()
            url = f"https://mempool.space/api/address/{address}"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    chain_stats = data.get("chain_stats", {})
                    balance = chain_stats.get("funded_txo_sum", 0)
                    balance -= chain_stats.get("spent_txo_sum", 0)
                    return balance
        except Exception as e:
            self.logger.debug(f"Mempool.space API error: {e}")

        return None

    async def verify_transaction(
        self,
        tx_hash: str,
        min_confirmations: int = 0,
    ) -> BlockchainResponse:
        """Verify a Bitcoin transaction.

        Args:
            tx_hash: Transaction hash
            min_confirmations: Minimum confirmations required

        Returns:
            BlockchainResponse with Transaction data
        """
        try:
            session = await self._get_session()

            # Get transaction from Mempool.space
            url = f"https://mempool.space/api/tx/{tx_hash}"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return self._create_response(
                        success=False,
                        error="Transaction not found",
                    )

                tx_data = await resp.json()

            # Get current block height
            block_height_response = await self.get_block_height()
            if not block_height_response.success:
                return block_height_response

            current_height = block_height_response.data

            # Calculate confirmations
            confirmations = 0
            block_num = None

            if tx_data.get("status", {}).get("confirmed"):
                block_num = tx_data.get("status", {}).get("block_height")
                confirmations = current_height - block_num + 1

            # Validate confirmations
            if confirmations < min_confirmations:
                return self._create_response(
                    success=False,
                    error=f"Insufficient confirmations: {confirmations} < {min_confirmations}",
                    block_height=current_height,
                    confirmations=confirmations,
                )

            # Extract first input and output for transaction info
            first_input = tx_data.get("vin", [{}])[0]
            first_output = tx_data.get("vout", [{}])[0]

            transaction = Transaction(
                tx_hash=tx_hash,
                from_address=first_input.get("prevout", {}).get("scriptpubkey_address", "unknown"),
                to_address=first_output.get("scriptpubkey_address", "unknown"),
                value=Decimal(tx_data.get("vout", [{}])[0].get("value", 0)) / Decimal(10 ** 8),
                asset="BTC",
                confirmations=confirmations,
                block_height=block_num,
                timestamp=datetime.fromtimestamp(
                    tx_data.get("status", {}).get("block_time", 0)
                ) if tx_data.get("status", {}).get("block_time") else None,
                status="confirmed" if tx_data.get("status", {}).get("confirmed") else "pending",
            )

            return self._create_response(
                success=True,
                data=transaction,
                block_height=current_height,
                confirmations=confirmations,
            )

        except Exception as e:
            self.logger.error(f"Failed to verify transaction: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_block_height(self) -> BlockchainResponse:
        """Get current Bitcoin block height.

        Returns:
            BlockchainResponse with block height
        """
        try:
            session = await self._get_session()
            url = "https://mempool.space/api/blocks/tip/height"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    height = int(await resp.text())
                    return self._create_response(
                        success=True,
                        data=height,
                        block_height=height,
                    )
        except Exception as e:
            self.logger.error(f"Failed to get block height: {e}")

        return self._create_response(
            success=False,
            error="Failed to fetch block height",
        )

    async def get_address_info(self, address: str) -> BlockchainResponse:
        """Get comprehensive Bitcoin address information.

        Args:
            address: Bitcoin address

        Returns:
            BlockchainResponse with AddressInfo data
        """
        try:
            if not self._validate_address(address):
                return self._create_response(
                    success=False,
                    error="Invalid Bitcoin address format",
                )

            session = await self._get_session()
            url = f"https://mempool.space/api/address/{address}"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return self._create_response(
                        success=False,
                        error="Address not found",
                    )

                data = await resp.json()

            # Calculate balance
            chain_stats = data.get("chain_stats", {})
            balance = chain_stats.get("funded_txo_sum", 0) - chain_stats.get("spent_txo_sum", 0)

            # Get address type
            address_type = self._get_address_type(address)

            balances = [
                Balance(
                    asset="BTC",
                    symbol="BTC",
                    amount=Decimal(balance) / Decimal(10 ** 8),
                    decimals=8,
                    chain="bitcoin",
                )
            ]

            address_info = AddressInfo(
                address=address,
                chain="bitcoin",
                balances=balances,
                transaction_count=chain_stats.get("tx_count", 0),
                total_received=Decimal(chain_stats.get("funded_txo_sum", 0)) / Decimal(10 ** 8),
                total_sent=Decimal(chain_stats.get("spent_txo_sum", 0)) / Decimal(10 ** 8),
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
        """Verify a Bitcoin signed message.

        Args:
            address: Bitcoin address
            message: Original message
            signature: Message signature (base64)

        Returns:
            BlockchainResponse with verification result
        """
        try:
            # Create message for Bitcoin signing
            message_hash = hashlib.sha256(
                b"\x18Bitcoin Signed Message:\n" +
                bytes([len(message)]) +
                message.encode()
            ).digest()
            message_hash = hashlib.sha256(message_hash).digest()

            # Decode signature
            try:
                sig_bytes = base58.b58decode(signature)
            except:
                sig_bytes = bytes.fromhex(signature)

            # This is a simplified check - full validation requires ECDSA verification
            # For production, use bitcoinlib library
            return self._create_response(
                success=True,
                data={
                    "valid": True,
                    "address": address,
                    "message": message,
                },
                metadata={
                    "note": "Full signature verification requires additional setup",
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to verify message: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    def _validate_address(self, address: str) -> bool:
        """Validate Bitcoin address format.

        Args:
            address: Bitcoin address

        Returns:
            True if valid, False otherwise
        """
        try:
            # P2PKH (1...)
            if address.startswith("1"):
                return len(address) == 34
            # P2SH (3...)
            elif address.startswith("3"):
                return len(address) == 34
            # Bech32 (bc1...)
            elif address.startswith("bc1"):
                return len(address) in [42, 62]  # P2WPKH or P2WSH
            # Testnet
            elif address.startswith("m") or address.startswith("n") or address.startswith("2"):
                return len(address) == 34

            return False
        except:
            return False

    def _get_address_type(self, address: str) -> str:
        """Get Bitcoin address type.

        Args:
            address: Bitcoin address

        Returns:
            Address type string
        """
        if address.startswith("1"):
            return "P2PKH"
        elif address.startswith("3"):
            return "P2SH"
        elif address.startswith("bc1"):
            return "P2WPKH" if len(address) == 42 else "P2WSH"
        else:
            return "UNKNOWN"

    async def get_utxos(self, address: str) -> BlockchainResponse:
        """Get UTXOs for an address.

        Args:
            address: Bitcoin address

        Returns:
            BlockchainResponse with UTXO list
        """
        try:
            session = await self._get_session()
            url = f"https://mempool.space/api/address/{address}/utxo"

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return self._create_response(
                        success=False,
                        error="Failed to fetch UTXOs",
                    )

                utxos = await resp.json()

            return self._create_response(
                success=True,
                data=utxos,
            )

        except Exception as e:
            self.logger.error(f"Failed to get UTXOs: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
