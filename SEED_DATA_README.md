# SimplyFI PoR Platform - Seed Data and API Specification

## Overview

This directory contains complete production-grade API specifications, database schema documentation, and seed data for the SimplyFI Proof of Reserves (PoR) crypto audit platform.

## Files Created

### 1. API Specification
- **File:** `/api/openapi.yaml`
- **Lines:** 4,260
- **Coverage:** 
  - 50+ endpoints across 12 endpoint groups
  - Complete OpenAPI 3.1 specification
  - All request/response schemas defined
  - Authentication and security requirements
  - Error handling for all status codes

**Endpoint Groups:**
- Auth (6 endpoints) - Login, register, MFA, refresh tokens
- Users (7 endpoints) - User management and CRUD
- Tenants (6 endpoints) - Organization management
- Engagements (9 endpoints) - Audit engagement lifecycle
- Assets (6 endpoints) - Crypto asset management
- Reserves (5 endpoints) - Reserve verification and ratios
- Merkle (4 endpoints) - Merkle tree generation/verification
- Blockchain (5 endpoints) - On-chain verification
- Reports (5 endpoints) - Report generation and download
- AI (5 endpoints) - AI-powered analysis and insights
- Admin (4 endpoints) - Admin dashboard and role management
- Onboarding (5 endpoints) - VASP onboarding workflows

### 2. Database Schema
- **File:** `/db/schema/erd.md`
- **Lines:** 488
- **Contains:**
  - Entity-Relationship Diagram (Mermaid format)
  - 16 table definitions with all columns and constraints
  - Data types and validation rules
  - Indexing strategy
  - Business rules and constraints
  - Security considerations

**Tables:**
- tenants, users, roles, permissions, user_roles, role_permissions
- crypto_assets, engagements, wallet_addresses, customer_liabilities
- merkle_trees, merkle_proofs, reconciliation_records
- defi_positions, audit_reports, audit_logs

### 3. Database Seed Data

#### SQL Seed Files (10 files)
```
01_tenants.sql              - 6 tenants (2 auditors, 3 VASPs, 1 regulator)
02_users.sql                - 80 users (5 admins, 10 auditors, 10 VASP, 50 customers, 5 regulators)
03_roles_permissions.sql    - 7 system roles with 40+ permissions
04_crypto_assets.sql        - 130 cryptocurrencies (Tier 1, 2, 3)
05_engagements.sql          - 5 engagements at different stages
06_wallets_balances.sql     - 40+ wallets with realistic balances
07_customer_liabilities.sql - 250+ customer liability records
08_merkle_trees.sql         - Merkle trees with 10 sample proofs
09_reconciliation.sql       - 30 days of reconciliation records
10_transactions_audit.sql   - 20 audit log entries
```

#### JSON Fixtures (2 files)
```
fixtures/users.json         - 17 sample users for API testing
fixtures/engagements.json   - 5 demo engagements with details
```

#### Seeding Script
```
seed.sh                      - Bash script to execute all SQL files
                              - Validates PostgreSQL connectivity
                              - Executes files in proper order
                              - Validates row counts
                              - Prints summary report
```

## Data Summary

### Users (80 total)
- 5 System Administrators
- 10 Auditors (Big4 and Crypto Compliance)
- 10 VASP Compliance/Treasury staff
- 50 Customer representatives
- 5 Regulatory supervisors

### Tenants (6 total)
- Kraken (VASP) - $15B AUM
- Coinbase (VASP) - $18B AUM
- Celsius Network (VASP) - $8B AUM
- Big4 Auditors LLP (Auditor)
- Crypto Compliance Partners (Auditor)
- Financial Conduct Authority (Regulator)

### Crypto Assets (130 total)
- **Tier 1 (10):** BTC, ETH, USDT, USDC, BNB, SOL, XRP, ADA, DOGE, DOT
- **Tier 2 (50):** AVAX, MATIC, LINK, UNI, AAVE, SUSHI, CRV, MKR, YFI, LIDO, etc.
- **Tier 3 (70):** TRX, VET, ALGO, APE, ARB, BAT, BCH, FIL, FLOW, etc.

All assets include:
- Symbol and name
- Supported blockchains
- Contract addresses (where applicable)
- Decimal places
- Logo URLs

### Engagements (5 total)

**1. Kraken - COMPLETED**
- Status: Completed
- Assets: 5 (BTC, ETH, USDT, USDC, SOL)
- Wallets: 32
- Customers: 4,250
- Reserve Ratio: 102.3%
- Completed: 2024-01-31

**2. Coinbase - REPORTING**
- Status: Reporting
- Assets: 5 (BTC, ETH, USDT, USDC, BNB)
- Wallets: 45
- Customers: 6,700
- Reserve Ratio: 103.1%

**3. Celsius - VERIFICATION**
- Status: Verification
- Assets: 4 (BTC, ETH, DAI, USDC)
- Wallets: 28
- Customers: 1,800
- Reserve Ratio: 101.8%

**4. Kraken Q2 - DATA COLLECTION**
- Status: Data Collection
- Assets: 5 (BTC, ETH, USDT, XRP, ADA)
- Wallets: 62
- Customers: 8,500
- Reserve Ratio: TBD

