"""Merkle Tree engine for Proof of Reserves."""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import base64

logger = logging.getLogger(__name__)


class HashAlgorithm(str, Enum):
    """Supported hash algorithms."""
    SHA256 = "sha256"
    KECCAK256 = "keccak256"


@dataclass
class MerkleLeaf:
    """A Merkle tree leaf representing customer liability."""
    customer_id: str
    anonymized_id: str  # Hash of customer_id for privacy
    assets: Dict[str, Decimal]  # {asset: amount}
    timestamp: datetime
    nonce: str  # For additional entropy
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with JSON-serializable values."""
        return {
            "customer_id": self.customer_id,
            "anonymized_id": self.anonymized_id,
            "assets": {k: float(v) for k, v in self.assets.items()},
            "timestamp": self.timestamp.isoformat(),
            "nonce": self.nonce,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), sort_keys=True)

    def hash(self, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """Compute leaf hash.

        Args:
            algorithm: Hash algorithm to use

        Returns:
            Hex-encoded hash
        """
        json_str = self.to_json()

        if algorithm == HashAlgorithm.SHA256:
            h = hashlib.sha256()
            h.update(json_str.encode())
            return h.hexdigest()
        elif algorithm == HashAlgorithm.KECCAK256:
            try:
                from Crypto.Hash import keccak
                k = keccak.new(digest_bits=256)
                k.update(json_str.encode())
                return k.hexdigest()
            except ImportError:
                # Fallback to SHA256
                h = hashlib.sha256()
                h.update(json_str.encode())
                return h.hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


@dataclass
class MerkleProof:
    """Merkle proof for leaf verification."""
    leaf_index: int
    leaf_hash: str
    siblings: List[str]  # Hashes of sibling nodes on path to root
    root_hash: str
    tree_depth: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        data = self.to_dict()
        data["timestamp"] = data["timestamp"].isoformat()
        return json.dumps(data)


@dataclass
class TreeStatistics:
    """Statistics about a Merkle tree."""
    total_leaves: int
    tree_depth: int
    root_hash: str
    generation_time_ms: float
    generation_timestamp: datetime
    hash_algorithm: str
    leaf_hashes: List[str] = field(default_factory=list)


class MerkleTree:
    """Merkle tree for PoR verification."""

    def __init__(
        self,
        algorithm: HashAlgorithm = HashAlgorithm.SHA256,
        batch_size: int = 1000,
    ):
        """Initialize Merkle tree.

        Args:
            algorithm: Hash algorithm to use
            batch_size: Batch size for streaming operations
        """
        self.algorithm = algorithm
        self.batch_size = batch_size
        self.leaves: List[MerkleLeaf] = []
        self.tree: Dict[int, List[str]] = {}  # Level -> hashes
        self.root_hash: Optional[str] = None
        self.generation_time: float = 0
        self.generation_timestamp: Optional[datetime] = None

    def add_leaf(self, leaf: MerkleLeaf) -> None:
        """Add a leaf to the tree.

        Args:
            leaf: Merkle leaf
        """
        self.leaves.append(leaf)

    def add_leaves(self, leaves: List[MerkleLeaf]) -> None:
        """Add multiple leaves to the tree.

        Args:
            leaves: List of Merkle leaves
        """
        self.leaves.extend(leaves)

    async def build(self) -> None:
        """Build the Merkle tree from leaves.

        This is an async operation to support large datasets.
        """
        start_time = time.time()

        if not self.leaves:
            raise ValueError("No leaves to build tree")

        # Compute leaf hashes
        leaf_hashes = []
        for i, leaf in enumerate(self.leaves):
            if i % self.batch_size == 0 and i > 0:
                await asyncio.sleep(0)  # Yield to event loop

            leaf_hashes.append(leaf.hash(self.algorithm))

        # Build tree bottom-up
        self.tree = {0: leaf_hashes}

        level = 0
        while len(self.tree[level]) > 1:
            current_level = self.tree[level]
            next_level = []

            for i in range(0, len(current_level), 2):
                if i % self.batch_size == 0 and i > 0:
                    await asyncio.sleep(0)

                # Pair current hash with next (or itself if odd)
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left

                # Hash the pair
                pair_hash = self._hash_pair(left, right)
                next_level.append(pair_hash)

            level += 1
            self.tree[level] = next_level

        # Root is the single hash at the top level
        self.root_hash = self.tree[level][0]
        self.generation_time = time.time() - start_time
        self.generation_timestamp = datetime.utcnow()

        logger.info(
            f"Built Merkle tree: {len(self.leaves)} leaves, "
            f"depth {level}, time {self.generation_time:.2f}s"
        )

    def _hash_pair(self, left: str, right: str) -> str:
        """Hash a pair of hashes.

        Args:
            left: Left hash
            right: Right hash

        Returns:
            Combined hash
        """
        combined = left + right

        if self.algorithm == HashAlgorithm.SHA256:
            h = hashlib.sha256()
            h.update(combined.encode())
            return h.hexdigest()
        elif self.algorithm == HashAlgorithm.KECCAK256:
            try:
                from Crypto.Hash import keccak
                k = keccak.new(digest_bits=256)
                k.update(combined.encode())
                return k.hexdigest()
            except ImportError:
                h = hashlib.sha256()
                h.update(combined.encode())
                return h.hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def get_proof(self, leaf_index: int) -> MerkleProof:
        """Generate proof for a leaf.

        Args:
            leaf_index: Index of the leaf

        Returns:
            Merkle proof
        """
        if leaf_index >= len(self.leaves):
            raise IndexError(f"Leaf index {leaf_index} out of range")

        if not self.root_hash:
            raise RuntimeError("Tree not built")

        leaf = self.leaves[leaf_index]
        leaf_hash = leaf.hash(self.algorithm)

        # Collect siblings on path to root
        siblings = []
        index = leaf_index

        for level in range(len(self.tree) - 1):
            level_hashes = self.tree[level]

            # Find sibling
            if index % 2 == 0:
                # This is a left child
                if index + 1 < len(level_hashes):
                    sibling = level_hashes[index + 1]
                else:
                    # Right sibling doesn't exist, use self
                    sibling = level_hashes[index]
            else:
                # This is a right child
                sibling = level_hashes[index - 1]

            siblings.append(sibling)

            # Move to parent position
            index = index // 2

        return MerkleProof(
            leaf_index=leaf_index,
            leaf_hash=leaf_hash,
            siblings=siblings,
            root_hash=self.root_hash,
            tree_depth=len(self.tree),
        )

    def verify_proof(self, proof: MerkleProof) -> bool:
        """Verify a Merkle proof.

        Args:
            proof: Merkle proof

        Returns:
            True if proof is valid
        """
        if proof.root_hash != self.root_hash:
            logger.warning("Proof root hash mismatch")
            return False

        # Reconstruct path from leaf to root
        current_hash = proof.leaf_hash
        index = proof.leaf_index

        for sibling in proof.siblings:
            if index % 2 == 0:
                current_hash = self._hash_pair(current_hash, sibling)
            else:
                current_hash = self._hash_pair(sibling, current_hash)

            index = index // 2

        return current_hash == self.root_hash

    def get_statistics(self) -> TreeStatistics:
        """Get tree statistics.

        Returns:
            Tree statistics
        """
        return TreeStatistics(
            total_leaves=len(self.leaves),
            tree_depth=len(self.tree),
            root_hash=self.root_hash or "",
            generation_time_ms=self.generation_time * 1000,
            generation_timestamp=self.generation_timestamp or datetime.utcnow(),
            hash_algorithm=self.algorithm.value,
            leaf_hashes=[
                leaf.hash(self.algorithm)
                for leaf in self.leaves
            ],
        )

    def serialize(self) -> Dict[str, Any]:
        """Serialize tree for storage.

        Returns:
            Serialized tree data
        """
        return {
            "algorithm": self.algorithm.value,
            "root_hash": self.root_hash,
            "tree": {
                str(level): hashes
                for level, hashes in self.tree.items()
            },
            "leaves": [
                {
                    "customer_id": leaf.customer_id,
                    "anonymized_id": leaf.anonymized_id,
                    "assets": {k: float(v) for k, v in leaf.assets.items()},
                    "timestamp": leaf.timestamp.isoformat(),
                    "nonce": leaf.nonce,
                    "metadata": leaf.metadata,
                }
                for leaf in self.leaves
            ],
            "generation_time": self.generation_time,
            "generation_timestamp": self.generation_timestamp.isoformat() if self.generation_timestamp else None,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "MerkleTree":
        """Deserialize tree from storage.

        Args:
            data: Serialized tree data

        Returns:
            Merkle tree instance
        """
        tree = cls(algorithm=HashAlgorithm(data["algorithm"]))

        # Reconstruct leaves
        for leaf_data in data.get("leaves", []):
            leaf = MerkleLeaf(
                customer_id=leaf_data["customer_id"],
                anonymized_id=leaf_data["anonymized_id"],
                assets={k: Decimal(str(v)) for k, v in leaf_data["assets"].items()},
                timestamp=datetime.fromisoformat(leaf_data["timestamp"]),
                nonce=leaf_data["nonce"],
                metadata=leaf_data.get("metadata", {}),
            )
            tree.add_leaf(leaf)

        # Reconstruct tree structure
        tree.tree = {
            int(level): hashes
            for level, hashes in data.get("tree", {}).items()
        }

        tree.root_hash = data.get("root_hash")
        tree.generation_time = data.get("generation_time", 0)

        if data.get("generation_timestamp"):
            tree.generation_timestamp = datetime.fromisoformat(
                data["generation_timestamp"]
            )

        return tree

    def export_root_for_publication(self) -> Dict[str, str]:
        """Export root hash for public publication.

        Args:
            None

        Returns:
            Root hash with metadata
        """
        return {
            "root_hash": self.root_hash or "",
            "algorithm": self.algorithm.value,
            "total_leaves": len(self.leaves),
            "tree_depth": len(self.tree),
            "timestamp": self.generation_timestamp.isoformat() if self.generation_timestamp else "",
        }

    def get_leaf_verification_data(self, leaf_index: int) -> Dict[str, Any]:
        """Get all data needed for a customer to verify their inclusion.

        Args:
            leaf_index: Index of leaf

        Returns:
            Customer verification data package
        """
        if leaf_index >= len(self.leaves):
            raise IndexError("Leaf index out of range")

        leaf = self.leaves[leaf_index]
        proof = self.get_proof(leaf_index)

        return {
            "customer_id": leaf.customer_id,
            "anonymized_id": leaf.anonymized_id,
            "assets": {k: float(v) for k, v in leaf.assets.items()},
            "leaf_hash": proof.leaf_hash,
            "proof": proof.to_dict(),
            "root_hash": self.root_hash,
            "instructions": "Verify that hash(leaf_data) + siblings = root_hash",
        }

    async def generate_batch_proofs(
        self,
        leaf_indices: List[int],
    ) -> List[MerkleProof]:
        """Generate proofs for multiple leaves.

        Args:
            leaf_indices: List of leaf indices

        Returns:
            List of proofs
        """
        proofs = []

        for i, index in enumerate(leaf_indices):
            if i % self.batch_size == 0 and i > 0:
                await asyncio.sleep(0)

            proofs.append(self.get_proof(index))

        return proofs

    def get_leaf_count(self) -> int:
        """Get total leaf count.

        Returns:
            Number of leaves
        """
        return len(self.leaves)

    def get_tree_depth(self) -> int:
        """Get tree depth.

        Returns:
            Tree depth
        """
        return len(self.tree)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"MerkleTree(leaves={len(self.leaves)}, "
            f"depth={len(self.tree)}, "
            f"root={'present' if self.root_hash else 'not built'})"
        )
