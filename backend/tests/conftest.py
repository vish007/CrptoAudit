"""Pytest configuration and fixtures for SimplyFI PoR Platform."""
import asyncio
import os
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from tests.factories import UserFactory, TenantFactory, TokenFactory


# Configure pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db():
    """Create an in-memory SQLite database for testing."""
    # Use SQLite in-memory database for tests
    database_url = "sqlite:///:memory:"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(test_db):
    """Provide database session for tests."""
    return test_db


@pytest.fixture
def client(test_db):
    """Create a FastAPI test client."""

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def async_client(test_db):
    """Create an async FastAPI test client."""
    from httpx import AsyncClient

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()

    app.dependency_overrides[get_db] = override_get_db

    async def _async_client():
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

    return _async_client


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock(return_value=1)
    mock.exists = AsyncMock(return_value=False)
    return mock


@pytest.fixture
def mock_s3():
    """Create a mock S3 client."""
    mock = AsyncMock()
    mock.upload_file = AsyncMock(return_value="s3://bucket/key")
    mock.download_file = AsyncMock(return_value=b"file content")
    mock.delete_file = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def user_factory():
    """Provide user factory."""
    return UserFactory


@pytest.fixture
def tenant_factory():
    """Provide tenant factory."""
    return TenantFactory


@pytest.fixture
def token_factory():
    """Provide token factory."""
    return TokenFactory


@pytest.fixture
def sample_user_data():
    """Provide sample user data."""
    tenant_id = str(uuid.uuid4())
    return {
        "tenant_id": tenant_id,
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "TestPassword123!",
        "is_active": True,
        "is_superadmin": False,
    }


@pytest.fixture
def sample_tenant_data():
    """Provide sample tenant data."""
    return {
        "name": "Test Auditor Firm",
        "type": "AUDITOR",
        "vara_license_number": "VARA-2024-001",
        "status": "ACTIVE",
    }


@pytest.fixture
def sample_engagement_data():
    """Provide sample engagement data."""
    return {
        "title": "Annual PoR Audit",
        "description": "Comprehensive Proof of Reserves audit",
        "status": "PLANNING",
    }


@pytest.fixture
def sample_asset_data():
    """Provide sample asset data."""
    return {
        "asset_name": "ETH",
        "blockchain": "ethereum",
        "total_balance": 1000.0,
        "wallet_count": 5,
    }


@pytest.fixture
def auth_headers(token_factory):
    """Create authorization headers with valid token."""
    token = token_factory.build(
        user_id=str(uuid.uuid4()),
        email="testuser@example.com",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(token_factory):
    """Create authorization headers with admin token."""
    token = token_factory.admin_build(
        user_id=str(uuid.uuid4()),
        email="admin@example.com",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_ethereum_adapter():
    """Mock Ethereum blockchain adapter."""
    mock = AsyncMock()
    mock.get_balance = AsyncMock(
        return_value=1000.5
    )
    mock.verify_address = AsyncMock(return_value=True)
    mock.get_erc20_balance = AsyncMock(return_value=5000.0)
    return mock


@pytest.fixture
def mock_bitcoin_adapter():
    """Mock Bitcoin blockchain adapter."""
    mock = AsyncMock()
    mock.get_balance = AsyncMock(return_value=50.25)
    mock.verify_address = AsyncMock(return_value=True)
    mock.get_utxos = AsyncMock(return_value=[
        {
            "txid": "abc123",
            "vout": 0,
            "value": 50.25,
            "confirmations": 100
        }
    ])
    return mock


@pytest.fixture
def mock_solana_adapter():
    """Mock Solana blockchain adapter."""
    mock = AsyncMock()
    mock.get_balance = AsyncMock(return_value=100.0)
    mock.verify_address = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_blockchains(
    mock_ethereum_adapter,
    mock_bitcoin_adapter,
    mock_solana_adapter,
):
    """Provide mocked blockchain adapters."""
    return {
        "ethereum": mock_ethereum_adapter,
        "bitcoin": mock_bitcoin_adapter,
        "solana": mock_solana_adapter,
    }


@pytest.fixture
def mock_blockchain_data():
    """Provide mock blockchain verification data."""
    return {
        "ethereum": {
            "0x1234567890123456789012345678901234567890": 1000.5
        },
        "bitcoin": {
            "1A1z7agoat7qsweQvUwhwYBCn1qWu5Hspp": 50.25
        },
        "solana": {
            "9B5X4z5zzJGLccBx86ggHmwYmUo9Uu7XuUTqMacHj9tZ": 100.0
        },
    }


@pytest.fixture
def cleanup_files():
    """Fixture to cleanup test files after tests."""
    files = []

    def add_file(filepath):
        files.append(filepath)
        return filepath

    yield add_file

    for filepath in files:
        if os.path.exists(filepath):
            os.remove(filepath)


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "e2e: end-to-end tests")
    config.addinivalue_line("markers", "slow: slow tests")
    config.addinivalue_line("markers", "async: async tests")
