"""Abstract base class for blockchain adapters."""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)


class ChainType(str, Enum):
    """Supported blockchain types."""
    ETHEREUM = "ethereum"
    BITCOIN = "bitcoin"
    SOLANA = "solana"
    XRP = "xrp"
    BNB_CHAIN = "bnb_chain"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    POLYGON = "polygon"
    BASE = "base"


class AssetType(str, Enum):
    """Asset classification."""
    NATIVE_COIN = "native_coin"
    ERC20_TOKEN = "erc20_token"
    BEP20_TOKEN = "bep20_token"
    SPL_TOKEN = "spl_token"
    XRPL_TOKEN = "xrpl_token"
    STAKING = "staking"
    LP_POSITION = "lp_position"
    LENDING_POSITION = "lending_position"


@dataclass
class BlockchainResponse:
    """Standardized response from blockchain operations."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    chain: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    block_height: Optional[int] = None
    confirmations: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate response consistency."""
        if self.success and self.data is None:
            logger.warning(f"Success response has no data for {self.chain}")
        if not self.success and self.error is None:
            self.error = "Unknown error"


@dataclass
class Balance:
    """Asset balance information."""
    asset: str
    symbol: str
    amount: Decimal
    decimals: int
    usd_value: Optional[Decimal] = None
    chain: Optional[str] = None
    contract_address: Optional[str] = None


@dataclass
class Transaction:
    """Transaction information."""
    tx_hash: str
    from_address: str
    to_address: str
    value: Decimal
    asset: str
    confirmations: int
    block_height: Optional[int] = None
    timestamp: Optional[datetime] = None
    gas_used: Optional[int] = None
    status: str = "pending"  # pending, confirmed, failed


@dataclass
class AddressInfo:
    """Comprehensive address information."""
    address: str
    chain: str
    balances: List[Balance]
    transaction_count: int
    total_received: Optional[Decimal] = None
    total_sent: Optional[Decimal] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    is_contract: bool = False
    contract_name: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, max_calls: int, window_seconds: int):
        """Initialize rate limiter.

        Args:
            max_calls: Maximum calls allowed
            window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: List[datetime] = []

    async def acquire(self) -> None:
        """Acquire a slot, blocking if necessary."""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.window_seconds)

        # Remove old calls outside the window
        self.calls = [call for call in self.calls if call > cutoff]

        if len(self.calls) >= self.max_calls:
            sleep_time = (self.calls[0] - cutoff).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            self.calls = []

        self.calls.append(now)


class BaseBlockchainAdapter(ABC):
    """Abstract base class for blockchain adapters."""

    def __init__(
        self,
        chain: ChainType,
        api_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        rate_limit: Optional[tuple] = None,
    ):
        """Initialize blockchain adapter.

        Args:
            chain: Chain type
            api_key: API key for external services
            rpc_url: RPC endpoint URL
            max_retries: Maximum retry attempts
            retry_delay: Initial retry delay in seconds
            rate_limit: Tuple of (max_calls, window_seconds)
        """
        self.chain = chain
        self.api_key = api_key
        self.rpc_url = rpc_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize rate limiter
        if rate_limit:
            self.rate_limiter = RateLimiter(rate_limit[0], rate_limit[1])
        else:
            self.rate_limiter = RateLimiter(100, 60)  # Default: 100 calls/min

    async def _retry_with_backoff(
        self,
        coro,
        operation_name: str = "operation",
    ) -> Any:
        """Retry async operation with exponential backoff.

        Args:
            coro: Coroutine to retry
            operation_name: Name for logging

        Returns:
            Result of operation

        Raises:
            Exception: If all retries fail
        """
        delay = self.retry_delay

        for attempt in range(self.max_retries):
            try:
                await self.rate_limiter.acquire()
                return await coro
            except asyncio.TimeoutError as e:
                if attempt == self.max_retries - 1:
                    self.logger.error(
                        f"{operation_name} failed after {self.max_retries} retries: {e}"
                    )
                    raise
                await asyncio.sleep(delay)
                delay *= 2
            except Exception as e:
                if attempt == self.max_retries - 1:
                    self.logger.error(
                        f"{operation_name} failed after {self.max_retries} retries: {e}"
                    )
                    raise
                await asyncio.sleep(delay)
                delay *= 2

        raise RuntimeError(f"Failed to complete {operation_name}")

    def _create_response(
        self,
        success: bool,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        **kwargs,
    ) -> BlockchainResponse:
        """Create standardized response.

        Args:
            success: Whether operation succeeded
            data: Response data
            error: Error message if any
            **kwargs: Additional metadata

        Returns:
            BlockchainResponse
        """
        return BlockchainResponse(
            success=success,
            data=data,
            error=error,
            chain=self.chain.value,
            **kwargs,
        )

    @abstractmethod
    async def get_balance(
        self,
        address: str,
        asset: Optional[str] = None,
    ) -> BlockchainResponse:
        """Get balance for an address.

        Args:
            address: Wallet address
            asset: Specific asset to query (optional)

        Returns:
            BlockchainResponse with Balance data
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_block_height(self) -> BlockchainResponse:
        """Get current block height.

        Returns:
            BlockchainResponse with block height
        """
        pass

    @abstractmethod
    async def get_address_info(self, address: str) -> BlockchainResponse:
        """Get comprehensive address information.

        Args:
            address: Wallet address

        Returns:
            BlockchainResponse with AddressInfo data
        """
        pass

    @abstractmethod
    async def verify_signed_message(
        self,
        address: str,
        message: str,
        signature: str,
    ) -> BlockchainResponse:
        """Verify a signed message.

        Args:
            address: Expected signer address
            message: Original message
            signature: Message signature

        Returns:
            BlockchainResponse with boolean success
        """
        pass

    async def health_check(self) -> BlockchainResponse:
        """Check adapter health and connectivity.

        Returns:
            BlockchainResponse indicating health status
        """
        try:
            response = await self.get_block_height()
            return response
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return self._create_response(
                success=False,
                error=f"Health check failed: {str(e)}",
            )

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}({self.chain.value})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"{self.__class__.__name__}(chain={self.chain}, rpc_url={self.rpc_url})"
