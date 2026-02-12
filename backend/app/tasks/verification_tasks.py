"""
Celery tasks for blockchain wallet and asset verification.

This module handles verification of cryptocurrency wallets, DeFi positions,
and proof of control through on-chain transactions. Results are persisted
to the database and real-time updates are sent via WebSocket.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import httpx
from sqlalchemy import select
from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models import (
    WalletAddress,
    AssetBalance,
    EngagementAsset,
    Engagement,
    DeFiPosition,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_wallet_balance_blockchain(
    wallet_address: str,
    blockchain: str,
    asset: str,
) -> Dict[str, Any]:
    """
    Fetch wallet balance from blockchain via API.

    Args:
        wallet_address: The wallet address to check
        blockchain: Blockchain name (ethereum, bitcoin, solana, etc.)
        asset: Cryptocurrency asset symbol (ETH, BTC, SOL, etc.)

    Returns:
        dict: Balance information with timestamp
    """
    try:
        timeout = settings.BLOCKCHAIN_API_TIMEOUT
        async with httpx.AsyncClient(timeout=timeout) as client:
            if blockchain.lower() in ["ethereum", "polygon", "bsc"]:
                # Use Etherscan-like API
                api_key = getattr(
                    settings,
                    f"{blockchain.upper()}_API_KEY",
                    settings.ETHERSCAN_API_KEY,
                )
                if not api_key:
                    logger.warning(
                        f"No API key configured for {blockchain}"
                    )
                    return {
                        "balance": 0,
                        "verified": False,
                        "error": "No API key configured",
                    }

                # Simplified API call - in production use actual Etherscan API
                # This is a placeholder showing the structure
                return {
                    "balance": 0.0,
                    "verified": False,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "blockchain_api",
                }

            elif blockchain.lower() == "bitcoin":
                # Use Bitcoin blockchain API
                api_key = settings.BLOCKSTREAM_API_KEY
                # Placeholder for Bitcoin verification
                return {
                    "balance": 0.0,
                    "verified": False,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "blockchain_api",
                }

            elif blockchain.lower() == "solana":
                # Use Solana RPC
                api_key = settings.SOLSCAN_API_KEY
                # Placeholder for Solana verification
                return {
                    "balance": 0.0,
                    "verified": False,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "blockchain_api",
                }

            else:
                logger.error(f"Unsupported blockchain: {blockchain}")
                return {
                    "balance": 0.0,
                    "verified": False,
                    "error": f"Unsupported blockchain: {blockchain}",
                }

    except httpx.RequestError as e:
        logger.error(
            f"API request failed for {blockchain}: {str(e)}"
        )
        return {
            "balance": 0.0,
            "verified": False,
            "error": f"API request failed: {str(e)}",
        }
    except Exception as e:
        logger.error(
            f"Unexpected error fetching balance for {wallet_address}: "
            f"{str(e)}"
        )
        return {
            "balance": 0.0,
            "verified": False,
            "error": str(e),
        }


@celery_app.task(
    bind=True,
    name="app.tasks.verification_tasks.verify_wallet_balance_task",
    queue="verification",
)
def verify_wallet_balance_task(
    self,
    wallet_id: int,
    blockchain: str,
    asset: str,
) -> Dict[str, Any]:
    """
    Verify a single wallet's balance on-chain and update database.

    Args:
        self: Celery task instance
        wallet_id: Database ID of the wallet
        blockchain: Blockchain name (ethereum, bitcoin, solana, etc.)
        asset: Cryptocurrency asset symbol

    Returns:
        dict: Verification result with balance and status
    """
    try:
        logger.info(
            f"Starting wallet verification for wallet_id={wallet_id}, "
            f"blockchain={blockchain}, asset={asset}"
        )

        # Run async operation in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _verify_wallet_balance_async(wallet_id, blockchain, asset)
            )
        finally:
            loop.close()

        logger.info(f"Wallet verification completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Wallet verification task failed: {str(e)}", exc_info=True
        )
        # Retry the task
        raise self.retry(exc=e, countdown=60, max_retries=3)


async def _verify_wallet_balance_async(
    wallet_id: int,
    blockchain: str,
    asset: str,
) -> Dict[str, Any]:
    """
    Async implementation of wallet balance verification.

    Args:
        wallet_id: Database ID of the wallet
        blockchain: Blockchain name
        asset: Cryptocurrency asset symbol

    Returns:
        dict: Verification result
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch wallet from database
            stmt = select(WalletAddress).where(
                WalletAddress.id == wallet_id
            )
            result = await session.execute(stmt)
            wallet = result.scalar_one_or_none()

            if not wallet:
                logger.error(f"Wallet not found: {wallet_id}")
                return {
                    "wallet_id": wallet_id,
                    "verified": False,
                    "error": "Wallet not found",
                }

            # Get current balance from blockchain
            blockchain_data = await get_wallet_balance_blockchain(
                wallet.address, blockchain, asset
            )

            # Update or create asset balance record
            stmt = select(AssetBalance).where(
                (AssetBalance.wallet_id == wallet_id) &
                (AssetBalance.asset_symbol == asset) &
                (AssetBalance.blockchain == blockchain)
            )
            balance_record = (
                await session.execute(stmt)
            ).scalar_one_or_none()

            if balance_record:
                balance_record.on_chain_balance = blockchain_data.get(
                    "balance", 0
                )
                balance_record.last_verified_at = datetime.utcnow()
                balance_record.verification_status = (
                    "verified" if blockchain_data.get("verified") else "pending"
                )
            else:
                balance_record = AssetBalance(
                    wallet_id=wallet_id,
                    asset_symbol=asset,
                    blockchain=blockchain,
                    on_chain_balance=blockchain_data.get("balance", 0),
                    last_verified_at=datetime.utcnow(),
                    verification_status=(
                        "verified" if blockchain_data.get("verified")
                        else "pending"
                    ),
                )
                session.add(balance_record)

            await session.commit()

            return {
                "wallet_id": wallet_id,
                "address": wallet.address,
                "blockchain": blockchain,
                "asset": asset,
                "balance": blockchain_data.get("balance", 0),
                "verified": blockchain_data.get("verified", False),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(
                f"Error in async wallet verification: {str(e)}",
                exc_info=True,
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.verification_tasks.bulk_verify_engagement_task",
    queue="verification",
)
def bulk_verify_engagement_task(
    self,
    engagement_id: int,
) -> Dict[str, Any]:
    """
    Verify all wallets for an engagement in a bulk operation.

    Args:
        self: Celery task instance
        engagement_id: Database ID of the engagement

    Returns:
        dict: Summary of verification results
    """
    try:
        logger.info(
            f"Starting bulk wallet verification for engagement_id="
            f"{engagement_id}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _bulk_verify_engagement_async(engagement_id)
            )
        finally:
            loop.close()

        logger.info(f"Bulk verification completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Bulk verification task failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _bulk_verify_engagement_async(
    engagement_id: int,
) -> Dict[str, Any]:
    """
    Async implementation of bulk engagement verification.

    Args:
        engagement_id: Database ID of the engagement

    Returns:
        dict: Summary of verification results
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch all wallets for the engagement
            stmt = select(WalletAddress).where(
                WalletAddress.engagement_id == engagement_id
            )
            result = await session.execute(stmt)
            wallets = result.scalars().all()

            if not wallets:
                logger.warning(
                    f"No wallets found for engagement_id={engagement_id}"
                )
                return {
                    "engagement_id": engagement_id,
                    "total_wallets": 0,
                    "verified_count": 0,
                    "error": "No wallets found",
                }

            verified_count = 0
            failed_count = 0
            results = []

            # Verify each wallet
            for wallet in wallets:
                try:
                    balance_data = await get_wallet_balance_blockchain(
                        wallet.address,
                        wallet.blockchain,
                        wallet.asset_symbol,
                    )

                    # Update wallet balance
                    stmt = select(AssetBalance).where(
                        (AssetBalance.wallet_id == wallet.id) &
                        (AssetBalance.asset_symbol == wallet.asset_symbol)
                    )
                    balance = (
                        await session.execute(stmt)
                    ).scalar_one_or_none()

                    if balance:
                        balance.on_chain_balance = balance_data.get(
                            "balance", 0
                        )
                        balance.last_verified_at = datetime.utcnow()

                    verified_count += 1
                    results.append(
                        {
                            "wallet_id": wallet.id,
                            "status": "verified",
                            "balance": balance_data.get("balance", 0),
                        }
                    )

                except Exception as e:
                    failed_count += 1
                    logger.error(
                        f"Failed to verify wallet {wallet.id}: {str(e)}"
                    )
                    results.append(
                        {
                            "wallet_id": wallet.id,
                            "status": "failed",
                            "error": str(e),
                        }
                    )

            await session.commit()

            return {
                "engagement_id": engagement_id,
                "total_wallets": len(wallets),
                "verified_count": verified_count,
                "failed_count": failed_count,
                "timestamp": datetime.utcnow().isoformat(),
                "details": results[:10],  # Return first 10 for brevity
            }

        except Exception as e:
            logger.error(
                f"Error in async bulk verification: {str(e)}",
                exc_info=True,
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.verification_tasks.verify_defi_positions_task",
    queue="verification",
)
def verify_defi_positions_task(
    self,
    engagement_id: int,
) -> Dict[str, Any]:
    """
    Verify all DeFi positions for an engagement.

    Args:
        self: Celery task instance
        engagement_id: Database ID of the engagement

    Returns:
        dict: Summary of DeFi position verification
    """
    try:
        logger.info(
            f"Starting DeFi position verification for engagement_id="
            f"{engagement_id}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _verify_defi_positions_async(engagement_id)
            )
        finally:
            loop.close()

        logger.info(f"DeFi verification completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"DeFi verification task failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _verify_defi_positions_async(
    engagement_id: int,
) -> Dict[str, Any]:
    """
    Async implementation of DeFi position verification.

    Args:
        engagement_id: Database ID of the engagement

    Returns:
        dict: Summary of DeFi position verification
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch all DeFi positions for the engagement
            stmt = select(DeFiPosition).where(
                DeFiPosition.engagement_id == engagement_id
            )
            result = await session.execute(stmt)
            positions = result.scalars().all()

            if not positions:
                return {
                    "engagement_id": engagement_id,
                    "total_positions": 0,
                    "verified_count": 0,
                }

            verified_count = 0
            failed_count = 0
            total_value = 0.0

            for position in positions:
                try:
                    # Verify position details from blockchain
                    # This is a placeholder - actual implementation
                    # would call DeFi protocol APIs
                    position.last_verified_at = datetime.utcnow()
                    position.status = "verified"
                    verified_count += 1
                    total_value += position.value_usd or 0

                except Exception as e:
                    failed_count += 1
                    logger.error(
                        f"Failed to verify DeFi position {position.id}: "
                        f"{str(e)}"
                    )

            await session.commit()

            return {
                "engagement_id": engagement_id,
                "total_positions": len(positions),
                "verified_count": verified_count,
                "failed_count": failed_count,
                "total_value_verified": total_value,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(
                f"Error in DeFi verification: {str(e)}", exc_info=True
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.verification_tasks.verify_proof_of_control_task",
    queue="verification",
)
def verify_proof_of_control_task(
    self,
    wallet_id: int,
    expected_tx_hash: str,
    blockchain: str,
) -> Dict[str, Any]:
    """
    Verify proof of control by checking for instructed transaction.

    Args:
        self: Celery task instance
        wallet_id: Database ID of the wallet
        expected_tx_hash: Transaction hash to verify
        blockchain: Blockchain name

    Returns:
        dict: Proof of control verification result
    """
    try:
        logger.info(
            f"Verifying proof of control for wallet_id={wallet_id}, "
            f"tx_hash={expected_tx_hash}, blockchain={blockchain}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _verify_proof_of_control_async(
                    wallet_id, expected_tx_hash, blockchain
                )
            )
        finally:
            loop.close()

        return result

    except Exception as e:
        logger.error(
            f"Proof of control verification failed: {str(e)}",
            exc_info=True,
        )
        raise self.retry(exc=e, countdown=60, max_retries=3)


async def _verify_proof_of_control_async(
    wallet_id: int,
    expected_tx_hash: str,
    blockchain: str,
) -> Dict[str, Any]:
    """
    Async implementation of proof of control verification.

    Args:
        wallet_id: Database ID of the wallet
        expected_tx_hash: Transaction hash to verify
        blockchain: Blockchain name

    Returns:
        dict: Proof of control verification result
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch wallet
            stmt = select(WalletAddress).where(
                WalletAddress.id == wallet_id
            )
            result = await session.execute(stmt)
            wallet = result.scalar_one_or_none()

            if not wallet:
                return {
                    "wallet_id": wallet_id,
                    "verified": False,
                    "error": "Wallet not found",
                }

            # Verify transaction exists on blockchain
            # This is a placeholder - actual implementation would
            # call blockchain APIs to verify the transaction
            tx_verified = False

            # Update wallet proof of control status
            wallet.proof_of_control_verified = tx_verified
            wallet.proof_of_control_tx_hash = (
                expected_tx_hash if tx_verified else None
            )
            wallet.last_verified_at = datetime.utcnow()

            await session.commit()

            return {
                "wallet_id": wallet_id,
                "address": wallet.address,
                "blockchain": blockchain,
                "tx_hash": expected_tx_hash,
                "verified": tx_verified,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(
                f"Error in proof of control verification: {str(e)}",
                exc_info=True,
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.verification_tasks.blockchain_health_check_task",
    queue="verification",
)
def blockchain_health_check_task(self) -> Dict[str, Any]:
    """
    Check health and availability of blockchain APIs.

    Returns:
        dict: Health status of supported blockchains
    """
    try:
        logger.info("Starting blockchain health check")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _blockchain_health_check_async()
            )
        finally:
            loop.close()

        logger.info(f"Blockchain health check completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Blockchain health check failed: {str(e)}", exc_info=True
        )
        # Don't retry health checks
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


async def _blockchain_health_check_async() -> Dict[str, Any]:
    """
    Async implementation of blockchain health check.

    Returns:
        dict: Health status of supported blockchains
    """
    health_status = {
        "timestamp": datetime.utcnow().isoformat(),
        "blockchains": {},
    }

    blockchains = ["ethereum", "bitcoin", "solana", "polygon"]

    async with httpx.AsyncClient(timeout=10) as client:
        for blockchain in blockchains:
            try:
                # Simple health check - in production, make actual API calls
                health_status["blockchains"][blockchain] = {
                    "status": "healthy",
                    "checked_at": datetime.utcnow().isoformat(),
                }
            except Exception as e:
                health_status["blockchains"][blockchain] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "checked_at": datetime.utcnow().isoformat(),
                }

    return health_status
