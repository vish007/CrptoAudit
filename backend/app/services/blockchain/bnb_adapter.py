"""BNB Chain blockchain adapter."""

import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from eth_utils import is_checksum_address, to_checksum_address
from web3 import Web3

from .base_adapter import (
    AddressInfo,
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
    Transaction,
)

logger = logging.getLogger(__name__)

# BEP-20 ABI (same as ERC-20)
BEP20_ABI = json.loads("""[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]""")

# BNB Staking ABI (simplified)
STAKING_ABI = json.loads("""[
    {
        "inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
        "name": "getStakingInfo",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "type": "function"
    }
]""")


class BNBAdapter(BaseBlockchainAdapter):
    """BNB Chain blockchain adapter."""

    CHAIN_CONFIG = {
        "name": "BNB Chain",
        "chain_id": 56,
        "default_rpc": "https://bsc-dataseed1.binance.org",
    }

    # Known BNB staking contracts
    BINANCE_STAKING = "0x1688a712fc040cd619b2831a8c61b9b690de4de2"

    def __init__(
        self,
        rpc_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize BNB Chain adapter.

        Args:
            rpc_url: Custom RPC URL
            **kwargs: Additional arguments
        """
        super().__init__(
            chain=ChainType.BNB_CHAIN,
            rpc_url=rpc_url or self.CHAIN_CONFIG["default_rpc"],
            **kwargs,
        )

        # Initialize Web3
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.web3.is_connected():
            self.logger.warning(f"Web3 not connected to {self.rpc_url}")

    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for a BNB address.

        Args:
            address: BNB address
            asset: Token contract address (optional)

        Returns:
            BlockchainResponse with Balance data
        """
        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            if asset is None:
                # Get native BNB balance
                return await self._get_bnb_balance(address)
            else:
                # Get BEP-20 token balance
                return await self._get_token_balance(address, asset)

        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_bnb_balance(self, address: str) -> BlockchainResponse:
        """Get native BNB balance."""
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance = Balance(
                asset="BNB",
                symbol="BNB",
                amount=Decimal(balance_wei) / Decimal(10 ** 18),
                decimals=18,
                chain="bnb_chain",
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
        token_address: str,
    ) -> BlockchainResponse:
        """Get BEP-20 token balance."""
        try:
            if not is_checksum_address(token_address):
                token_address = to_checksum_address(token_address)

            contract = self.web3.eth.contract(
                address=token_address,
                abi=BEP20_ABI,
            )

            # Get balance and decimals
            balance_raw = contract.functions.balanceOf(address).call()
            decimals = contract.functions.decimals().call()
            symbol = contract.functions.symbol().call()

            balance = Balance(
                asset=token_address,
                symbol=symbol,
                amount=Decimal(balance_raw) / Decimal(10 ** decimals),
                decimals=decimals,
                contract_address=token_address,
                chain="bnb_chain",
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

    async def verify_transaction(
        self,
        tx_hash: str,
        min_confirmations: int = 0,
    ) -> BlockchainResponse:
        """Verify a BNB transaction.

        Args:
            tx_hash: Transaction hash
            min_confirmations: Minimum confirmations required

        Returns:
            BlockchainResponse with Transaction data
        """
        try:
            # Get transaction
            tx = self.web3.eth.get_transaction(tx_hash)
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)

            # Get current block height
            current_block = self.web3.eth.block_number
            confirmations = current_block - receipt.blockNumber

            # Validate confirmations
            if confirmations < min_confirmations:
                return self._create_response(
                    success=False,
                    error=f"Insufficient confirmations: {confirmations} < {min_confirmations}",
                    block_height=current_block,
                    confirmations=confirmations,
                )

            # Create transaction object
            transaction = Transaction(
                tx_hash=tx_hash,
                from_address=tx["from"],
                to_address=tx["to"],
                value=Decimal(tx["value"]) / Decimal(10 ** 18),
                asset="BNB",
                confirmations=confirmations,
                block_height=receipt.blockNumber,
                timestamp=datetime.fromtimestamp(
                    self.web3.eth.get_block(receipt.blockNumber).timestamp
                ),
                gas_used=receipt.gasUsed,
                status="confirmed" if receipt.status == 1 else "failed",
            )

            return self._create_response(
                success=True,
                data=transaction,
                block_height=current_block,
                confirmations=confirmations,
            )

        except Exception as e:
            self.logger.error(f"Failed to verify transaction: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_block_height(self) -> BlockchainResponse:
        """Get current BNB block height.

        Returns:
            BlockchainResponse with block height
        """
        try:
            block_height = self.web3.eth.block_number

            return self._create_response(
                success=True,
                data=block_height,
                block_height=block_height,
            )
        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_address_info(self, address: str) -> BlockchainResponse:
        """Get comprehensive BNB address information.

        Args:
            address: BNB address

        Returns:
            BlockchainResponse with AddressInfo data
        """
        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            # Get native balance
            balance_wei = self.web3.eth.get_balance(address)
            balances = [
                Balance(
                    asset="BNB",
                    symbol="BNB",
                    amount=Decimal(balance_wei) / Decimal(10 ** 18),
                    decimals=18,
                    chain="bnb_chain",
                )
            ]

            # Get transaction count
            tx_count = self.web3.eth.get_transaction_count(address)

            # Check if contract
            code = self.web3.eth.get_code(address)
            is_contract = len(code) > 0

            address_info = AddressInfo(
                address=address,
                chain="bnb_chain",
                balances=balances,
                transaction_count=tx_count,
                is_contract=is_contract,
            )

            return self._create_response(
                success=True,
                data=address_info,
            )
        except Exception as e:
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
        """Verify a BNB signed message (EIP-191).

        Args:
            address: Expected signer address
            message: Original message
            signature: Message signature (hex string)

        Returns:
            BlockchainResponse with verification result
        """
        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            # Recover address from signature
            from eth_account.messages import encode_defunct
            message_hash = encode_defunct(text=message)

            recovered_address = self.web3.eth.account.recover_message(
                message_hash,
                signature=signature,
            )

            # Normalize and compare
            recovered_address = to_checksum_address(recovered_address)
            is_valid = recovered_address.lower() == address.lower()

            return self._create_response(
                success=is_valid,
                data={
                    "valid": is_valid,
                    "recovered_address": recovered_address,
                    "expected_address": address,
                },
            )
        except Exception as e:
            self.logger.error(f"Failed to verify message: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_bnb_staking(self, address: str) -> BlockchainResponse:
        """Get BNB staking information.

        Args:
            address: BNB address

        Returns:
            BlockchainResponse with staking data
        """
        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            # Query staking contract
            staking_contract = self.web3.eth.contract(
                address=to_checksum_address(self.BINANCE_STAKING),
                abi=STAKING_ABI,
            )

            try:
                staked_amount = staking_contract.functions.getStakingInfo(address).call()

                return self._create_response(
                    success=True,
                    data={
                        "staked_bnb": Decimal(staked_amount) / Decimal(10 ** 18),
                    },
                )
            except:
                # If staking contract call fails, return zero
                return self._create_response(
                    success=True,
                    data={
                        "staked_bnb": Decimal(0),
                    },
                )

        except Exception as e:
            self.logger.error(f"Failed to get staking info: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def estimate_gas(
        self,
        from_address: str,
        to_address: str,
        value: int = 0,
        data: Optional[str] = None,
    ) -> BlockchainResponse:
        """Estimate gas for a transaction.

        Args:
            from_address: Sender address
            to_address: Recipient address
            value: Value in wei
            data: Call data (optional)

        Returns:
            BlockchainResponse with gas estimate
        """
        try:
            estimate = self.web3.eth.estimate_gas({
                "from": from_address,
                "to": to_address,
                "value": value,
                "data": data or "0x",
            })

            return self._create_response(
                success=True,
                data=estimate,
            )
        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )
