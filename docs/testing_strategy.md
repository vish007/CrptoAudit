# SimplyFI PoR Platform: Testing Strategy

**Document Version**: 1.0
**Last Updated**: February 2026
**Target Audience**: QA, Engineering, Product

---

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Pyramid](#test-pyramid)
3. [Coverage Goals & Metrics](#coverage-goals--metrics)
4. [Unit Testing](#unit-testing)
5. [Integration Testing](#integration-testing)
6. [End-to-End Testing](#end-to-end-testing)
7. [Performance Testing](#performance-testing)
8. [Test Data Strategy](#test-data-strategy)
9. [CI/CD Integration](#cicd-integration)
10. [Manual Testing](#manual-testing)

---

## Testing Philosophy

The SimplyFI PoR platform requires multiple layers of testing to ensure:

1. **Correctness**: Business logic works as specified
2. **Security**: No vulnerabilities or data leaks
3. **Reliability**: System behaves consistently under load
4. **Compliance**: VARA regulations and audit standards met
5. **Performance**: Response times acceptable for user workflows

**Testing Approach**: Test Pyramid with heavy unit test base, moderate integration tests, and targeted E2E tests.

```
        /\
       /E2E\         High confidence, slower, expensive
      /-----\
     /       \
    / INT.   \       Moderate speed, catch integration issues
   /---------\
  /           \
 /   UNIT     \      Fast, isolated, comprehensive coverage
/             \
```

---

## Test Pyramid

### Level 1: Unit Tests (60% of test suite)

**Purpose**: Verify individual functions and classes work correctly in isolation

**Characteristics**:
- Fast (< 100ms per test)
- No external dependencies (mocked)
- Run on every code change
- High code coverage

**Examples**:
- Merkle tree hash computation
- Reserve ratio calculation
- Blockchain address validation
- JWT token generation/verification
- User permission checks

### Level 2: Integration Tests (30% of test suite)

**Purpose**: Verify components work together correctly

**Characteristics**:
- Moderate speed (100ms - 1 second per test)
- Use test database and Redis
- Test API endpoints with realistic payloads
- Run in CI/CD pipeline

**Examples**:
- API endpoint returns correct response
- Database operations (create, read, update)
- Celery task execution
- Cache invalidation workflows
- Multi-step transaction flows

### Level 3: End-to-End Tests (10% of test suite)

**Purpose**: Verify complete user workflows work from UI to database

**Characteristics**:
- Slower (1-10 seconds per test)
- Test critical happy paths only
- Use staging environment
- Run before production deployment

**Examples**:
- VASP onboarding workflow (signup → asset config → first audit)
- Engagement lifecycle (creation → verification → report)
- Merkle tree verification (customer portal flow)
- Report generation and download

---

## Coverage Goals & Metrics

### Target Coverage by Module

| Module | Target Coverage | Priority | Notes |
|--------|-----------------|----------|-------|
| **Core Business Logic** | 90% | Critical | Merkle engine, reserve ratio calc, verification logic |
| **API Endpoints** | 85% | Critical | REST endpoints, validation, error handling |
| **Blockchain Adapters** | 80% | High | Provider integration, fallback handling, error cases |
| **Merkle Tree Engine** | 95% | Critical | Cryptographic correctness paramount |
| **AI/ML Services** | 75% | Medium | LLaMA integration, fallback to rule-based |
| **Authentication** | 90% | Critical | JWT, MFA, RBAC, session management |
| **Database Models** | 85% | High | ORM operations, relationships, constraints |
| **Notification Services** | 70% | Low | Email, SMS, WebSocket (covered by integration tests) |
| **Utility Functions** | 75% | Low | Formatters, validators, helpers |

### Coverage Metrics

```bash
# Run coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html

# Expected output:
# app/core/security.py          95%
# app/services/merkle/         96%
# app/services/blockchain/     82%
# app/api/v1/endpoints/        87%
# TOTAL                         88%
```

### Coverage Thresholds

- **PR Rejection**: Coverage decreases by >1%
- **Warning**: Coverage < target for module
- **Gate**: Overall coverage must be ≥85% to merge to main

---

## Unit Testing

### Testing Framework & Tools

```python
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = """
    -v
    --tb=short
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
"""

# pytest.ini
[pytest]
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests (skip by default)
    security: Security tests
```

### Example Unit Tests

**Test Merkle Tree Hash Computation**:
```python
# tests/unit/test_merkle_engine.py
import pytest
from decimal import Decimal
from datetime import datetime
from app.services.merkle.merkle_engine import MerkleLeaf, HashAlgorithm

@pytest.mark.unit
class TestMerkleLeaf:
    def test_merkle_leaf_hash_sha256(self):
        """Verify SHA-256 hash computation."""
        leaf = MerkleLeaf(
            customer_id="cust-123",
            anonymized_id=hashlib.sha256(b"cust-123").hexdigest(),
            assets={"BTC": Decimal("1.5"), "ETH": Decimal("10")},
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            nonce="nonce-abc"
        )

        # Hash should be deterministic
        hash1 = leaf.hash(HashAlgorithm.SHA256)
        hash2 = leaf.hash(HashAlgorithm.SHA256)
        assert hash1 == hash2

        # Hash should be 64 hex chars (256 bits)
        assert len(hash1) == 64
        assert all(c in '0123456789abcdef' for c in hash1)

    def test_merkle_leaf_to_json_deterministic(self):
        """Verify JSON serialization is deterministic."""
        leaf = MerkleLeaf(
            customer_id="cust-123",
            anonymized_id="hash123",
            assets={"BTC": Decimal("1.5"), "ETH": Decimal("10")},
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            nonce="nonce"
        )

        json1 = leaf.to_json()
        json2 = leaf.to_json()
        assert json1 == json2

        # Keys should be sorted for deterministic ordering
        import json as json_lib
        parsed = json_lib.loads(json1)
        assert list(parsed.keys()) == sorted(parsed.keys())

    def test_merkle_leaf_hash_changes_with_data(self):
        """Verify hash changes when data changes."""
        leaf1 = MerkleLeaf(
            customer_id="cust-123",
            anonymized_id="hash123",
            assets={"BTC": Decimal("1.5")},
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            nonce="nonce"
        )

        leaf2 = MerkleLeaf(
            customer_id="cust-123",
            anonymized_id="hash123",
            assets={"BTC": Decimal("2.0")},  # Changed
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            nonce="nonce"
        )

        assert leaf1.hash() != leaf2.hash()
```

**Test Reserve Ratio Calculation**:
```python
# tests/unit/test_reserves.py
import pytest
from decimal import Decimal
from app.services.reserves import calculate_reserve_ratio

@pytest.mark.unit
class TestReserveRatio:
    def test_reserve_ratio_100_percent(self):
        """Verify 1:1 reserve (100%)."""
        assets = Decimal("1000")
        liabilities = Decimal("1000")
        ratio = calculate_reserve_ratio(assets, liabilities)
        assert ratio == Decimal("1.00")

    def test_reserve_ratio_150_percent(self):
        """Verify 1.5:1 reserve (150%)."""
        assets = Decimal("1500")
        liabilities = Decimal("1000")
        ratio = calculate_reserve_ratio(assets, liabilities)
        assert ratio == Decimal("1.50")

    def test_reserve_ratio_below_minimum(self):
        """Verify detection of under-reserve."""
        assets = Decimal("940")
        liabilities = Decimal("1000")
        ratio = calculate_reserve_ratio(assets, liabilities)
        assert ratio == Decimal("0.94")
        assert ratio < Decimal("0.95")  # Below VARA minimum

    def test_reserve_ratio_zero_liabilities(self):
        """Verify edge case: no liabilities."""
        assets = Decimal("1000")
        liabilities = Decimal("0")
        with pytest.raises(ZeroDivisionError):
            calculate_reserve_ratio(assets, liabilities)

    def test_reserve_ratio_precision(self):
        """Verify decimal precision preserved."""
        assets = Decimal("1000.123456789")
        liabilities = Decimal("999.987654321")
        ratio = calculate_reserve_ratio(assets, liabilities)
        # Should be >= 1.00 and preserve precision
        assert ratio > Decimal("1.00")
        assert str(ratio).count(".") == 1  # One decimal point
```

**Test Authentication**:
```python
# tests/unit/test_auth.py
import pytest
from datetime import datetime, timedelta
from app.core.security import (
    hash_password, verify_password,
    create_access_token, verify_token
)

@pytest.mark.unit
class TestAuthentication:
    def test_password_hashing_different_hashes(self):
        """Verify same password creates different hashes."""
        password = "StrongPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        # Different hashes due to salt
        assert hash1 != hash2
        # But both verify against original
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)

    def test_password_verification_wrong_password(self):
        """Verify wrong password fails verification."""
        password = "StrongPassword123!"
        hashed = hash_password(password)
        assert verify_password("WrongPassword", hashed) == False

    def test_jwt_token_creation_valid(self):
        """Verify JWT token creation and verification."""
        user_id = "user-123"
        expires_delta = timedelta(minutes=60)

        token = create_access_token(user_id, expires_delta)
        assert token
        assert token.startswith("eyJ")  # JWT header prefix

    def test_jwt_token_verification_valid(self):
        """Verify valid JWT token passes verification."""
        user_id = "user-123"
        token = create_access_token(user_id, timedelta(minutes=60))

        decoded = verify_token(token)
        assert decoded["sub"] == user_id
        assert "exp" in decoded

    def test_jwt_token_verification_expired(self):
        """Verify expired JWT token fails verification."""
        user_id = "user-123"
        # Create token with 1-second expiry
        token = create_access_token(user_id, timedelta(seconds=1))

        import time
        time.sleep(2)  # Wait for expiry

        with pytest.raises(TokenExpiredException):
            verify_token(token)

    def test_jwt_token_verification_invalid(self):
        """Verify invalid JWT token fails verification."""
        with pytest.raises(TokenInvalidException):
            verify_token("invalid.token.here")
```

### Unit Test Organization

```
tests/
├── unit/
│   ├── test_merkle_engine.py
│   ├── test_reserves.py
│   ├── test_auth.py
│   ├── test_validators.py
│   ├── blockchain/
│   │   ├── test_bitcoin_adapter.py
│   │   ├── test_ethereum_adapter.py
│   │   ├── test_solana_adapter.py
│   │   └── test_multi_chain_adapter.py
│   ├── defi/
│   │   ├── test_aave_verifier.py
│   │   └── test_uniswap_verifier.py
│   └── services/
│       ├── test_email_service.py
│       └── test_notification_service.py
├── integration/
│   ├── test_auth_endpoints.py
│   ├── test_engagement_api.py
│   ├── test_merkle_api.py
│   ├── test_report_generation.py
│   └── test_blockchain_verification.py
└── e2e/
    ├── test_vasp_onboarding.py
    ├── test_engagement_lifecycle.py
    └── test_customer_verification.py
```

---

## Integration Testing

### Testing Database Operations

```python
# tests/integration/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models import *

@pytest.fixture(scope="function")
def db_session():
    """Create test database session."""
    # Use in-memory SQLite for speed
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()

# tests/integration/test_engagement_db.py
@pytest.mark.integration
class TestEngagementDatabase:
    def test_create_engagement(self, db_session):
        """Test engagement creation."""
        tenant = Tenant(
            id="tenant-1",
            name="Test VASP",
            type="VASP",
            status="ACTIVE"
        )
        db_session.add(tenant)

        engagement = Engagement(
            id="eng-1",
            name="Q1 Audit",
            client_tenant_id="tenant-1",
            auditor_tenant_id="auditor-1",
            reporting_date=datetime(2024, 1, 15),
            status="PLANNING"
        )
        db_session.add(engagement)
        db_session.commit()

        # Retrieve and verify
        retrieved = db_session.query(Engagement).filter_by(id="eng-1").first()
        assert retrieved is not None
        assert retrieved.name == "Q1 Audit"
        assert retrieved.status == "PLANNING"

    def test_engagement_asset_relationship(self, db_session):
        """Test engagement-to-asset relationship."""
        engagement = Engagement(...)
        db_session.add(engagement)
        db_session.flush()

        asset = EngagementAsset(
            engagement_id=engagement.id,
            asset_symbol="BTC",
            asset_name="Bitcoin"
        )
        db_session.add(asset)
        db_session.commit()

        # Verify relationship
        retrieved = db_session.query(Engagement).filter_by(id=engagement.id).first()
        assert len(retrieved.assets) == 1
        assert retrieved.assets[0].asset_symbol == "BTC"
```

### Testing API Endpoints

```python
# tests/integration/test_auth_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.integration
class TestAuthEndpoints:
    def test_login_success(self, client, db_session):
        """Test successful login."""
        # Create user
        user = create_test_user(db_session, email="test@simplyfi.com")

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@simplyfi.com",
                "password": "correct_password"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        """Test login with wrong password."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@simplyfi.com",
                "password": "wrong_password"
            }
        )

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login for non-existent user."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@simplyfi.com",
                "password": "password"
            }
        )

        assert response.status_code == 401

    def test_mfa_required(self, client, db_session):
        """Test MFA requirement when enabled."""
        # Create user with MFA enabled
        user = create_test_user(db_session, mfa_enabled=True)

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": user.email,
                "password": "correct_password"
            }
        )

        # Should require MFA
        assert response.status_code == 200
        data = response.json()
        assert data.get("mfa_required") == True
        assert "temp_token" in data

    def test_register_user_success(self, client):
        """Test user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@simplyfi.com",
                "full_name": "New User",
                "password": "StrongPassword123!",
                "tenant_id": "tenant-1"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@simplyfi.com"

    def test_register_duplicate_email(self, client, db_session):
        """Test registration with duplicate email."""
        create_test_user(db_session, email="existing@simplyfi.com")

        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "existing@simplyfi.com",
                "full_name": "Another User",
                "password": "StrongPassword123!",
                "tenant_id": "tenant-1"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
```

### Testing Celery Tasks

```python
# tests/integration/test_celery_tasks.py
import pytest
from celery import Celery
from app.tasks.celery_app import celery_app
from app.tasks.reconciliation_tasks import daily_reconciliation_task

@pytest.fixture
def celery_config():
    return {
        "broker_url": "memory://",
        "result_backend": "cache+memory://"
    }

@pytest.mark.integration
class TestCeleryTasks:
    def test_daily_reconciliation_task(self, db_session):
        """Test daily reconciliation task."""
        # Setup engagement with balances
        engagement = create_test_engagement(db_session)
        create_test_asset_balance(db_session, engagement, "BTC", Decimal("100"))

        # Execute task
        result = daily_reconciliation_task.apply_async(
            args=[str(engagement.id)],
            task_id="test-task-1"
        ).get(timeout=5)

        # Verify reconciliation record created
        from app.models.asset import ReconciliationRecord
        records = db_session.query(ReconciliationRecord).filter_by(
            engagement_id=engagement.id
        ).all()
        assert len(records) > 0
        assert records[0].status in ["RECONCILED", "VARIANCE_FLAGGED"]

    def test_task_retry_on_failure(self):
        """Test task retry logic."""
        # Mock API to fail first time
        with patch("blockchain_api") as mock_api:
            mock_api.get_balance.side_effect = [
                Exception("API timeout"),  # First call fails
                {"balance": 100}  # Second call succeeds
            ]

            result = some_task.apply_async().get()
            assert result["status"] == "success"
            assert mock_api.get_balance.call_count == 2  # Retried
```

---

## End-to-End Testing

### Critical User Journey Tests

```python
# tests/e2e/test_vasp_onboarding.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.e2e
class TestVASPOnboarding:
    """Test complete VASP onboarding workflow."""

    def test_vasp_onboarding_flow(self, client, db_session):
        """Test end-to-end VASP onboarding: signup -> profile -> first audit."""

        # Step 1: SuperAdmin creates VASP tenant
        response = client.post(
            "/api/v1/admin/tenants",
            json={
                "name": "New Exchange",
                "type": "VASP",
                "vara_license_number": "VARA-123-2024"
            },
            headers={"Authorization": f"Bearer {superadmin_token}"}
        )
        assert response.status_code == 201
        vasp_tenant_id = response.json()["id"]

        # Step 2: VASP Admin registers account
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@exchange.com",
                "full_name": "Exchange Admin",
                "password": "StrongPassword123!",
                "tenant_id": vasp_tenant_id
            }
        )
        assert response.status_code == 201
        vasp_admin_user_id = response.json()["id"]

        # Get auth token
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@exchange.com", "password": "StrongPassword123!"}
        )
        assert response.status_code == 200
        vasp_token = response.json()["access_token"]

        # Step 3: VASP Admin adds wallet addresses
        response = client.post(
            "/api/v1/wallets",
            json={
                "address": "bc1qz3khxnyq05mtp2v6ujjmqwg87fv5k6n3wpuqhd",
                "blockchain": "Bitcoin",
                "custody_type": "SELF_CUSTODY",
                "wallet_type": "COLD"
            },
            headers={"Authorization": f"Bearer {vasp_token}"}
        )
        assert response.status_code == 201
        wallet_id = response.json()["id"]

        # Step 4: VASP Finance uploads liability data
        liability_data = """customer_id,BTC,ETH,USDC
cust_001,0.5,10,1000
cust_002,0.3,20,2000
cust_003,0.2,5,500"""

        response = client.post(
            "/api/v1/liabilities/upload",
            files={"file": ("liabilities.csv", liability_data)},
            headers={"Authorization": f"Bearer {vasp_token}"}
        )
        assert response.status_code == 200

        # Step 5: Lead Auditor creates engagement
        response = client.post(
            "/api/v1/engagements",
            json={
                "name": "Q1 2024 Audit",
                "client_tenant_id": vasp_tenant_id,
                "reporting_date": "2024-01-15T00:00:00Z",
                "assets": ["BTC", "ETH", "USDC"]
            },
            headers={"Authorization": f"Bearer {lead_auditor_token}"}
        )
        assert response.status_code == 201
        engagement_id = response.json()["id"]

        # Step 6: Verify engagement status
        response = client.get(
            f"/api/v1/engagements/{engagement_id}",
            headers={"Authorization": f"Bearer {vasp_token}"}
        )
        assert response.status_code == 200
        engagement = response.json()
        assert engagement["status"] == "PLANNING"
        assert len(engagement["assets"]) == 3

        # Onboarding complete!
        assert vasp_tenant_id
        assert engagement_id
        assert wallet_id
```

### Engagement Lifecycle E2E Test

```python
# tests/e2e/test_engagement_lifecycle.py
@pytest.mark.e2e
class TestEngagementLifecycle:
    """Test complete engagement: planning -> data collection -> verification -> reporting."""

    def test_full_engagement_cycle(self, client, db_session):
        """Test engagement from creation to report completion."""

        # Pre-setup: Create VASP tenant and auditor tenant
        vasp_tenant = create_test_tenant(db_session, type="VASP")
        auditor_tenant = create_test_tenant(db_session, type="AUDITOR")
        engagement = create_test_engagement(db_session, vasp_tenant, auditor_tenant)

        # Phase 1: Data Collection
        # Upload liability data
        response = client.post(
            "/api/v1/liabilities/upload",
            files={"file": ("liabilities.csv", test_liability_data)}
        )
        assert response.status_code == 200

        # Phase 2: Verification
        # Create wallet and initiate verification
        wallet = create_test_wallet(db_session, engagement, "Bitcoin", "bc1q...")
        response = client.post(
            "/api/v1/blockchain/verify-balance",
            json={
                "engagement_id": engagement.id,
                "wallet_id": wallet.id,
                "blockchain": "Bitcoin"
            }
        )
        assert response.status_code == 200
        verification_result = response.json()
        assert verification_result["status"] == "VERIFIED"
        assert "balance" in verification_result

        # Phase 3: Merkle Tree Generation
        response = client.post(
            "/api/v1/merkle/generate-tree",
            json={"engagement_id": engagement.id}
        )
        assert response.status_code == 200
        merkle_response = response.json()
        assert "merkle_root" in merkle_response

        # Auditor approves Merkle root
        response = client.put(
            f"/api/v1/merkle/{merkle_response['tree_id']}/approve",
            json={"approved": True}
        )
        assert response.status_code == 200

        # Phase 4: Report Generation
        response = client.post(
            "/api/v1/reports/generate",
            json={
                "engagement_id": engagement.id,
                "template": "AGREED_UPON_PROCEDURES"
            }
        )
        assert response.status_code == 200
        report_response = response.json()
        assert report_response["status"] == "GENERATED"

        # Lead Auditor approves report
        response = client.put(
            f"/api/v1/reports/{report_response['id']}/approve",
            json={"approved": True}
        )
        assert response.status_code == 200

        # Verify engagement completed
        response = client.get(f"/api/v1/engagements/{engagement.id}")
        assert response.status_code == 200
        final_engagement = response.json()
        assert final_engagement["status"] == "COMPLETED"
```

### Customer Merkle Verification E2E Test

```python
# tests/e2e/test_customer_verification.py
@pytest.mark.e2e
class TestCustomerMerkleVerification:
    """Test customer portal merkle verification flow."""

    def test_customer_can_verify_merkle_proof(self, client, db_session):
        """Test customer verifying their balance in Merkle tree."""

        # Setup: Create engagement with Merkle tree
        engagement = create_test_engagement(db_session)
        merkle_tree = create_test_merkle_tree(db_session, engagement)

        # Customer gets verification link from email (simulated)
        verification_id = merkle_tree.customer_proofs[0]["verification_id"]

        # Customer clicks verification link and enters verification ID
        response = client.post(
            "/api/v1/merkle/verify",
            json={"verification_id": verification_id}
        )
        assert response.status_code == 200
        proof_response = response.json()

        # Verify response contains customer balance and Merkle proof
        assert "customer_balance" in proof_response
        assert "merkle_proof" in proof_response
        assert "merkle_root" in proof_response

        # Customer can verify the proof is valid
        response = client.post(
            "/api/v1/merkle/verify-proof",
            json={
                "leaf_hash": proof_response["leaf_hash"],
                "proof_path": proof_response["merkle_proof"],
                "root_hash": proof_response["merkle_root"]
            }
        )
        assert response.status_code == 200
        verify_response = response.json()
        assert verify_response["valid"] == True

        # Customer can access report summary
        response = client.get(
            f"/api/v1/reports/{engagement.report_id}/customer-summary"
        )
        assert response.status_code == 200
        summary = response.json()
        assert summary["reserve_ratio"] > 0.95  # >= VARA minimum
```

---

## Performance Testing

### Load Testing with Locust

```python
# tests/performance/locustfile.py
from locust import HttpUser, task, constant_throughput
import random

class AuditorUser(HttpUser):
    """Simulate auditor performing verification."""
    wait_time = constant_throughput(1)  # 1 request/second

    def on_start(self):
        """Login before starting."""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "auditor@simplyfi.com", "password": "password"}
        )
        self.token = response.json()["access_token"]

    @task(70)
    def verify_balance(self):
        """70% of traffic - balance verification."""
        engagement_id = random.choice(["eng-001", "eng-002", "eng-003"])
        wallet_id = random.choice([f"wallet-{i}" for i in range(1, 11)])

        self.client.post(
            "/api/v1/blockchain/verify-balance",
            json={
                "engagement_id": engagement_id,
                "wallet_id": wallet_id,
                "blockchain": "Ethereum"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(20)
    def get_verification_status(self):
        """20% of traffic - check status."""
        engagement_id = random.choice(["eng-001", "eng-002", "eng-003"])
        self.client.get(
            f"/api/v1/engagements/{engagement_id}/verification-status",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(10)
    def generate_report(self):
        """10% of traffic - generate report."""
        engagement_id = random.choice(["eng-001", "eng-002", "eng-003"])
        self.client.post(
            "/api/v1/reports/generate",
            json={"engagement_id": engagement_id},
            headers={"Authorization": f"Bearer {self.token}"}
        )

class VASPUser(HttpUser):
    """Simulate VASP finance team."""
    wait_time = constant_throughput(0.5)

    def on_start(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "finance@vasp.com", "password": "password"}
        )
        self.token = response.json()["access_token"]

    @task
    def view_engagement(self):
        engagement_id = random.choice(["eng-001", "eng-002", "eng-003"])
        self.client.get(
            f"/api/v1/engagements/{engagement_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

**Run Load Test**:
```bash
# Start load testing server
locust -f tests/performance/locustfile.py --host http://localhost:8000

# Navigate to http://localhost:8089
# Configure: 100 users, 2 users/second spawn rate
# Run for 10 minutes
# Monitor: Response time, throughput, errors
```

**Performance Targets**:

| Endpoint | P50 | P95 | P99 | Error Rate |
|----------|-----|-----|-----|-----------|
| GET /health | 50ms | 100ms | 150ms | 0% |
| POST /auth/login | 200ms | 500ms | 1000ms | 0.1% |
| POST /blockchain/verify-balance | 5s | 15s | 30s | 1% |
| POST /reports/generate | 30s | 60s | 120s | 2% |
| GET /api/v1/engagements | 100ms | 200ms | 500ms | 0.1% |

### Stress Testing

```bash
# Gradually increase load until system breaks
# Start: 10 concurrent users
# Increase: 10 users every minute
# Stop when: Error rate > 5% or response time > 30s

locust -f tests/performance/locustfile.py \
  --host http://localhost:8000 \
  --spawn-rate 10/m \
  --run-time 30m \
  --csv=stress_test_results
```

---

## Test Data Strategy

### Fixtures Approach

```python
# tests/conftest.py
import pytest
from app.models import Tenant, User, Engagement
from app.core.security import hash_password

@pytest.fixture(scope="session")
def test_tenants():
    """Create test tenant data."""
    return {
        "auditor": Tenant(
            id="auditor-1",
            name="SimplyFI Auditors",
            type="AUDITOR"
        ),
        "vasp_1": Tenant(
            id="vasp-1",
            name="Exchange A",
            type="VASP",
            vara_license_number="VARA-100-2024"
        ),
        "vasp_2": Tenant(
            id="vasp-2",
            name="Exchange B",
            type="VASP",
            vara_license_number="VARA-101-2024"
        )
    }

@pytest.fixture(scope="function")
def test_users(test_tenants):
    """Create test user data."""
    return {
        "auditor": User(
            id="user-auditor-1",
            email="auditor@simplyfi.com",
            full_name="Lead Auditor",
            hashed_password=hash_password("auditor_password"),
            tenant_id=test_tenants["auditor"].id,
            is_superadmin=False
        ),
        "vasp_admin": User(
            id="user-vasp-1",
            email="admin@exchange.com",
            full_name="VASP Admin",
            hashed_password=hash_password("vasp_password"),
            tenant_id=test_tenants["vasp_1"].id
        )
    }

@pytest.fixture(scope="function")
def db_session(test_tenants, test_users):
    """Populate test database with fixtures."""
    session = TestSessionLocal()

    # Add tenants
    for tenant in test_tenants.values():
        session.add(tenant)

    # Add users
    for user in test_users.values():
        session.add(user)

    session.commit()
    yield session
    session.close()
```

### Factory Pattern

```python
# tests/factories.py
import factory
from app.models import Engagement, EngagementAsset
from decimal import Decimal
from datetime import datetime

class TenantFactory(factory.Factory):
    class Meta:
        model = Tenant

    id = factory.Faker('uuid4')
    name = factory.Faker('company')
    type = "VASP"
    status = "ACTIVE"

class EngagementFactory(factory.Factory):
    class Meta:
        model = Engagement

    id = factory.Faker('uuid4')
    name = factory.Faker('sentence')
    client_tenant_id = factory.SubFactory(TenantFactory)
    auditor_tenant_id = factory.LazyAttribute(lambda _: TenantFactory().id)
    reporting_date = datetime(2024, 1, 15)
    status = "PLANNING"

class AssetBalanceFactory(factory.Factory):
    class Meta:
        model = AssetBalance

    id = factory.Faker('uuid4')
    engagement_id = factory.SelfAttribute('..engagement.id')
    reported_balance = Decimal("100.00")
    verified_balance = Decimal("100.50")

# Usage in tests
def test_with_factories():
    engagement = EngagementFactory()
    assets = [AssetBalanceFactory(engagement_id=engagement.id) for _ in range(5)]
```

### Mocking External Services

```python
# tests/unit/test_blockchain_adapter.py
from unittest.mock import patch, MagicMock

@pytest.mark.unit
def test_bitcoin_balance_verification_mocked():
    """Test balance verification with mocked Blockstream API."""

    mock_response = {
        "chain_stats": {
            "funded_txo_sum": 500000000,  # 5 BTC in satoshis
            "spent_txo_sum": 250000000
        }
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        adapter = BitcoinAdapter()
        balance = adapter.verify_balance("bc1qz3khxnyq05...")

        assert balance.balance == Decimal("2.5")  # (500M - 250M) / 1e8
        assert balance.verified_at is not None

        # Verify API was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "blockstream" in call_args[0][0]
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test & Coverage

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio pytest-mock

    - name: Run unit tests
      run: pytest tests/unit -v --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0

    - name: Run integration tests
      run: pytest tests/integration -v
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

    - name: Check coverage thresholds
      run: |
        coverage report --fail-under=85
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit
        language: system
        pass_filenames: false
        always_run: true

      - id: coverage
        name: coverage
        entry: coverage report --fail-under=85
        language: system
        pass_filenames: false
        always_run: true
```

**Install pre-commit hooks**:
```bash
pip install pre-commit
pre-commit install
```

---

## Manual Testing

### Test Plans

**VASP Onboarding Test Plan**:
```markdown
## Test Case: VASP Onboarding
**Status**: In Progress
**Date**: 2024-02-15
**Tester**: QA Engineer

### Pre-conditions
- Fresh test environment
- Test accounts available
- Sample liability data prepared

### Test Steps
1. SuperAdmin logs in to admin dashboard
   - [ ] Login successful
   - [ ] See admin panel

2. Create new VASP tenant
   - [ ] Click "Add VASP"
   - [ ] Fill form: name="Test Exchange", license="VARA-999-2024"
   - [ ] Submit
   - [ ] Verify VASP created in list

3. VASP Admin registers account
   - [ ] Receive email with registration link
   - [ ] Click link
   - [ ] Fill registration form
   - [ ] Set strong password
   - [ ] Accept terms
   - [ ] Verify email confirmation sent

4. Log in as VASP Admin
   - [ ] Login successful
   - [ ] See VASP dashboard
   - [ ] Can access wallet configuration

5. Add wallet address
   - [ ] Click "Add Wallet"
   - [ ] Enter Bitcoin address
   - [ ] Select custody type: "Self Custody"
   - [ ] Submit
   - [ ] Verify wallet appears in list

6. Upload liability data
   - [ ] Click "Upload Liabilities"
   - [ ] Select CSV file with sample data
   - [ ] Verify preview shows correct rows
   - [ ] Submit
   - [ ] Verify success message

### Expected Results
- VASP created successfully
- Admin account created
- Wallet configured
- Liability data imported

### Actual Results
[To be filled during test execution]

### Issues Found
- [ ] None
- [ ] List any issues...
```

---

## Summary

This testing strategy provides:
- Comprehensive test pyramid approach
- Unit, integration, and E2E test examples
- Performance testing procedures with load tests
- Test data fixtures and factory pattern
- CI/CD integration with GitHub Actions
- Coverage goals and metrics per module
- Manual testing checklists and plans

Teams can use this document to:
- Write testable code with clear interfaces
- Achieve >85% code coverage consistently
- Catch bugs early in development
- Maintain performance baselines
- Automate testing in CI/CD pipeline
- Plan manual testing for complex workflows
- Onboard new QA engineers with test procedures

