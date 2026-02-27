"""Integration tests for Merkle tree API."""
import pytest
import asyncio
from fastapi.testclient import TestClient
from datetime import datetime
from decimal import Decimal

from app.services.merkle.merkle_engine import (
    MerkleTree,
    MerkleLeaf,
)


@pytest.mark.integration
class TestMerkleTreeGeneration:
    """Integration tests for Merkle tree generation."""

    @pytest.mark.asyncio
    async def test_generate_merkle_tree(self):
        """Test generating a complete Merkle tree."""
        tree = MerkleTree()

        # Add customer liabilities
        for i in range(100):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"anon_{i}",
                assets={"ETH": Decimal("10"), "USDC": Decimal("1000")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        assert tree.root_hash is not None
        assert tree.get_leaf_count() == 100

    @pytest.mark.asyncio
    async def test_get_merkle_root(self):
        """Test retrieving Merkle root."""
        tree = MerkleTree()

        for i in range(10):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"anon_{i}",
                assets={"BTC": Decimal("1")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        root = tree.export_root_for_publication()

        assert root["root_hash"] is not None
        assert root["total_leaves"] == 10
        assert root["algorithm"] == "sha256"


@pytest.mark.integration
class TestCustomerVerification:
    """Integration tests for customer Merkle proof verification."""

    @pytest.mark.asyncio
    async def test_verify_customer_proof_valid(self):
        """Test customer can verify valid proof."""
        tree = MerkleTree()

        customers = []
        for i in range(50):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"anon_{i}",
                assets={"ETH": Decimal("5"), "USDC": Decimal("500")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)
            customers.append(leaf)

        await tree.build()

        # Get proof for customer 0
        proof = tree.get_proof(0)

        # Verify proof
        assert tree.verify_proof(proof) is True

    @pytest.mark.asyncio
    async def test_verify_customer_proof_invalid(self):
        """Test that invalid proof fails verification."""
        tree = MerkleTree()

        for i in range(20):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"anon_{i}",
                assets={"ETH": Decimal("5")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        # Get valid proof
        proof = tree.get_proof(0)

        # Tamper with proof
        original_leaf_hash = proof.leaf_hash
        proof.leaf_hash = "0" * 64

        # Verification should fail
        assert tree.verify_proof(proof) is False

        # Restore and verify it works
        proof.leaf_hash = original_leaf_hash
        assert tree.verify_proof(proof) is True


@pytest.mark.integration
class TestMerkleTreeStats:
    """Integration tests for Merkle tree statistics."""

    @pytest.mark.asyncio
    async def test_merkle_tree_stats(self):
        """Test getting Merkle tree statistics."""
        tree = MerkleTree()

        for i in range(1000):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"anon_{i}",
                assets={"USDC": Decimal("100")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        stats = tree.get_statistics()

        assert stats.total_leaves == 1000
        assert stats.root_hash == tree.root_hash
        assert stats.hash_algorithm == "sha256"
        assert stats.generation_time_ms > 0
        assert len(stats.leaf_hashes) == 1000


@pytest.mark.integration
class TestMerkleProofAPI:
    """Integration tests for Merkle proof API endpoints."""

    @pytest.mark.asyncio
    async def test_batch_proof_generation(self):
        """Test generating multiple proofs efficiently."""
        tree = MerkleTree()

        for i in range(100):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"anon_{i}",
                assets={"ETH": Decimal("10")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        # Generate proofs for multiple customers
        indices = [0, 25, 50, 75, 99]
        proofs = await tree.generate_batch_proofs(indices)

        assert len(proofs) == len(indices)

        # Verify all proofs
        for proof in proofs:
            assert tree.verify_proof(proof) is True

    @pytest.mark.asyncio
    async def test_leaf_verification_data_package(self):
        """Test getting customer verification data package."""
        tree = MerkleTree()

        for i in range(10):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:03d}",
                anonymized_id=f"anon_{i}",
                assets={"USDC": Decimal("1000"), "ETH": Decimal("5")},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)

        await tree.build()

        # Get verification data for customer 0
        verification_data = tree.get_leaf_verification_data(0)

        assert "customer_id" in verification_data
        assert "proof" in verification_data
        assert "root_hash" in verification_data
        assert "assets" in verification_data
        assert verification_data["customer_id"] == "CUST-000"


@pytest.mark.integration
class TestMerkleSerializationAPI:
    """Integration tests for Merkle tree serialization."""

    @pytest.mark.asyncio
    async def test_serialize_and_deserialize_tree(self):
        """Test serializing and deserializing Merkle tree."""
        tree = MerkleTree()

        original_data = []
        for i in range(50):
            leaf = MerkleLeaf(
                customer_id=f"CUST-{i:05d}",
                anonymized_id=f"anon_{i}",
                assets={"ETH": Decimal(str(10 + i % 5))},
                timestamp=datetime.utcnow(),
                nonce=f"nonce_{i}",
            )
            tree.add_leaf(leaf)
            original_data.append(leaf.customer_id)

        await tree.build()
        original_root = tree.root_hash

        # Serialize
        serialized = tree.serialize()

        # Verify serialized data
        assert serialized["root_hash"] == original_root
        assert len(serialized["leaves"]) == 50

        # Deserialize
        restored = MerkleTree.deserialize(serialized)

        # Verify restored tree
        assert restored.root_hash == original_root
        assert restored.get_leaf_count() == 50

        # Verify proofs still work with restored tree
        proof = restored.get_proof(0)
        assert restored.verify_proof(proof) is True
