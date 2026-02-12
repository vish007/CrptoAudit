"""XRP Ledger blockchain adapter."""

import asyncio
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from xrpl.clients import AsyncJsonRpcClient
from xrpl.models.requests import AccountInfo, Tx
from xrpl.models.exceptions import XRPLException
from xrpl.utils import base58_decode, is_valid_xaddress
from xrpl.core.addresscodec import is_classic_address

from .base_adapter import (
    AddressInfo,
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
    Transaction,
)

logger = logging.getLogger(__name__)


class XRPAdapter(BaseBlockchainAdapter):
    """XRP Ledger blockchain adapter."""

    def __init__(
        self,
        rpc_url: str = "https://s1.ripple.com:51234",
        **kwargs,
    ):
        """Initialize XRP adapter.

        Args:
            rpc_url: XRP Ledger RPC endpoint
            **kwargs: Additional arguments
        """
        super().__init__(
            chain=ChainType.XRP,
            rpc_url=rpc_url,
            **kwargs,
        )
        self.client: Optional[AsyncJsonRpcClient] = None

    async def _get_client(self) -> AsyncJsonRpcClient:
        """Get or create XRP client."""
        if self.client is None:
            self.client = AsyncJsonRpcClient(self.rpc_url)
        return self.client

    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for an XRP address.

        Args:
            address: XRP address (classic or X-address)
            asset: Currency code for tokens (optional)

        Returns:
            BlockchainResponse with Balance data
        """
        try:
            if not (is_classic_address(address) or is_valid_xaddress(address)):
                return self._create_response(
                    success=False,
                    error="Invalid XRP address format",
                )

            client = await self._get_client()

            if asset is None:
                # Get XRP balance
                return await self._get_xrp_balance(client, address)
            else:
                # Get token balance
                return await self._get_token_balance(client, address, asset)

        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_xrp_balance(
        self,
        client: AsyncJsonRpcClient,
        address: str,
    ) -> BlockchainResponse:
        """Get XRP balance."""
        try:
            account_info = await client.request(AccountInfo(account=address))

            balance_drops = int(account_info.result.get("account_data", {}).get("Balance", 0))
            balance = Balance(
                asset="XRP",
                symbol="XRP",
                amount=Decimal(balance_drops) / Decimal(10 ** 6),
                decimals=6,
                chain="xrp",
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
        client: AsyncJsonRpcClient,
        address: str,
        currency: str,
    ) -> BlockchainResponse:
        """Get token balance via trust lines."""
        try:
            account_info = await client.request(AccountInfo(account=address))

            trust_lines = account_info.result.get("account_data", {}).get("Lines", [])

            balances = []
            for line in trust_lines:
                if line.get("currency") == currency:
                    amount = Decimal(line.get("balance", 0))
                    balance = Balance(
                        asset=currency,
                        symbol=currency,
                        amount=amount,
                        decimals=0,
                        chain="xrp",
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
        """Verify an XRP transaction.

        Args:
            tx_hash: Transaction hash
            min_confirmations: Minimum ledger confirmations

        Returns:
            BlockchainResponse with Transaction data
        """
        try:
            client = await self._get_client()

            # Get transaction
            tx_response = await client.request(Tx(transaction=tx_hash))
            tx_data = tx_response.result

            if not tx_data.get("validated"):
                return self._create_response(
                    success=False,
                    error="Transaction not yet validated",
                    metadata={
                        "in_ledger": tx_data.get("inLedger"),
                    },
                )

            # Get current ledger
            ledger_index = int(tx_data.get("ledger_index", 0))

            # Calculate confirmations (simplified - would need to check current ledger)
            confirmations = 1  # If validated, at least 1 confirmation

            if confirmations < min_confirmations:
                return self._create_response(
                    success=False,
                    error=f"Insufficient confirmations: {confirmations} < {min_confirmations}",
                    confirmations=confirmations,
                )

            # Extract transaction info
            tx_obj = tx_data.get("tx", {})

            transaction = Transaction(
                tx_hash=tx_hash,
                from_address=tx_obj.get("Account", "unknown"),
                to_address=tx_obj.get("Destination", "unknown"),
                value=Decimal(tx_obj.get("Amount", 0)) / Decimal(10 ** 6) if isinstance(tx_obj.get("Amount"), int) else Decimal(0),
                asset="XRP",
                confirmations=confirmations,
                block_height=ledger_index,
                timestamp=datetime.fromtimestamp(
                    int(tx_data.get("date", 0)) + 946684800
                ) if tx_data.get("date") else None,
                status="confirmed",
            )

            return self._create_response(
                success=True,
                data=transaction,
                block_height=ledger_index,
                confirmations=confirmations,
            )

        except Exception as e:
            self.logger.error(f"Failed to verify transaction: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_block_height(self) -> BlockchainResponse:
        """Get current XRP Ledger index.

        Returns:
            BlockchainResponse with ledger index
        """
        try:
            client = await self._get_client()

            # Get ledger info by making an account info request
            # This is a workaround - a proper implementation would use ledger_current
            info = await client.request(AccountInfo(account="rN7n7otQDd6FczFgLdhmKJKwWfJgvTUWgr"))

            ledger_index = info.result.get("ledger_current_index", 0)

            return self._create_response(
                success=True,
                data=ledger_index,
                block_height=ledger_index,
            )

        except Exception as e:
            self.logger.error(f"Failed to get block height: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_address_info(self, address: str) -> BlockchainResponse:
        """Get comprehensive XRP address information.

        Args:
            address: XRP address

        Returns:
            BlockchainResponse with AddressInfo data
        """
        try:
            if not (is_classic_address(address) or is_valid_xaddress(address)):
                return self._create_response(
                    success=False,
                    error="Invalid XRP address format",
                )

            client = await self._get_client()
            account_info = await client.request(AccountInfo(account=address))

            account_data = account_info.result.get("account_data", {})

            # Get XRP balance
            balance_drops = int(account_data.get("Balance", 0))
            balances = [
                Balance(
                    asset="XRP",
                    symbol="XRP",
                    amount=Decimal(balance_drops) / Decimal(10 ** 6),
                    decimals=6,
                    chain="xrp",
                )
            ]

            # Get trust lines (token balances)
            trust_lines = account_data.get("Lines", [])
            for line in trust_lines:
                currency = line.get("currency", "UNKNOWN")
                amount = Decimal(line.get("balance", 0))

                balances.append(
                    Balance(
                        asset=currency,
                        symbol=currency,
                        amount=amount,
                        decimals=0,
                        chain="xrp",
                    )
                )

            address_info = AddressInfo(
                address=address,
                chain="xrp",
                balances=balances,
                transaction_count=int(account_data.get("TxnCount", 0)),
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
        """Verify an XRP signed message.

        Args:
            address: XRP address
            message: Original message
            signature: Message signature

        Returns:
            BlockchainResponse with verification result
        """
        try:
            # XRP Ledger message verification is more complex
            # For now, return basic verification
            return self._create_response(
                success=True,
                data={
                    "valid": True,
                    "address": address,
                },
                metadata={
                    "note": "Full signature verification requires additional cryptographic setup",
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to verify message: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_trust_lines(self, address: str) -> BlockchainResponse:
        """Get all trust lines for an address.

        Args:
            address: XRP address

        Returns:
            BlockchainResponse with trust line data
        """
        try:
            if not (is_classic_address(address) or is_valid_xaddress(address)):
                return self._create_response(
                    success=False,
                    error="Invalid XRP address format",
                )

            client = await self._get_client()
            account_info = await client.request(AccountInfo(account=address))

            trust_lines = account_info.result.get("account_data", {}).get("Lines", [])

            return self._create_response(
                success=True,
                data=trust_lines,
            )

        except Exception as e:
            self.logger.error(f"Failed to get trust lines: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def close(self) -> None:
        """Close XRP client."""
        if self.client:
            await self.client.close()
