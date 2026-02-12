"""Merkle tree generation and verification endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import hashlib
import json

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.engagement import Engagement
from app.models.merkle import MerkleTree, MerkleLeaf, MerkleProof
from app.schemas.merkle import (
    MerkleTreeResponse,
    MerkleProofResponse,
    MerkleVerificationRequest,
    MerkleVerificationResponse,
    MerkleStatsResponse,
    MerkleTreeCreate,
)

router = APIRouter(prefix="/engagements", tags=["merkle"])


def calculate_merkle_root(leaves: List[str]) -> str:
    """
    Calculate merkle root from leaf hashes.

    Args:
        leaves: List of leaf hashes

    Returns:
        Root hash
    """
    if not leaves:
        return hashlib.sha256(b"").hexdigest()

    current_level = leaves.copy()

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left

            combined = left + right
            parent_hash = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(parent_hash)

        current_level = next_level

    return current_level[0]


@router.post("/{engagement_id}/merkle/generate", response_model=MerkleTreeResponse)
async def generate_merkle_tree(
    engagement_id: str,
    merkle_create: MerkleTreeCreate,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate merkle tree for customer liabilities.

    Args:
        engagement_id: Engagement ID
        merkle_create: Generation parameters
        current_user: Current authenticated user
        session: Database session

    Returns:
        Generated merkle tree

    Raises:
        HTTPException: If engagement not found
    """
    from datetime import datetime, timezone
    from app.models.asset import CustomerLiability

    tenant_id = extract_tenant_id(current_user)
    user_id = current_user.get("sub")

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can generate merkle trees",
        )

    # Get customer liabilities for asset
    from app.models.engagement import EngagementAsset
    stmt = select(EngagementAsset).where(
        and_(
            EngagementAsset.engagement_id == engagement_id,
            EngagementAsset.asset_symbol == merkle_create.asset_symbol,
        )
    )
    result = await session.execute(stmt)
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    stmt = select(CustomerLiability).where(
        and_(
            CustomerLiability.engagement_id == engagement_id,
            CustomerLiability.asset_id == asset.id,
        )
    )
    result = await session.execute(stmt)
    liabilities = result.scalars().all()

    # Create tree
    leaf_hashes = []
    merkle_leaves = []

    for idx, liability in enumerate(liabilities):
        user_hash = hashlib.sha256(liability.anonymized_user_id.encode()).hexdigest()
        data_hash = hashlib.sha256(
            f"{liability.balance}".encode()
        ).hexdigest()

        leaf_data = {
            "user_id_hash": user_hash,
            "balance": str(liability.balance),
        }

        leaf_hash = hashlib.sha256(
            json.dumps(leaf_data).encode()
        ).hexdigest()

        leaf_hashes.append(leaf_hash)
        merkle_leaves.append(
            {
                "index": idx,
                "user_hash": user_hash,
                "data_hash": data_hash,
                "leaf_hash": leaf_hash,
                "balance_snapshot": leaf_data,
            }
        )

    root_hash = calculate_merkle_root(leaf_hashes)

    # Save to database
    merkle_tree = MerkleTree(
        engagement_id=engagement_id,
        root_hash=root_hash,
        total_leaves=len(merkle_leaves),
        generated_at=datetime.now(timezone.utc),
        algorithm=merkle_create.algorithm,
        status="GENERATING",
        asset_symbol=merkle_create.asset_symbol,
        created_by=user_id,
    )

    session.add(merkle_tree)
    await session.flush()

    # Add leaves
    for leaf_data in merkle_leaves:
        merkle_leaf = MerkleLeaf(
            tree_id=merkle_tree.id,
            leaf_index=leaf_data["index"],
            user_hash=leaf_data["user_hash"],
            data_hash=leaf_data["data_hash"],
            balance_snapshot_json=json.dumps(leaf_data["balance_snapshot"]),
            leaf_hash=leaf_data["leaf_hash"],
            created_by=user_id,
        )
        session.add(merkle_leaf)

    merkle_tree.status = "PUBLISHED"
    await session.commit()
    await session.refresh(merkle_tree)

    return merkle_tree


@router.get("/{engagement_id}/merkle/root", response_model=dict)
async def get_merkle_root(
    engagement_id: str,
    asset_symbol: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get merkle root for asset.

    Args:
        engagement_id: Engagement ID
        asset_symbol: Asset symbol
        current_user: Current authenticated user
        session: Database session

    Returns:
        Merkle root hash
    """
    stmt = select(MerkleTree).where(
        and_(
            MerkleTree.engagement_id == engagement_id,
            MerkleTree.asset_symbol == asset_symbol,
            MerkleTree.status == "PUBLISHED",
        )
    )
    result = await session.execute(stmt)
    tree = result.scalar_one_or_none()

    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merkle tree not found",
        )

    return {
        "root_hash": tree.root_hash,
        "total_leaves": tree.total_leaves,
        "algorithm": tree.algorithm,
        "generated_at": tree.generated_at,
    }


@router.post("/merkle/verify", response_model=MerkleVerificationResponse)
async def verify_merkle_proof(
    verification_request: MerkleVerificationRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Public endpoint to verify merkle proof (for customers).

    Args:
        verification_request: Proof verification data
        session: Database session

    Returns:
        Verification result
    """
    proof_path = verification_request.proof_path
    current_hash = verification_request.leaf_hash
    leaf_index = verification_request.leaf_index

    # Reconstruct root
    for proof_item in proof_path:
        sibling_hash = proof_item.get("hash")
        direction = proof_item.get("direction", "right")

        if direction == "right":
            combined = current_hash + sibling_hash
        else:
            combined = sibling_hash + current_hash

        current_hash = hashlib.sha256(combined.encode()).hexdigest()

    is_valid = current_hash == verification_request.root_hash

    from datetime import datetime, timezone
    return MerkleVerificationResponse(
        is_valid=is_valid,
        root_hash=verification_request.root_hash,
        message="Proof verified successfully" if is_valid else "Proof verification failed",
        verified_at=datetime.now(timezone.utc),
    )


@router.get("/{engagement_id}/merkle/stats", response_model=MerkleStatsResponse)
async def get_merkle_stats(
    engagement_id: str,
    asset_symbol: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get merkle tree statistics.

    Args:
        engagement_id: Engagement ID
        asset_symbol: Asset symbol
        current_user: Current authenticated user
        session: Database session

    Returns:
        Merkle tree stats
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    stmt = select(MerkleTree).where(
        and_(
            MerkleTree.engagement_id == engagement_id,
            MerkleTree.asset_symbol == asset_symbol,
        )
    )
    result = await session.execute(stmt)
    tree = result.scalar_one_or_none()

    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merkle tree not found",
        )

    from sqlalchemy import func
    stmt = select(func.count()).select_from(MerkleProof).where(
        MerkleProof.tree_id == tree.id
    )
    result = await session.execute(stmt)
    proof_count = result.scalar()

    from sqlalchemy import func
    stmt = select(func.sum(MerkleProof.verification_count)).where(
        MerkleProof.tree_id == tree.id
    )
    result = await session.execute(stmt)
    total_verifications = result.scalar() or 0

    return MerkleStatsResponse(
        tree_id=tree.id,
        engagement_id=engagement_id,
        asset_symbol=asset_symbol,
        status=tree.status,
        total_leaves=tree.total_leaves,
        total_proofs_generated=proof_count,
        total_verifications=total_verifications,
        root_hash=tree.root_hash,
        algorithm=tree.algorithm,
        generated_at=tree.generated_at,
        last_verified_at=tree.updated_at,
    )
