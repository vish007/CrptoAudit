"""Unit tests for Merkle tree engine."""
import asyncio
import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from app.services.merkle.merkle_engine import (
    MerkleTree,
    MerkleLeaf,
    MerkleProof,
    HashAlgorithm,
    TreeStatistics,
)


@pytest.mark.unit
class TestMerkleLeaf:
    """Tests for MerkleLeaf class."""

    def test_leaf_creation(self):
        """Test creating a leaf node."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5"), "USDC": Decimal("1000")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        assert leaf.customer_id == "CUST-001"
        assert leaf.anonymized_id == "hash_001"
        assert leaf.assets["ETH"] == Decimal("10.5")

    def test_leaf_to_dict(self):
        """Test leaf conversion to dictionary."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        leaf_dict = leaf.to_dict()
        assert leaf_dict["customer_id"] == "CUST-001"
        assert leaf_dict["assets"]["ETH"] == 10.5

    def test_leaf_to_json(self):
        """Test leaf conversion to JSON."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        json_str = leaf.to_json()
        assert "CUST-001" in json_str
        assert "ETH" in json_str

    def test_leaf_hash_sha256(self):
        """Test leaf SHA256 hash."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        leaf_hash = leaf.hash(HashAlgorithm.SHA256)
        assert isinstance(leaf_hash, str)
        assert len(leaf_hash) == 64  # SHA256 hex is 64 chars

    def test_leaf_hash_keccak256(self):
        """Test leaf Keccak256 hash."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        leaf_hash = leaf.hash(HashAlgorithm.KECCAK256)
        assert isinstance(leaf_hash, str)
        assert len(leaf_hash) >= 64

    def test_leaf_hash_deterministic(self):
        """Test that same leaf produces same hash."""
        leaf1 = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            nonce="nonce_123",
        )

        leaf2 = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            nonce="nonce_123",
        )

        assert leaf1.hash() == leaf2.hash()


@pytest.mark.unit
class TestMerkleTree:
    """Tests for MerkleTree class."""

    @pytest.mark.asyncio
    async def test_build_tree_single_leaf(self):
        """Test building tree with single leaf."""
        tree = MerkleTree()
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10.5")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )
        tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert len(tree.tree) > 0

    @pytest.mark.asyncio
    async def test_build_tree_multiple_leaves(self):
        """Test building tree with multiple leaves."""
        tree = MerkleTree()

        for i in range(5):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal(str(10 + i))},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert tree.get_leaf_count() == 5

    @pytest.mark.asyncio
    async def test_build_tree_power_of_two_leaves(self):
        """Test building tree with power of 2 leaves."""
        tree = MerkleTree()

        # Add 8 leaves (power of 2)
        for i in range(8):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert tree.get_leaf_count() == 8

    @pytest.mark.asyncio
    async def test_build_tree_non_power_of_two_leaves(self):
        """Test building tree with non-power of 2 leaves."""
        tree = MerkleTree()

        # Add 7 leaves (not power of 2)
        for i in range(7):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert tree.get_leaf_count() == 7

    @pytest.mark.asyncio
    async def test_generate_proof_valid(self):
        """Test generating proof for valid leaf."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        proof = tree.get_proof(0)

        assert isinstance(proof, MerkleProof)
        assert proof.leaf_index == 0
        assert len(proof.siblings) > 0
        assert proof.root_hash == tree.root_hash

    @pytest.mark.asyncio
    async def test_verify_proof_valid(self):
        """Test verifying valid proof."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        proof = tree.get_proof(0)

        assert tree.verify_proof(proof) is True

    @pytest.mark.asyncio
    async def test_verify_proof_invalid_tampered_data(self):
        """Test that proof fails for tampered data."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        proof = tree.get_proof(0)

        # Tamper with proof
        proof.leaf_hash = "0" * 64

        assert tree.verify_proof(proof) is False

    @pytest.mark.asyncio
    async def test_verify_proof_wrong_root(self):
        """Test that proof fails with wrong root."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        proof = tree.get_proof(0)

        # Change root hash
        proof.root_hash = "0" * 64

        assert tree.verify_proof(proof) is False

    @pytest.mark.asyncio
    async def test_merkle_root_deterministic(self):
        """Test that root is deterministic for same data."""
        async def build_tree():
            tree = MerkleTree()
            for i in range(5):
                leaf = MerkleLeaf(
                    customer_id=f"CUST-{i:03d}",
                    anonymized_id=f"hash_{i}",
                    assets={"ETH": Decimal("10")},
                    timestamp=datetime(2024, 1, 1),
                    nonce=f"nonce_{i}",
                )
                tree.add_leaf(leaf)
            await tree.build()
            return tree.root_hash

        root1 = await build_tree()
        root2 = await build_tree()

        assert root1 == root2

    @pytest.mark.asyncio
    async def test_large_tree_1000_leaves(self):
        """Test building large tree with 1000 leaves."""
        tree = MerkleTree()

        for i in range(1000):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert tree.get_leaf_count() == 1000

        # Verify a proof works
        proof = tree.get_proof(500)
        assert tree.verify_proof(proof) is True

    def test_empty_tree_raises_error(self):
        """Test that building empty tree raises error."""
        tree = MerkleTree()

        with pytest.raises(ValueError, match="No leaves to build tree"):
            asyncio.run(tree.build())

    @pytest.mark.asyncio
    async def test_tree_serialization_deserialization(self):
        """Test serializing and deserializing tree."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime(2024, 1, 1),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        original_root = tree.root_hash

        # Serialize
        serialized = tree.serialize()

        # Deserialize
        restored_tree = MerkleTree.deserialize(serialized)

        assert restored_tree.root_hash == original_root

    def test_sha256_algorithm(self):
        """Test SHA256 hash algorithm."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        hash1 = leaf.hash(HashAlgorithm.SHA256)
        hash2 = leaf.hash(HashAlgorithm.SHA256)

        assert hash1 == hash2
        assert len(hash1) == 64

    def test_keccak256_algorithm(self):
        """Test Keccak256 hash algorithm."""
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )

        hash_val = leaf.hash(HashAlgorithm.KECCAK256)
        assert isinstance(hash_val, str)
        assert len(hash_val) >= 64

    @pytest.mark.asyncio
    async def test_leaf_hash_format(self):
        """Test leaf hash format is hex string."""
        tree = MerkleTree()
        leaf = MerkleLeaf(
            customer_id="CUST-001",
            anonymized_id="hash_001",
            assets={"ETH": Decimal("10")},
            timestamp=datetime.utcnow(),
            nonce="nonce_123",
        )
        tree.add_leaf(leaf)

        await tree.build()

        # All hashes should be valid hex strings
        for level_hashes in tree.tree.values():
            for hash_val in level_hashes:
                assert all(c in "0123456789abcdef" for c in hash_val.lower())

    @pytest.mark.asyncio
    async def test_batch_proof_generation(self):
        """Test generating proofs for multiple leaves."""
        tree = MerkleTree()

        for i in range(10):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        leaf_indices = [0, 3, 5, 9]
        proofs = await tree.generate_batch_proofs(leaf_indices)

        assert len(proofs) == 4
        for i, proof in enumerate(proofs):
            assert proof.leaf_index == leaf_indices[i]

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting tree statistics."""
        tree = MerkleTree()

        for i in range(5):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()
        stats = tree.get_statistics()

        assert isinstance(stats, TreeStatistics)
        assert stats.total_leaves == 5
        assert stats.root_hash == tree.root_hash
        assert stats.hash_algorithm == "sha256"
        assert stats.generation_time_ms > 0

    @pytest.mark.asyncio
    async def test_get_leaf_verification_data(self):
        """Test getting leaf verification data."""
        tree = MerkleTree()

        for i in range(4):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"hash_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        verification_data = tree.get_leaf_verification_data(0)

        assert "customer_id" in verification_data
        assert "proof" in verification_data
        assert "root_hash" in verification_data
        assert verification_data["customer_id"] == "CUST-000"
