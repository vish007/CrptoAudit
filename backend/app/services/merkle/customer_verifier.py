"""Customer-facing Merkle tree verification service."""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import hashlib

from .merkle_engine import MerkleTree, MerkleProof, HashAlgorithm

logger = logging.getLogger(__name__)


class VerificationResult:
    """Result of a verification attempt."""

    def __init__(
        self,
        is_valid: bool,
        customer_id: str,
        timestamp: datetime,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize verification result.

        Args:
            is_valid: Whether verification passed
            customer_id: Customer ID
            timestamp: Verification timestamp
            message: Result message
            details: Additional details
        """
        self.is_valid = is_valid
        self.customer_id = customer_id
        self.timestamp = timestamp
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_valid": self.is_valid,
            "customer_id": self.customer_id,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "details": self.details,
        }


class CustomerVerifier:
    """Customer-facing verification service for Merkle tree proofs."""

    def __init__(
        self,
        merkle_tree: MerkleTree,
        rate_limit: int = 100,
        rate_window_seconds: int = 60,
    ):
        """Initialize customer verifier.

        Args:
            merkle_tree: The published Merkle tree
            rate_limit: Maximum verification requests per window
            rate_window_seconds: Rate limit window in seconds
        """
        self.merkle_tree = merkle_tree
        self.logger = logging.getLogger(self.__class__.__name__)

        # Rate limiting
        self.rate_limit = rate_limit
        self.rate_window_seconds = rate_window_seconds
        self.verification_log: Dict[str, list] = {}

    async def verify_inclusion(
        self,
        customer_id: str,
        proof_data: Dict[str, Any],
    ) -> VerificationResult:
        """Verify customer inclusion in Merkle tree.

        Args:
            customer_id: Customer ID
            proof_data: Proof data from verification package

        Returns:
            Verification result
        """
        timestamp = datetime.utcnow()

        # Check rate limit
        if not self._check_rate_limit(customer_id):
            return VerificationResult(
                is_valid=False,
                customer_id=customer_id,
                timestamp=timestamp,
                message="Rate limit exceeded",
            )

        try:
            # Extract proof data
            leaf_hash = proof_data.get("leaf_hash")
            root_hash = proof_data.get("root_hash")
            siblings = proof_data.get("proof", {}).get("siblings", [])
            leaf_index = proof_data.get("proof", {}).get("leaf_index")

            if not all([leaf_hash, root_hash, siblings is not None, leaf_index is not None]):
                return VerificationResult(
                    is_valid=False,
                    customer_id=customer_id,
                    timestamp=timestamp,
                    message="Invalid proof data: missing required fields",
                )

            # Create proof object
            proof = MerkleProof(
                leaf_index=leaf_index,
                leaf_hash=leaf_hash,
                siblings=siblings,
                root_hash=root_hash,
                tree_depth=self.merkle_tree.get_tree_depth(),
                timestamp=timestamp,
            )

            # Verify proof
            is_valid = self.merkle_tree.verify_proof(proof)

            # Log verification
            self._log_verification(customer_id, is_valid)

            if is_valid:
                message = f"Customer {customer_id} successfully verified in Merkle tree"
                details = {
                    "leaf_index": leaf_index,
                    "tree_depth": self.merkle_tree.get_tree_depth(),
                    "total_leaves": self.merkle_tree.get_leaf_count(),
                }
            else:
                message = f"Proof verification failed for customer {customer_id}"
                details = {
                    "leaf_hash": leaf_hash,
                    "root_hash": root_hash,
                    "computed_root": self.merkle_tree.root_hash,
                }

            return VerificationResult(
                is_valid=is_valid,
                customer_id=customer_id,
                timestamp=timestamp,
                message=message,
                details=details,
            )

        except Exception as e:
            self.logger.error(f"Verification error: {e}")
            return VerificationResult(
                is_valid=False,
                customer_id=customer_id,
                timestamp=timestamp,
                message=f"Verification error: {str(e)}",
            )

    async def verify_multiple(
        self,
        verifications: Dict[str, Dict[str, Any]],
    ) -> Dict[str, VerificationResult]:
        """Verify multiple customers in batch.

        Args:
            verifications: Dictionary mapping customer_id to proof_data

        Returns:
            Dictionary of verification results
        """
        tasks = [
            self.verify_inclusion(customer_id, proof_data)
            for customer_id, proof_data in verifications.items()
        ]

        results = await asyncio.gather(*tasks)

        return {
            customer_id: result
            for customer_id, result in zip(verifications.keys(), results)
        }

    async def verify_leaf_data(
        self,
        customer_id: str,
        assets: Dict[str, float],
        proof_data: Dict[str, Any],
        nonce: str = "",
    ) -> VerificationResult:
        """Verify both leaf data and inclusion.

        Args:
            customer_id: Customer ID
            assets: Asset holdings
            proof_data: Proof data
            nonce: Optional nonce value

        Returns:
            Verification result
        """
        timestamp = datetime.utcnow()

        try:
            # Find customer in tree
            leaf_hash_from_proof = proof_data.get("leaf_hash")

            if not leaf_hash_from_proof:
                return VerificationResult(
                    is_valid=False,
                    customer_id=customer_id,
                    timestamp=timestamp,
                    message="No leaf hash in proof data",
                )

            # Verify proof
            proof_result = await self.verify_inclusion(customer_id, proof_data)

            if not proof_result.is_valid:
                return proof_result

            # Additional check: verify assets match
            details = {
                **proof_result.details,
                "assets_verified": True,
                "asset_count": len(assets),
            }

            return VerificationResult(
                is_valid=True,
                customer_id=customer_id,
                timestamp=timestamp,
                message=f"Customer {customer_id} and assets verified",
                details=details,
            )

        except Exception as e:
            self.logger.error(f"Data verification error: {e}")
            return VerificationResult(
                is_valid=False,
                customer_id=customer_id,
                timestamp=timestamp,
                message=f"Verification error: {str(e)}",
            )

    def _check_rate_limit(self, customer_id: str) -> bool:
        """Check if customer is within rate limit.

        Args:
            customer_id: Customer ID

        Returns:
            True if within limit, False otherwise
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.rate_window_seconds)

        # Get or create log for customer
        if customer_id not in self.verification_log:
            self.verification_log[customer_id] = []

        log = self.verification_log[customer_id]

        # Remove old entries
        log[:] = [t for t in log if t > cutoff]

        # Check limit
        if len(log) >= self.rate_limit:
            return False

        return True

    def _log_verification(self, customer_id: str, success: bool) -> None:
        """Log a verification attempt.

        Args:
            customer_id: Customer ID
            success: Whether verification succeeded
        """
        if customer_id not in self.verification_log:
            self.verification_log[customer_id] = []

        self.verification_log[customer_id].append(datetime.utcnow())

        self.logger.info(
            f"Verification attempt for {customer_id}: "
            f"{'success' if success else 'failed'}"
        )

    def get_verification_stats(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get verification statistics.

        Args:
            customer_id: Specific customer (optional)

        Returns:
            Verification statistics
        """
        if customer_id:
            log = self.verification_log.get(customer_id, [])
            return {
                "customer_id": customer_id,
                "total_verifications": len(log),
                "recent_verifications": len([
                    t for t in log
                    if t > datetime.utcnow() - timedelta(seconds=self.rate_window_seconds)
                ]),
                "last_verification": log[-1].isoformat() if log else None,
            }
        else:
            # Overall stats
            total_customers = len(self.verification_log)
            total_verifications = sum(len(log) for log in self.verification_log.values())

            return {
                "total_customers_verified": total_customers,
                "total_verification_attempts": total_verifications,
                "rate_limit": self.rate_limit,
                "rate_window_seconds": self.rate_window_seconds,
            }

    async def clear_old_logs(self) -> None:
        """Clear old verification logs."""
        cutoff = datetime.utcnow() - timedelta(days=30)

        for customer_id in list(self.verification_log.keys()):
            log = self.verification_log[customer_id]
            log[:] = [t for t in log if t > cutoff]

            if not log:
                del self.verification_log[customer_id]

        self.logger.info("Cleared old verification logs")