**5. Coinbase Special - PLANNING**
- Status: Planning
- Assets: 4 (BTC, ETH, SOL, MATIC)
- Wallets: 38
- Customers: 3,200
- Reserve Ratio: TBD

### Wallet Data
- 40+ sample wallets across multiple blockchains
- Realistic balances (from 0.0001 to millions)
- Mix of cold storage, hot wallets, custody accounts
- Some balances with variance (under-reserved scenarios)

### Customer Liabilities
- 250+ customer liability records
- Mix of account types: spot, margin, earning, staking
- Realistic balances and USD values
- Some marked as unverified
- Special cases: zero balances, very small amounts

### Merkle Trees
- 1 Merkle tree for completed engagement
- 10 sample proofs for customer verification
- Real-looking hash values (SHA256 format)
- Proper proof arrays for tree reconstruction

### Reconciliation Data
- 30 days of daily reconciliation records
- Progressive reserve ratio changes
- Realistic USD values for liabilities and reserves
- Tracks compliance status over time

### Audit Logs
- 20 sample audit entries covering:
  - User login and authentication
  - Engagement creation and status updates
  - Asset verification
  - Merkle tree generation
  - Report generation
  - User role assignments
  - Tenant settings updates
  - Data imports and exports
  - AI analysis execution
  - Compliance checks

## Usage

### Running the Seed Script

```bash
cd /path/to/db/seed

# Set environment variables (optional)
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=simplyfi_por
export DB_USER=postgres
export DB_PASSWORD=postgres

# Execute seeding
./seed.sh
```

The script will:
1. Wait for PostgreSQL to be ready
2. Execute all SQL files in order
3. Validate row counts for each table
4. Print a summary report

### Manual SQL Execution

```bash
# Connect to database
psql -h localhost -p 5432 -U postgres -d simplyfi_por

# Execute individual seed files
\i db/seed/01_tenants.sql
\i db/seed/02_users.sql
# ... continue with other files
```

### Docker Compose Integration

Add to your docker-compose.yml:

```yaml
db:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: simplyfi_por
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
  ports:
    - "5432:5432"
  volumes:
    - ./db/seed:/docker-entrypoint-initdb.d
```

## API Specification Usage

### Generating Client SDKs

```bash
# OpenAPI Generator (generate Python client)
openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g python \
  -o ./generated-python-client

# SwaggerHub UI
# Open: https://editor.swagger.io/
# Import: api/openapi.yaml
```

### API Documentation

```bash
# Generate Redoc documentation
docker run -p 8080:8080 \
  -e SPEC_URL=api/openapi.yaml \
  redocly/redoc

# Generate Swagger UI
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/app/openapi.yaml \
  -v $(pwd)/api:/app \
  swaggerapi/swagger-ui
```

## Data Dictionary

### Key Fields

**reserve_ratio**
- Percentage: (Total Reserves / Total Liabilities) × 100
- Compliant: ≥ 100%
- Warning: 95-100%
- Critical: < 95%

**variance**
- Percentage difference: (on_chain_balance - reported_balance) / reported_balance
- Positive: On-chain balance greater than reported
- Negative: On-chain balance less than reported (red flag)

**asset_type**
- Tier 1: Major cryptocurrencies (BTC, ETH, stablecoins)
- Tier 2: Significant altcoins
- Tier 3: Other supported assets

**engagement_status**
- planning: Initial setup phase
- data_collection: Gathering wallet/liability data
- verification: Verifying balances and creating proofs
- reporting: Generating audit reports
- completed: Audit finalized

## Validation Rules

All seed data adheres to:
- ✓ Valid UUIDs (v4 format)
- ✓ Realistic financial values (decimal, not float)
- ✓ Proper JSON encoding
- ✓ Valid cryptographic addresses
- ✓ Consistent date ranges
- ✓ Foreign key relationships
- ✓ Business logic constraints

## Performance Notes

- Total inserts: ~1,200 records across 16 tables
- Execution time: ~5-10 seconds on modern hardware
- Indexes created automatically for optimal query performance
- Ready for production use after schema migration

## Security Notes

1. **Passwords** - All user password hashes use bcrypt (not real passwords)
2. **API Keys** - Not included in seed data (configure separately)
3. **Private Keys** - Never stored in database
4. **Audit Trail** - All operations logged with timestamps and user IDs
5. **Multi-tenancy** - Full tenant isolation enforced

## Next Steps

1. **Schema Setup** - Run database migrations to create tables
2. **Seed Database** - Execute `./seed.sh` to populate data
3. **Generate Documentation** - Use OpenAPI spec to create docs
4. **Configure API** - Set up authentication and API keys
5. **Test Endpoints** - Use provided JSON fixtures for testing

## Support

For questions about:
- **API Specification** - See `/api/openapi.yaml`
- **Database Schema** - See `/db/schema/erd.md`
- **Seed Data Details** - Review individual SQL files
- **Execution Issues** - Check `seed.sh` and PostgreSQL logs

---

**Created:** 2024-02-27
**Version:** 1.0.0
**Status:** Production-Ready
