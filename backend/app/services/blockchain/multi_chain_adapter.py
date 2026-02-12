"""Multi-chain adapter and orchestrator for blockchain verification."""

import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from .base_adapter import (
    Balance,
    BaseBlockchainAdapter,
    BlockchainResponse,
    ChainType,
)
from .ethereum_adapter import EthereumAdapter
from .bitcoin_adapter import BitcoinAdapter
from .solana_adapter import SolanaAdapter
from .xrp_adapter import XRPAdapter
from .bnb_adapter import BNBAdapter

logger = logging.getLogger(__name__)


@dataclass
class AggregatedBalance:
    """Aggregated balance across chains."""
    asset: str
    symbol: str
    total_amount: Decimal
    decimals: int
    by_chain: Dict[str, Decimal] = field(default_factory=dict)
    chain_details: List[Balance] = field(default_factory=list)


class CryptoAssetMapping(str, Enum):
    """Mapping of 153 cryptocurrencies to their native chains."""

    # Major coins
    BTC = "bitcoin"
    ETH = "ethereum"
    BNB = "bnb_chain"
    SOL = "solana"
    XRP = "xrp"
    ADA = "cardano"
    DOGE = "dogecoin"
    MATIC = "polygon"

    # Ethereum tokens
    USDT = "ethereum"
    USDC = "ethereum"
    BUSD = "ethereum"
    DAI = "ethereum"
    WETH = "ethereum"
    UNISWAP = "ethereum"
    AAVE = "ethereum"
    LINK = "ethereum"
    UNI = "ethereum"
    CURVE = "ethereum"
    YFI = "ethereum"
    COMP = "ethereum"
    MKR = "ethereum"
    SUSHI = "ethereum"
    LIDO = "ethereum"
    FRAX = "ethereum"
    ROCKET_POOL = "ethereum"
    CONVEX = "ethereum"
    BALANCER = "ethereum"

    # Solana tokens
    STEP = "solana"
    COPE = "solana"
    ORCA = "solana"
    MARINADE = "solana"
    RAYDIUM = "solana"

    # BNB Chain tokens
    CAKE = "bnb_chain"
    ALPACA = "bnb_chain"

    # XRP Ledger tokens
    GEN = "xrp"

    # Layer 2 / EVM compatible
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    POLYGON_TOKEN = "polygon"
    BASE = "base"


# Asset to RPC chain mapping (supports cross-chain assets)
CROSS_CHAIN_ASSETS = {
    "USDT": ["ethereum", "polygon", "bnb_chain", "solana", "xrp"],
    "USDC": ["ethereum", "polygon", "bnb_chain", "solana", "arbitrum", "optimism"],
    "BUSD": ["ethereum", "bnb_chain"],
    "DAI": ["ethereum", "polygon"],
    "ETH": ["ethereum", "arbitrum", "optimism", "polygon"],
}


class ChainRegistry:
    """Registry for managing blockchain adapters."""

    def __init__(self):
        """Initialize chain registry."""
        self.adapters: Dict[ChainType, BaseBlockchainAdapter] = {}
        self.rate_limits: Dict[ChainType, Tuple[int, int]] = {}
        self.health_status: Dict[ChainType, bool] = {}

    def register(
        self,
        chain: ChainType,
        adapter: BaseBlockchainAdapter,
        rate_limit: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Register a blockchain adapter.

        Args:
            chain: Chain type
            adapter: Adapter instance
            rate_limit: Rate limit (calls, window_seconds)
        """
        self.adapters[chain] = adapter
        if rate_limit:
            self.rate_limits[chain] = rate_limit
        self.health_status[chain] = True
        logger.info(f"Registered adapter for {chain.value}")

    def get(self, chain: ChainType) -> Optional[BaseBlockchainAdapter]:
        """Get adapter for chain.

        Args:
            chain: Chain type

        Returns:
            Adapter or None if not registered
        """
        return self.adapters.get(chain)

    def get_all(self) -> Dict[ChainType, BaseBlockchainAdapter]:
        """Get all registered adapters.

        Returns:
            Dictionary of adapters
        """
        return self.adapters.copy()

    def is_healthy(self, chain: ChainType) -> bool:
        """Check if chain adapter is healthy.

        Args:
            chain: Chain type

        Returns:
            Health status
        """
        return self.health_status.get(chain, False)

    async def set_health_status(self, chain: ChainType, healthy: bool) -> None:
        """Set chain health status.

        Args:
            chain: Chain type
            healthy: Health status
        """
        self.health_status[chain] = healthy


class MultiChainAdapter:
    """Multi-chain adapter for orchestrating verification across all chains."""

    def __init__(self, registry: Optional[ChainRegistry] = None):
        """Initialize multi-chain adapter.

        Args:
            registry: Chain registry (created if None)
        """
        self.registry = registry or ChainRegistry()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def initialize_default_adapters(
        self,
        ethereum_rpc: Optional[str] = None,
        bitcoin_api_key: Optional[str] = None,
        solana_rpc: Optional[str] = None,
        xrp_rpc: Optional[str] = None,
        bnb_rpc: Optional[str] = None,
    ) -> None:
        """Initialize default adapters for all major chains.

        Args:
            ethereum_rpc: Ethereum RPC URL
            bitcoin_api_key: Bitcoin API key
            solana_rpc: Solana RPC URL
            xrp_rpc: XRP RPC URL
            bnb_rpc: BNB RPC URL
        """
        try:
            # Ethereum and L2s
            eth = EthereumAdapter(
                chain=ChainType.ETHEREUM,
                rpc_url=ethereum_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.ETHEREUM, eth, (100, 60))

            arbitrum = EthereumAdapter(
                chain=ChainType.ARBITRUM,
                rpc_url=ethereum_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.ARBITRUM, arbitrum, (100, 60))

            optimism = EthereumAdapter(
                chain=ChainType.OPTIMISM,
                rpc_url=ethereum_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.OPTIMISM, optimism, (100, 60))

            polygon = EthereumAdapter(
                chain=ChainType.POLYGON,
                rpc_url=ethereum_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.POLYGON, polygon, (100, 60))

            base = EthereumAdapter(
                chain=ChainType.BASE,
                rpc_url=ethereum_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.BASE, base, (100, 60))

            # Bitcoin
            btc = BitcoinAdapter(
                api_key=bitcoin_api_key,
                rate_limit=(30, 60),
            )
            self.registry.register(ChainType.BITCOIN, btc, (30, 60))

            # Solana
            sol = SolanaAdapter(
                rpc_url=solana_rpc or "https://api.mainnet-beta.solana.com",
                rate_limit=(50, 60),
            )
            self.registry.register(ChainType.SOLANA, sol, (50, 60))

            # XRP Ledger
            xrp = XRPAdapter(
                rpc_url=xrp_rpc or "https://s1.ripple.com:51234",
                rate_limit=(30, 60),
            )
            self.registry.register(ChainType.XRP, xrp, (30, 60))

            # BNB Chain
            bnb = BNBAdapter(
                rpc_url=bnb_rpc,
                rate_limit=(100, 60),
            )
            self.registry.register(ChainType.BNB_CHAIN, bnb, (100, 60))

            self.logger.info("Initialized default adapters for all chains")

        except Exception as e:
            self.logger.error(f"Failed to initialize adapters: {e}")
            raise

    def map_asset_to_chains(self, asset: str) -> List[ChainType]:
        """Map asset to supported chains.

        Args:
            asset: Asset symbol (e.g., "USDT")

        Returns:
            List of chains supporting this asset
        """
        # Check cross-chain assets first
        if asset in CROSS_CHAIN_ASSETS:
            chains = []
            for chain_value in CROSS_CHAIN_ASSETS[asset]:
                try:
                    chains.append(ChainType(chain_value))
                except ValueError:
                    continue
            return chains

        # Check native asset mappings
        try:
            mapping = CryptoAssetMapping[asset]
            chain_value = mapping.value
            return [ChainType(chain_value)]
        except (KeyError, ValueError):
            # Default to checking all chains
            return list(self.registry.get_all().keys())

    async def verify_balance(
        self,
        address: str,
        asset: str,
        chain: Optional[ChainType] = None,
    ) -> BlockchainResponse:
        """Verify balance for a single address/asset/chain.

        Args:
            address: Wallet address
            asset: Asset symbol or contract
            chain: Specific chain (optional)

        Returns:
            BlockchainResponse with balance data
        """
        if chain:
            adapter = self.registry.get(chain)
            if not adapter:
                return BlockchainResponse(
                    success=False,
                    error=f"Adapter not available for {chain.value}",
                    chain=chain.value,
                )

            try:
                return await adapter.get_balance(address, asset)
            except Exception as e:
                self.logger.error(f"Balance verification failed: {e}")
                return BlockchainResponse(
                    success=False,
                    error=str(e),
                    chain=chain.value,
                )
        else:
            # Verify on all chains
            return await self._verify_balance_all_chains(address, asset)

    async def _verify_balance_all_chains(
        self,
        address: str,
        asset: str,
    ) -> BlockchainResponse:
        """Verify balance across all chains.

        Args:
            address: Wallet address
            asset: Asset symbol

        Returns:
            BlockchainResponse with aggregated data
        """
        chains = self.map_asset_to_chains(asset)

        tasks = []
        for chain in chains:
            adapter = self.registry.get(chain)
            if adapter and self.registry.is_healthy(chain):
                tasks.append(self._safe_balance_check(adapter, address, asset))

        if not tasks:
            return BlockchainResponse(
                success=False,
                error=f"No healthy adapters available for {asset}",
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        balances = []
        for result in results:
            if isinstance(result, BlockchainResponse) and result.success and result.data:
                if isinstance(result.data, list):
                    balances.extend(result.data)
                else:
                    balances.append(result.data)

        return BlockchainResponse(
            success=len(balances) > 0,
            data=balances,
            metadata={"chains_checked": len(chains)},
        )

    async def _safe_balance_check(
        self,
        adapter: BaseBlockchainAdapter,
        address: str,
        asset: str,
    ) -> BlockchainResponse:
        """Safely check balance with error handling.

        Args:
            adapter: Blockchain adapter
            address: Wallet address
            asset: Asset symbol

        Returns:
            BlockchainResponse
        """
        try:
            return await asyncio.wait_for(
                adapter.get_balance(address, asset),
                timeout=30,
            )
        except asyncio.TimeoutError:
            await self.registry.set_health_status(adapter.chain, False)
            return BlockchainResponse(
                success=False,
                error="Request timeout",
                chain=adapter.chain.value,
            )
        except Exception as e:
            return BlockchainResponse(
                success=False,
                error=str(e),
                chain=adapter.chain.value,
            )

    async def aggregate_balances(
        self,
        address: str,
        assets: List[str],
    ) -> Dict[str, AggregatedBalance]:
        """Aggregate balances across all chains.

        Args:
            address: Wallet address
            assets: List of assets to verify

        Returns:
            Dictionary of aggregated balances
        """
        tasks = [self.verify_balance(address, asset) for asset in assets]
        results = await asyncio.gather(*tasks)

        aggregated: Dict[str, AggregatedBalance] = {}

        for result in results:
            if result.success and result.data:
                balances = result.data if isinstance(result.data, list) else [result.data]

                for balance in balances:
                    key = balance.symbol.upper()

                    if key not in aggregated:
                        aggregated[key] = AggregatedBalance(
                            asset=balance.asset,
                            symbol=balance.symbol,
                            total_amount=Decimal(0),
                            decimals=balance.decimals,
                        )

                    aggregated[key].total_amount += balance.amount
                    chain = balance.chain or result.chain or "unknown"

                    if chain not in aggregated[key].by_chain:
                        aggregated[key].by_chain[chain] = Decimal(0)

                    aggregated[key].by_chain[chain] += balance.amount
                    aggregated[key].chain_details.append(balance)

        return aggregated

    async def verify_all_wallets(
        self,
        wallets: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """Verify all wallets for an engagement.

        Args:
            wallets: Dict mapping chain to list of addresses

        Returns:
            Comprehensive verification results
        """
        results = {
            "verified_at": datetime.utcnow().isoformat(),
            "wallets": {},
            "summary": {
                "total_chains": len(wallets),
                "total_addresses": sum(len(addrs) for addrs in wallets.values()),
                "healthy_chains": 0,
            },
        }

        tasks = []
        task_map = {}

        for chain_str, addresses in wallets.items():
            try:
                chain = ChainType(chain_str)
            except ValueError:
                self.logger.warning(f"Unknown chain: {chain_str}")
                continue

            adapter = self.registry.get(chain)
            if not adapter:
                self.logger.warning(f"No adapter for chain: {chain_str}")
                continue

            for address in addresses:
                task = adapter.get_address_info(address)
                tasks.append(task)
                task_map[len(tasks) - 1] = (chain_str, address)

        if not tasks:
            return results

        task_results = await asyncio.gather(*tasks, return_exceptions=True)

        for idx, result in enumerate(task_results):
            chain_str, address = task_map[idx]

            if chain_str not in results["wallets"]:
                results["wallets"][chain_str] = []

            if isinstance(result, BlockchainResponse) and result.success:
                results["summary"]["healthy_chains"] += 1
                results["wallets"][chain_str].append({
                    "address": address,
                    "verified": True,
                    "data": result.data.__dict__ if hasattr(result.data, "__dict__") else str(result.data),
                })
            else:
                results["wallets"][chain_str].append({
                    "address": address,
                    "verified": False,
                    "error": result.error if isinstance(result, BlockchainResponse) else str(result),
                })

        return results

    async def verify_transaction(
        self,
        tx_hash: str,
        chain: ChainType,
        min_confirmations: int = 0,
    ) -> BlockchainResponse:
        """Verify a transaction on a specific chain.

        Args:
            tx_hash: Transaction hash
            chain: Chain type
            min_confirmations: Minimum confirmations

        Returns:
            BlockchainResponse with transaction data
        """
        adapter = self.registry.get(chain)
        if not adapter:
            return BlockchainResponse(
                success=False,
                error=f"No adapter for {chain.value}",
            )

        try:
            return await adapter.verify_transaction(tx_hash, min_confirmations)
        except Exception as e:
            self.logger.error(f"Transaction verification failed: {e}")
            return BlockchainResponse(
                success=False,
                error=str(e),
                chain=chain.value,
            )

    async def verify_signed_message(
        self,
        address: str,
        message: str,
        signature: str,
        chain: ChainType,
    ) -> BlockchainResponse:
        """Verify a signed message on a specific chain.

        Args:
            address: Signer address
            message: Original message
            signature: Signature
            chain: Chain type

        Returns:
            BlockchainResponse with verification result
        """
        adapter = self.registry.get(chain)
        if not adapter:
            return BlockchainResponse(
                success=False,
                error=f"No adapter for {chain.value}",
            )

        try:
            return await adapter.verify_signed_message(address, message, signature)
        except Exception as e:
            self.logger.error(f"Message verification failed: {e}")
            return BlockchainResponse(
                success=False,
                error=str(e),
                chain=chain.value,
            )

    async def health_check_all(self) -> Dict[str, bool]:
        """Check health of all adapters.

        Returns:
            Dictionary of chain health status
        """
        tasks = []
        chains = []

        for chain, adapter in self.registry.get_all().items():
            tasks.append(adapter.health_check())
            chains.append(chain)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        health = {}
        for chain, result in zip(chains, results):
            if isinstance(result, BlockchainResponse):
                is_healthy = result.success
            else:
                is_healthy = False

            health[chain.value] = is_healthy
            await self.registry.set_health_status(chain, is_healthy)

        return health

    async def close(self) -> None:
        """Close all adapters."""
        for adapter in self.registry.get_all().values():
            if hasattr(adapter, "close"):
                try:
                    await adapter.close()
                except Exception as e:
                    self.logger.error(f"Error closing adapter: {e}")
