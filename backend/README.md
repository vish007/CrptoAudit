# SimplyFI Proof of Reserves Platform - Backend

Production-grade FastAPI backend for a multi-tenant SaaS Proof of Reserves (PoR) auditing platform serving VARA-regulated crypto audit firms.

## Overview

### Architecture
- **Framework**: FastAPI with async/await
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Storage**: AWS S3
- **Authentication**: JWT with MFA
- **Authorization**: Granular RBAC with custom role builder
- **Blockchain Integration**: 20+ blockchains, 153+ cryptocurrencies
- **AI Analytics**: LangChain with local LLM support
- **Merkle Proofs**: Privacy-preserving customer verification

### Core Components

#### Multi-Tenant Architecture
- Tenant isolation at database level
- Three tenant types: Auditors, VASPs, Regulators
- Role-based access control scoped to tenants
- Complete audit trails for compliance

#### Engagement Management
- Full audit engagement lifecycle (PLANNING → COMPLETED)
- Asset tier classification (Primary, Secondary, Tertiary)
- Timeline phase tracking
- Customer liability aggregation

#### Reserve Verification
- Multi-chain wallet verification
- Real-time balance verification from blockchain
- DeFi position tracking
- Reserve ratio calculations per VARA standards
- Customer fund segregation verification

#### Merkle Tree Privacy
- Generate merkle trees from customer liabilities
- Customer self-verification without revealing balances
- Proof path generation and validation
- Tree publication and archival

#### Blockchain Operations
- Support for 20+ blockchains
- Address validation (Ethereum, Bitcoin, Solana, XRP, etc.)
- Balance verification via RPC endpoints
- Instructed movement verification
- DeFi protocol integration

#### Reporting
- Proof of Reserves reports
- Audit assurance reports
- Management letters
- Customer-facing summaries
- PDF generation with ReportLab

#### AI Analytics
- Anomaly detection in balance data
- Automated report narrative generation
- VARA compliance checking
- Interactive audit assistant
- Risk scoring and recommendations

## Project Structure

```
backend/
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Settings management
│   │   ├── security.py           # JWT, passwords, permissions
│   │   └── database.py           # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # Users, Tenants, Roles, Permissions
│   │   ├── engagement.py         # Engagements, Assets, Timelines
│   │   ├── asset.py              # Crypto assets, Wallets, Balances
│   │   └── merkle.py             # Merkle trees and proofs
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py               # User request/response schemas
│   │   ├── engagement.py         # Engagement schemas
│   │   ├── asset.py              # Asset schemas
│   │   └── merkle.py             # Merkle schemas
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # Main router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py       # Authentication
│   │           ├── users.py      # User management
│   │           ├── tenants.py    # Tenant management
│   │           ├── engagements.py # Engagement CRUD
│   │           ├── assets.py     # Asset management
│   │           ├── reserves.py   # Reserve calculations
│   │           ├── merkle.py     # Merkle operations
│   │           ├── blockchain.py # Blockchain verification
│   │           ├── reports.py    # Report generation
│   │           ├── ai.py         # AI analytics
│   │           ├── admin.py      # Admin functions
│   │           └── onboarding.py # VASP onboarding
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── audit_log.py          # Audit logging
│   │   └── tenant.py             # Tenant isolation
│   └── utils/
│       ├── __init__.py
│       ├── pagination.py         # Pagination helpers
│       └── validators.py         # Address & data validators
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- AWS S3 bucket (for reports)

### Installation

1. **Clone repository and navigate to backend**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
# Run migrations (when using Alembic)
# alembic upgrade head

# Or initialize directly
python -c "import asyncio; from app.core.database import init_db; asyncio.run(init_db())"
```

6. **Run development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/api/docs for interactive API documentation.

## API Endpoints

### Authentication (`/auth`)
- `POST /login` - User login
- `POST /register` - Register new user
- `POST /refresh` - Refresh access token
- `POST /logout` - Logout
- `POST /mfa/setup` - Setup MFA
- `POST /mfa/verify` - Verify MFA token

### Users (`/users`)
- `GET /me` - Get current user
- `PUT /me` - Update profile
- `POST /me/change-password` - Change password
- `GET` - List users
- `GET /{id}` - Get user details
- `PUT /{id}` - Update user
- `DELETE /{id}` - Delete user
- `POST /{id}/roles` - Assign role

### Tenants (`/tenants`)
- `POST` - Create tenant
- `GET` - List tenants
- `GET /{id}` - Get tenant
- `PUT /{id}` - Update tenant
- `DELETE /{id}` - Delete tenant
- `GET /{id}/members` - List tenant members
- `PUT /{id}/settings` - Update settings

### Engagements (`/engagements`)
- `POST` - Create engagement
- `GET` - List engagements
- `GET /{id}` - Get engagement
- `PUT /{id}` - Update engagement
- `PUT /{id}/status` - Update status
- `DELETE /{id}` - Delete engagement
- `POST /{id}/assets` - Bulk add assets
- `GET /{id}/timeline` - Get timeline
- `POST /{id}/timeline` - Add timeline phase

### Assets (`/assets`)
- `POST` - Create asset
- `GET` - List assets
- `GET /{id}` - Get asset
- `GET /{id}/wallets` - List wallets
- `POST /{id}/wallets` - Add wallet
- `POST /{id}/verify-balance` - Verify balance
- `POST /bulk-import` - Bulk import assets

### Reserves (`/engagements/{id}/reserves`)
- `GET` - Get reserves summary
- `POST /calculate` - Calculate ratios
- `GET /ratio-table` - Get ratio table
- `POST /verify-segregation` - Verify segregation
- `GET /reconciliation` - Get reconciliation records

### Merkle Trees (`/engagements/{id}/merkle`)
- `POST /generate` - Generate tree
- `GET /root` - Get root hash
- `POST /verify` - Verify proof (public)
- `GET /stats` - Get statistics

### Blockchain (`/blockchain`)
- `GET /supported-chains` - Get supported chains
- `POST /verify-address` - Verify address
- `POST /verify-balance` - Verify balance
- `POST /verify-control` - Verify control
- `POST /defi/verify-position` - Verify DeFi position

### Reports (`/engagements/{id}/reports`)
- `POST /por` - Generate PoR report
- `POST /assurance` - Generate assurance report
- `POST /management-letter` - Generate management letter
- `POST /customer-summary` - Generate customer summary
- `GET /{id}/download` - Download report

### AI Analytics (`/ai`)
- `POST /analyze` - Analyze data for anomalies
- `POST /generate-narrative` - Generate report sections
- `POST /compliance-check` - Check VARA compliance
- `POST /chat` - Interactive assistant
- `GET /insights/{id}` - Get insights

### Admin (`/admin`)
- `GET /dashboard` - Dashboard stats
- `POST /roles` - Create role
- `GET /roles` - List roles
- `GET /roles/{id}` - Get role
- `PUT /roles/{id}` - Update role
- `PUT /roles/{id}/permissions` - Set permissions
- `DELETE /roles/{id}` - Delete role
- `POST /permissions` - Create permission
- `GET /permissions` - List permissions
- `GET /audit-log` - Get audit logs

### Onboarding (`/onboarding`)
- `POST /vasp` - Register VASP
- `POST /{id}/import-assets` - Import assets
- `POST /{id}/import-wallets` - Import wallets
- `POST /{id}/import-liabilities` - Import liabilities
- `GET /{id}/status` - Get status
- `POST /{id}/validate` - Validate data

## Authentication & Authorization

### JWT Tokens
- Access tokens: 60 minutes (configurable)
- Refresh tokens: 7 days (configurable)
- Algorithm: HS256

### Role-Based Access Control (RBAC)
- System roles (predefined)
- Custom roles (admin-created)
- Field-level restrictions
- Engagement-scoped roles

### MFA (Multi-Factor Authentication)
- TOTP-based (Google Authenticator, Authy)
- Per-user enablement
- Time-based one-time passwords

## Database Models

### User Management
- **User**: Platform users with authentication
- **Tenant**: Organizations (Auditors, VASPs, Regulators)
- **Role**: RBAC roles with permissions
- **Permission**: Granular resource-action permissions
- **UserRole**: Many-to-many user-role mapping
- **AuditLog**: Complete audit trail

### Engagements
- **Engagement**: Audit engagement between auditor and client
- **EngagementAsset**: Assets included in engagement
- **EngagementTimeline**: Phases and milestones

### Assets & Reserves
- **CryptoAsset**: Cryptocurrency definitions
- **WalletAddress**: Wallet addresses holding assets
- **AssetBalance**: Balance snapshots per wallet
- **CustomerLiability**: Customer account balances
- **ReserveRatio**: Calculated ratios per asset
- **DeFiPosition**: DeFi protocol positions
- **ReconciliationRecord**: Daily/periodic reconciliation

### Merkle Trees
- **MerkleTree**: Tree metadata and root hash
- **MerkleLeaf**: Individual customer liabilities
- **MerkleProof**: Proof paths for verification

## Configuration

All configuration via environment variables in `.env` file:

### Core Settings
- `DEBUG` - Development mode (False for production)
- `ENVIRONMENT` - Deployment environment
- `APP_NAME`, `APP_VERSION` - Application metadata

### Database
- `DATABASE_URL` - PostgreSQL connection string
- `DB_POOL_SIZE`, `DB_MAX_OVERFLOW` - Connection pooling
- `DB_POOL_RECYCLE` - Connection recycle timeout

### Security
- `JWT_SECRET` - Secret key for signing tokens (CHANGE IN PRODUCTION!)
- `JWT_ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token lifetime
- `PASSWORD_MIN_LENGTH` - Minimum password length
- `MFA_ENABLED_BY_DEFAULT` - Enable MFA for new users

### Blockchain
- `BLOCKCHAIN_API_KEYS_*` - API keys for blockchain services
- `BLOCKCHAIN_API_TIMEOUT` - RPC timeout (seconds)

### VARA Compliance
- `VARA_LICENSE_NUMBER` - Firm's VARA license
- `VARA_COMPLIANCE_LEVEL` - Compliance level (LEVEL_1, 2, or 3)
- `VARA_MIN_RESERVE_RATIO` - Minimum reserve ratio (0.95 = 95%)

## Development

### Code Style
- PEP 8 compliant
- Type hints throughout
- Docstrings for all functions
- Async/await patterns

### Testing
```bash
# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/api/test_auth.py

# Run in watch mode
pytest-watch
```

### Database Migrations
Using Alembic:
```bash
# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Deployment

### Docker
```bash
# Build image
docker build -t simplyfi-por-backend .

# Run container
docker run -p 8000:8000 --env-file .env simplyfi-por-backend
```

### Kubernetes
See `k8s/` directory for manifests

### Production Checklist
- [ ] Change `JWT_SECRET` to secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ENVIRONMENT=production`
- [ ] Set up PostgreSQL with backups
- [ ] Set up Redis with persistence
- [ ] Configure AWS S3 bucket
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS origins
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Set up backup strategy
- [ ] Test disaster recovery

## Monitoring & Logging

- All requests logged via audit middleware
- Structured logging in JSON format
- Health check endpoints (`/health`, `/ready`)
- Detailed error responses
- Performance metrics ready for APM integration

## Support

For issues or questions:
1. Check existing documentation
2. Review API error responses
3. Check application logs
4. Contact SimplyFI support

## License

Proprietary - SimplyFI 2024
