"""Ethereum and EVM-compatible blockchain adapter."""

import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from eth_account.messages import encode_defunct
from eth_keys import keys
from eth_typing import ChecksumAddress
from eth_utils import is_checksum_address, to_checksum_address
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import BlockNotFound, TransactionNotFound, ValidationError

from .base_adapter import (
    AddressInfo,
    AssetType,
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
    Transaction,
)

logger = logging.getLogger(__name__)

# Standard ERC-20 ABI for balance checking
ERC20_ABI = json.loads("""[
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

# Aave V3 Pool ABI (simplified)
AAVE_POOL_ABI = json.loads("""[
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"name": "totalCollateralBase", "type": "uint256"},
            {"name": "totalDebtBase", "type": "uint256"},
            {"name": "availableBorrowsBase", "type": "uint256"},
            {"name": "currentLiquidationThreshold", "type": "uint256"},
            {"name": "ltv", "type": "uint256"},
            {"name": "healthFactor", "type": "uint256"}
        ],
        "type": "function"
    }
]""")

# Uniswap V3 Position Manager ABI (simplified)
UNISWAP_V3_ABI = json.loads("""[
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "positions",
        "outputs": [
            {"name": "nonce", "type": "uint96"},
            {"name": "operator", "type": "address"},
            {"name": "token0", "type": "address"},
            {"name": "token1", "type": "address"},
            {"name": "fee", "type": "uint24"},
            {"name": "tickLower", "type": "int24"},
            {"name": "tickUpper", "type": "int24"},
            {"name": "liquidity", "type": "uint128"},
            {"name": "feeGrowthInside0LastX128", "type": "uint256"},
            {"name": "feeGrowthInside1LastX128", "type": "uint256"},
            {"name": "tokensOwed0", "type": "uint128"},
            {"name": "tokensOwed1", "type": "uint128"}
        ],
        "type": "function"
    }
]""")


class EthereumAdapter(BaseBlockchainAdapter):
    """Ethereum and EVM-compatible blockchain adapter."""

    # Chain configurations
    CHAIN_CONFIGS = {
        ChainType.ETHEREUM: {
            "name": "Ethereum Mainnet",
            "chain_id": 1,
            "default_rpc": "https://eth-mainnet.g.alchemy.com/v2/demo",
            "block_time": 12,
        },
        ChainType.ARBITRUM: {
            "name": "Arbitrum One",
            "chain_id": 42161,
            "default_rpc": "https://arb-mainnet.g.alchemy.com/v2/demo",
            "block_time": 0.5,
        },
        ChainType.OPTIMISM: {
            "name": "Optimism",
            "chain_id": 10,
            "default_rpc": "https://opt-mainnet.g.alchemy.com/v2/demo",
            "block_time": 2,
        },
        ChainType.POLYGON: {
            "name": "Polygon",
            "chain_id": 137,
            "default_rpc": "https://polygon-mainnet.g.alchemy.com/v2/demo",
            "block_time": 2,
        },
        ChainType.BASE: {
            "name": "Base",
            "chain_id": 8453,
            "default_rpc": "https://base-mainnet.g.alchemy.com/v2/demo",
            "block_time": 2,
        },
    }

    # Known protocol addresses
    AAVE_V3_POOLS = {
        ChainType.ETHEREUM: "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
        ChainType.ARBITRUM: "0x794a61358D6845106d5b7a8520A8f7d147B8d9DE",
        ChainType.POLYGON: "0x794a61358D6845106d5b7a8520A8f7d147B8d9DE",
    }

    LIDO_STETH = {
        ChainType.ETHEREUM: "0xae7ab96520DE3A18E5e111B5eaAb095312D7fE84",
    }

    UNISWAP_V3_POSITION_MANAGER = {
        ChainType.ETHEREUM: "0xC36442b4a4522E871399CD717aBDD847Ab11218e",
        ChainType.ARBITRUM: "0xC36442b4a4522E871399CD717aBDD847Ab11218e",
        ChainType.POLYGON: "0xC36442b4a4522E871399CD717aBDD847Ab11218e",
    }

    def __init__(
        self,
        chain: ChainType,
        api_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize Ethereum adapter.

        Args:
            chain: EVM chain type
            api_key: Alchemy/Infura API key
            rpc_url: Custom RPC URL
            **kwargs: Additional arguments
        """
        if chain not in self.CHAIN_CONFIGS:
            raise ValueError(f"Unsupported chain: {chain}")

        super().__init__(chain=chain, api_key=api_key, rpc_url=rpc_url, **kwargs)

        # Initialize Web3
        config = self.CHAIN_CONFIGS[chain]
        endpoint = rpc_url or config["default_rpc"]

        self.web3 = Web3(Web3.HTTPProvider(endpoint))
        self.chain_config = config

        if not self.web3.is_connected():
            self.logger.warning(f"Web3 not connected to {endpoint}")

    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for an address.

        Args:
            address: Ethereum address
            asset: Specific token contract address (optional)

        Returns:
            BlockchainResponse with Balance data
        """
        try:
            # Normalize address
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            if asset is None:
                # Get native ETH balance
                return await self._get_native_balance(address)
            else:
                # Get ERC-20 token balance
                return await self._get_token_balance(address, asset)

        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def _get_native_balance(self, address: str) -> BlockchainResponse:
        """Get native coin balance."""
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance = Balance(
                asset="ETH" if self.chain == ChainType.ETHEREUM else "NATIVE",
                symbol="ETH" if self.chain == ChainType.ETHEREUM else "NATIVE",
                amount=Decimal(balance_wei) / Decimal(10 ** 18),
                decimals=18,
                chain=self.chain.value,
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
        """Get ERC-20 token balance."""
        try:
            if not is_checksum_address(token_address):
                token_address = to_checksum_address(token_address)

            contract = self.web3.eth.contract(
                address=token_address,
                abi=ERC20_ABI,
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
                chain=self.chain.value,
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
        """Verify a transaction.

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
                asset="ETH",
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

        except TransactionNotFound:
            return self._create_response(
                success=False,
                error="Transaction not found",
            )
        except Exception as e:
            self.logger.error(f"Failed to verify transaction: {e}")
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_block_height(self) -> BlockchainResponse:
        """Get current block height.

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
        """Get comprehensive address information.

        Args:
            address: Ethereum address

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
                    asset="ETH",
                    symbol="ETH",
                    amount=Decimal(balance_wei) / Decimal(10 ** 18),
                    decimals=18,
                    chain=self.chain.value,
                )
            ]

            # Get transaction count
            tx_count = self.web3.eth.get_transaction_count(address)

            # Check if contract
            code = self.web3.eth.get_code(address)
            is_contract = len(code) > 0

            address_info = AddressInfo(
                address=address,
                chain=self.chain.value,
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
        """Verify an EIP-191 signed message.

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

            # Encode message in EIP-191 format
            message_hash = encode_defunct(text=message)

            # Recover signer address from signature
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

    async def get_aave_v3_positions(self, address: str) -> BlockchainResponse:
        """Get Aave V3 lending/borrowing positions.

        Args:
            address: User address

        Returns:
            BlockchainResponse with position data
        """
        try:
            if self.chain not in self.AAVE_V3_POOLS:
                return self._create_response(
                    success=False,
                    error=f"Aave V3 not supported on {self.chain}",
                )

            pool_address = self.AAVE_V3_POOLS[self.chain]

            if not is_checksum_address(address):
                address = to_checksum_address(address)

            contract = self.web3.eth.contract(
                address=to_checksum_address(pool_address),
                abi=AAVE_POOL_ABI,
            )

            data = contract.functions.getUserAccountData(address).call()

            return self._create_response(
                success=True,
                data={
                    "total_collateral": Decimal(data[0]) / Decimal(10 ** 8),
                    "total_debt": Decimal(data[1]) / Decimal(10 ** 8),
                    "available_borrows": Decimal(data[2]) / Decimal(10 ** 8),
                    "health_factor": Decimal(data[5]) / Decimal(10 ** 18),
                },
            )
        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_lido_staking(self, address: str) -> BlockchainResponse:
        """Get Lido staking position (stETH balance).

        Args:
            address: User address

        Returns:
            BlockchainResponse with stETH balance
        """
        try:
            if self.chain not in self.LIDO_STETH:
                return self._create_response(
                    success=False,
                    error=f"Lido not available on {self.chain}",
                )

            steth_address = self.LIDO_STETH[self.chain]

            return await self._get_token_balance(address, steth_address)

        except Exception as e:
            return self._create_response(
                success=False,
                error=str(e),
            )

    async def get_uniswap_v3_positions(self, address: str) -> BlockchainResponse:
        """Get Uniswap V3 LP positions.

        Args:
            address: User address

        Returns:
            BlockchainResponse with LP position data
        """
        try:
            if self.chain not in self.UNISWAP_V3_POSITION_MANAGER:
                return self._create_response(
                    success=False,
                    error=f"Uniswap V3 not supported on {self.chain}",
                )

            manager_address = self.UNISWAP_V3_POSITION_MANAGER[self.chain]

            if not is_checksum_address(address):
                address = to_checksum_address(address)

            # Get NFT balance (positions held)
            nft_abi = json.loads("""[
                {
                    "inputs": [{"name": "owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "inputs": [{"name": "owner", "type": "address"}, {"name": "index", "type": "uint256"}],
                    "name": "tokenOfOwnerByIndex",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }
            ]""")

            contract = self.web3.eth.contract(
                address=to_checksum_address(manager_address),
                abi=nft_abi,
            )

            balance = contract.functions.balanceOf(address).call()

            positions = []
            for i in range(balance):
                token_id = contract.functions.tokenOfOwnerByIndex(address, i).call()
                positions.append(token_id)

            return self._create_response(
                success=True,
                data={
                    "position_count": balance,
                    "position_ids": positions,
                },
            )

        except Exception as e:
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
