"""Pydantic schemas for Merkle tree operations."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MerkleLeafBase(BaseModel):
    """Base merkle leaf schema."""

    leaf_index: int = Field(..., ge=0)
    user_hash: str = Field(..., min_length=1, max_length=255)
    data_hash: str = Field(..., min_length=1, max_length=255)
    balance_snapshot_json: Dict[str, Any]


class MerkleLeafResponse(MerkleLeafBase):
    """Merkle leaf response."""

    id: str
    tree_id: str
    leaf_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MerkleTreeBase(BaseModel):
    """Base merkle tree schema."""

    root_hash: str = Field(..., min_length=1, max_length=255)
    total_leaves: int = Field(..., ge=1)
    algorithm: str = Field(..., pattern="^(SHA256|KECCAK256)$")
    asset_symbol: str = Field(..., min_length=1, max_length=20)


class MerkleTreeCreate(BaseModel):
    """Create merkle tree request."""

    asset_symbol: str = Field(..., min_length=1, max_length=20)
    algorithm: str = Field(default="SHA256", pattern="^(SHA256|KECCAK256)$")


class MerkleTreeResponse(MerkleTreeBase):
    """Merkle tree response."""

    id: str
    engagement_id: str
    status: str
    generated_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MerkleProofBase(BaseModel):
    """Base merkle proof schema."""

    proof_path_json: List[Dict[str, str]]  # List of {hash, direction}


class MerkleProofResponse(MerkleProofBase):
    """Merkle proof response."""

    id: str
    tree_id: str
    leaf_id: str
    verified_at: Optional[datetime]
    verification_count: int
    last_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MerkleVerificationRequest(BaseModel):
    """Public merkle verification request."""

    root_hash: str = Field(..., min_length=1, max_length=255)
    leaf_hash: str = Field(..., min_length=1, max_length=255)
    proof_path: List[Dict[str, str]]  # List of {hash, direction}
    leaf_index: int = Field(..., ge=0)


class MerkleVerificationResponse(BaseModel):
    """Merkle verification response."""

    is_valid: bool
    root_hash: str
    message: str
    verified_at: datetime


class MerklePublishRequest(BaseModel):
    """Publish merkle tree request."""

    pass


class MerkleStatsResponse(BaseModel):
    """Merkle tree statistics response."""

    tree_id: str
    engagement_id: str
    asset_symbol: str
    status: str
    total_leaves: int
    total_proofs_generated: int
    total_verifications: int
    root_hash: str
    algorithm: str
    generated_at: datetime
    last_verified_at: Optional[datetime]
