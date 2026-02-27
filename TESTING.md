# Testing Guide for SimplyFI PoR Platform

## Overview

This document describes the comprehensive test suite for the SimplyFI Proof of Reserves (PoR) crypto audit platform. The suite includes 90+ tests covering unit, integration, and end-to-end scenarios.

## Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py                 # Pytest fixtures and configuration
├── factories.py                # Test data factories
├── mocks/
│   ├── __init__.py
│   └── blockchain_mocks.py    # Mock blockchain API responses
├── unit/                       # Unit tests (50+ tests)
│   ├── __init__.py
│   ├── test_merkle_engine.py
│   ├── test_security.py
│   ├── test_validators.py
│   ├── test_reserve_calculations.py
│   ├── test_anomaly_detector.py
│   └── test_compliance_engine.py
├── integration/                # Integration tests (30+ tests)
│   ├── __init__.py
│   ├── test_auth_api.py
│   ├── test_engagement_api.py
│   ├── test_merkle_api.py
│   ├── test_reserves_api.py
│   └── test_onboarding_api.py
└── run_tests.sh               # Test runner script

tests/e2e/                      # End-to-end tests (10+ tests)
├── __init__.py
├── conftest.py               # E2E fixtures
├── test_full_audit_flow.py
├── test_customer_verification.py
└── test_rbac_enforcement.py

pytest.ini                     # Pytest configuration
requirements-test.txt          # Testing dependencies
```

## Test Categories

### Unit Tests (50+ tests)

Unit tests verify individual components in isolation without external dependencies.

#### 1. **Merkle Tree Engine Tests** (`test_merkle_engine.py`)
- Tree building with single/multiple leaves
- Leaf hashing (SHA256, Keccak256)
- Proof generation and verification
- Batch operations
- Large-scale trees (1000 leaves)
- Serialization/deserialization

#### 2. **Security Tests** (`test_security.py`)
- Password hashing and verification
- JWT token creation and validation
- Token expiration handling
- MFA setup and verification
- Permission extraction

#### 3. **Validator Tests** (`test_validators.py`)
- Ethereum address validation
- Bitcoin address validation (P2PKH, Segwit)
- Solana address validation
- XRP address validation
- Crypto amount validation
- Blockchain name validation
- Custody/wallet type validation

#### 4. **Reserve Calculation Tests** (`test_reserve_calculations.py`)
- Reserve ratio calculations (100%, >100%, <100%)
- Multiple asset aggregation
- DeFi position handling
- Variance calculations
- VARA compliance checks
- Reserve segregation

#### 5. **Anomaly Detection Tests** (`test_anomaly_detector.py`)
- Negative balance detection
- Duplicate user ID detection
- Outlier balance detection (Z-score)
- Sudden balance change detection
- Anomaly severity scoring
- Reconciliation anomalies

#### 6. **Compliance Engine Tests** (`test_compliance_engine.py`)
- Reserve requirement verification
- Asset segregation compliance
- Daily reconciliation checks
- Quarterly reporting compliance
- Compliance score calculation
- Remediation step generation

### Integration Tests (30+ tests)

Integration tests verify interactions between multiple components.

#### 1. **Authentication API Tests** (`test_auth_api.py`)
- User registration
- Login flow
- Token refresh
- Protected endpoints
- Role-based access control
- Tenant isolation

#### 2. **Engagement API Tests** (`test_engagement_api.py`)
- CRUD operations
- Pagination
- Status updates
- Asset management
- Timeline tracking

#### 3. **Merkle API Tests** (`test_merkle_api.py`)
- Tree generation
- Root hash retrieval
- Customer proof verification
- Batch proof generation
- Serialization

#### 4. **Reserves API Tests** (`test_reserves_api.py`)
- Reserve ratio calculation
- Segregation verification
- Reconciliation data
- DeFi integration

#### 5. **Onboarding API Tests** (`test_onboarding_api.py`)
- VASP registration
- Asset import
- Wallet import (CSV)
- Liability import
- Data validation
- Status tracking

### End-to-End Tests (10+ tests)

E2E tests verify complete user workflows.

#### 1. **Full Audit Flow** (`test_full_audit_flow.py`)
- SuperAdmin creates VASP tenant
- VASP onboarding
- Engagement creation
- On-chain verification
- Merkle tree generation
- Reserve calculation
- Report generation
- Customer verification
- VARA compliance check

#### 2. **Customer Verification** (`test_customer_verification.py`)
- Merkle proof verification
- Balance viewing
- Trust indicators
- Offline verification

#### 3. **RBAC Enforcement** (`test_rbac_enforcement.py`)
- Role-based access control
- Tenant isolation
- Custom permissions
- Audit logging

## Running Tests

### Setup

```bash
# Install testing dependencies
pip install -r backend/requirements-test.txt

# Navigate to backend directory
cd backend
```

### Run All Tests

```bash
# Run complete test suite with coverage
bash tests/run_tests.sh all

# Or use pytest directly
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Specific Test Categories

```bash
# Unit tests only
bash tests/run_tests.sh unit

# Integration tests only
bash tests/run_tests.sh integration

# E2E tests only
bash tests/run_tests.sh e2e
```

### Run Specific Tests

```bash
# Run tests matching pattern
bash tests/run_tests.sh match merkle

# Run specific test file
pytest tests/unit/test_merkle_engine.py -v

# Run specific test class
pytest tests/unit/test_merkle_engine.py::TestMerkleTree -v

# Run specific test
pytest tests/unit/test_merkle_engine.py::TestMerkleTree::test_build_tree_single_leaf -v
```

### Code Quality

```bash
# Run linting
bash tests/run_tests.sh lint

# Generate coverage report
bash tests/run_tests.sh coverage
```

## Test Data Generation

The suite uses factories for consistent test data generation:

```python
from tests.factories import (
    UserFactory,
    TenantFactory,
    EngagementFactory,
    AssetFactory,
    WalletFactory,
    CustomerLiabilityFactory,
    TokenFactory,
)

# Create test user
user = UserFactory.build(email="test@example.com")

# Create admin user
admin = UserFactory.admin_build()

# Create token
token = TokenFactory.build(user_id="user-123")

# Create engagement
engagement = EngagementFactory.in_progress_build()
```

## Fixtures

Key pytest fixtures available:

```python
def test_with_database(db):
    """Database session fixture."""
    pass

def test_with_client(client):
    """FastAPI TestClient fixture."""
    response = client.get("/health")

def test_with_auth(auth_headers):
    """Authorization headers fixture."""
    client.get("/api/v1/engagements", headers=auth_headers)

def test_with_mocks(mock_ethereum_adapter, mock_bitcoin_adapter):
    """Mock blockchain adapters."""
    pass
```

## Mock Responses

Mock blockchain API responses available in `tests/mocks/blockchain_mocks.py`:

```python
from tests.mocks.blockchain_mocks import (
    EthereumMockResponses,
    BitcoinMockResponses,
    SolanaMockResponses,
    DeFiMockResponses,
    CustodianMockResponses,
)

# Get mock balance response
ethereum_response = EthereumMockResponses.balance_response(
    address="0x742d35Cc6634C0532925a3b844Bc314e5505b748",
    balance=1000.5
)
```

## Coverage Report

After running tests, view coverage:

```bash
# Open HTML coverage report
open htmlcov/index.html

# View coverage in terminal
cat .coverage
```

### Coverage Goals

- **Unit Tests**: 90%+ coverage
- **Integration Tests**: 80%+ coverage
- **Overall**: 85%+ coverage minimum

## Test Markers

Tests are organized with markers for selective execution:

```bash
# Run only async tests
pytest -m async

# Run only slow tests
pytest -m slow

# Run everything except slow tests
pytest -m "not slow"
```

## Best Practices

### 1. Test Naming
- Descriptive names: `test_verify_proof_valid_leaf`
- Clear what's being tested

### 2. Test Organization
- One concept per test
- Use helper methods for setup
- Clean up after tests

### 3. Assertions
- Clear assertion messages
- Use appropriate assertion types
- Test both success and failure paths

### 4. Mocking
- Mock external dependencies
- Keep mocks realistic
- Document mock behavior

### 5. Fixtures
- Reusable fixtures for common setup
- Session/module/function scope
- Clear fixture names

## Continuous Integration

Tests are integrated with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run unit tests
  run: pytest tests/unit --cov=app --cov-fail-under=90

- name: Run integration tests
  run: pytest tests/integration --tb=short

- name: Run E2E tests
  run: pytest tests/e2e -v
```

## Troubleshooting

### Common Issues

1. **Async test failures**
   ```bash
   # Ensure pytest-asyncio is installed
   pip install pytest-asyncio

   # Use pytest mark
   @pytest.mark.asyncio
   async def test_async_function():
       pass
   ```

2. **Database connection errors**
   ```bash
   # Tests use in-memory SQLite by default
   # No database setup needed
   ```

3. **Missing fixtures**
   ```bash
   # Ensure conftest.py is in test directory
   # Pytest automatically discovers fixtures
   ```

4. **Timeout issues**
   ```bash
   # Increase timeout in pytest.ini
   # Or use @pytest.mark.timeout(60)
   ```

## Contributing Tests

When adding new features:

1. Write unit tests first (TDD)
2. Add integration tests for component interactions
3. Add E2E tests for user workflows
4. Maintain 85%+ coverage
5. Document complex test scenarios

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-the-session-in-tests)
- [AsyncIO Testing](https://docs.python.org/3/library/asyncio-dev.html#debug-mode)

## Support

For issues or questions about tests:

1. Check existing test examples
2. Review documentation in test files
3. Consult conftest.py for available fixtures
4. Ask in team documentation or issues
