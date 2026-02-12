# SimplyFI Proof of Reserves (PoR) Platform

## Enterprise Crypto Digital Asset Auditing Platform

A full-stack, multi-tenant SaaS platform for performing Proof of Reserves (PoR) audits on VARA-regulated Virtual Asset Service Providers (VASPs). Built for SimplyFI's advisory and assurance practice, this platform enables end-to-end audit workflows covering 153+ cryptocurrencies across 20+ blockchains.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        NGINX (Reverse Proxy)                     │
│                    Port 80 / SSL Termination                     │
├────────────────────────┬────────────────────────────────────────┤
│                        │                                         │
│   React Frontend       │        FastAPI Backend                  │
│   (Port 3000)          │        (Port 8000)                      │
│                        │                                         │
│   - Auditor Dashboard  │   - REST API (60+ endpoints)           │
│   - VASP Dashboard     │   - JWT Auth + RBAC                    │
│   - Merkle Tree Viz    │   - WebSocket (real-time)              │
│   - Blockchain Explorer│   - Background Tasks (Celery)          │
│   - Report Builder     │   - AI Agent (LLaMA)                   │
│   - Onboarding Wizard  │   - Blockchain Adapters                │
│   - Customer Portal    │   - Merkle Tree Engine                 │
│   - Admin Panel        │   - Report Generator                   │
│                        │   - VARA Compliance Engine              │
├────────────────────────┴────────────────────────────────────────┤
│                        Data Layer                                │
│  ┌──────────┐  ┌───────┐  ┌───────┐  ┌──────────────────────┐  │
│  │PostgreSQL│  │ Redis │  │ MinIO │  │  Blockchain APIs      │  │
│  │  (RBAC,  │  │(Cache,│  │ (S3   │  │  (Etherscan, Infura, │  │
│  │ Engage-  │  │ Queue,│  │Report │  │  Blockstream, Solana, │  │
│  │ ments,   │  │ Pub/  │  │Storage│  │  XRP Ledger, BSCScan)│  │
│  │ Assets)  │  │ Sub)  │  │   )   │  │                      │  │
│  └──────────┘  └───────┘  └───────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Proof of Reserves Engine
- On-chain verification of 153+ cryptocurrencies across 20+ blockchains
- Asset balance verification with independent blockchain queries
- Proof of control via instructed movement of funds
- Customer liability verification with data integrity checks
- Reserve ratio calculation (assets vs liabilities per asset class)
- VARA 100% one-to-one reserve requirement compliance checking

### Merkle Tree Verification
- SHA-256 / Keccak-256 Merkle tree construction
- Supports millions of customer leaves with streaming processing
- Individual customer proof generation and verification
- Interactive tree visualization in the UI
- Customer self-service verification portal
- Published Merkle root hash for transparency

### Blockchain Integration
- Bitcoin: UTXO verification, multi-provider (Blockstream, Mempool.space)
- Ethereum: ERC-20, DeFi positions (Aave, Compound, Uniswap, Lido)
- Solana: SPL tokens, staking accounts
- XRP Ledger: Trust lines, payments
- BNB Chain: BEP-20, staking
- L2 Support: Arbitrum, Optimism, Polygon, Base, zkSync

### Agentic AI (LLaMA)
- Anomaly detection in balances and transactions
- Automated report narrative generation
- VARA compliance assessment
- Interactive audit assistant (chat)
- DeFi risk scoring
- Fallback to rule-based analysis when LLM unavailable

### Role-Based Access Control
- 7 system roles: SuperAdmin, Auditor, VASP Admin, VASP Finance, VASP Compliance, Customer, Regulator
- Custom role builder with permission matrix
- Field-level access restrictions
- Per-engagement scoped permissions
- Full audit logging of all actions

### Report Generation
- PoR Agreed-Upon Procedures Report (ISRS 4400)
- Assurance Report (ISAE 3000)
- Reserve Ratio Summary Table
- Management Letter
- Customer-Facing Summary
- VARA Quarterly Compliance Statement
- Export as JSON, CSV, XLSX, PDF

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Redux Toolkit, Tailwind CSS, Recharts, Framer Motion |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2, Celery |
| Database | PostgreSQL 16 (async), Redis 7, MinIO (S3) |
| AI | LLaMA (llama-cpp-python), LangChain, rule-based fallback |
| Blockchain | Web3.py, python-bitcoinlib, solders, xrpl-py |
| Infrastructure | Docker, Nginx, Alembic (migrations) |

---

## Quick Start

### Prerequisites
- Docker and Docker Compose v2
- Git

### 1. Clone and Configure

```bash
cd simplyfi-por-platform
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys and configuration
```

### 2. Launch All Services

```bash
docker-compose up -d
```

This starts: PostgreSQL, Redis, MinIO, Backend API, Frontend, Celery Worker, Celery Beat, Nginx

### 3. Initialize Database

```bash
docker-compose exec backend python -m infrastructure.scripts.init_db
```

### 4. Seed Demo Data (Optional)

```bash
docker-compose exec backend python -m infrastructure.scripts.seed_demo_data
```

### 5. Access the Platform

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/v1 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |

### Default Credentials (Demo)
- SuperAdmin: admin@simplyfi.com / Admin123!
- Auditor: auditor@simplyfi.com / Auditor123!
- VASP Admin: vasp@demo-exchange.com / Vasp123!

---

## Project Structure

```
simplyfi-por-platform/
├── docker-compose.yml
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   ├── alembic/
│   │   └── env.py
│   └── app/
│       ├── main.py                    # FastAPI application
│       ├── core/
│       │   ├── config.py              # Settings & environment
│       │   ├── security.py            # JWT, passwords, permissions
│       │   └── database.py            # Async SQLAlchemy setup
│       ├── models/
│       │   ├── user.py                # User, Tenant, Role, AuditLog
│       │   ├── engagement.py          # Engagement, Timeline
│       │   ├── asset.py               # CryptoAsset, Wallet, Balance, DeFi
│       │   └── merkle.py              # MerkleTree, Leaf, Proof
│       ├── schemas/
│       │   ├── user.py                # Auth & user schemas
│       │   ├── engagement.py          # Engagement schemas
│       │   ├── asset.py               # Asset & reserve schemas
│       │   └── merkle.py              # Merkle tree schemas
│       ├── api/v1/
│       │   ├── router.py              # Main API router
│       │   └── endpoints/
│       │       ├── auth.py            # Login, register, MFA
│       │       ├── users.py           # User management
│       │       ├── tenants.py         # Tenant management
│       │       ├── engagements.py     # Engagement CRUD
│       │       ├── assets.py          # Asset management
│       │       ├── reserves.py        # Reserve verification
│       │       ├── merkle.py          # Merkle tree operations
│       │       ├── blockchain.py      # On-chain verification
│       │       ├── reports.py         # Report generation
│       │       ├── ai.py              # AI agent endpoints
│       │       ├── admin.py           # Administration
│       │       └── onboarding.py      # VASP onboarding
│       ├── services/
│       │   ├── blockchain/
│       │   │   ├── base_adapter.py    # Abstract blockchain adapter
│       │   │   ├── ethereum_adapter.py
│       │   │   ├── bitcoin_adapter.py
│       │   │   ├── solana_adapter.py
│       │   │   ├── xrp_adapter.py
│       │   │   ├── bnb_adapter.py
│       │   │   ├── multi_chain_adapter.py  # Chain orchestrator
│       │   │   └── defi_verifier.py   # DeFi position verification
│       │   ├── merkle/
│       │   │   ├── merkle_engine.py   # Merkle tree construction
│       │   │   └── customer_verifier.py
│       │   ├── ai/
│       │   │   ├── llama_agent.py     # LLaMA-based audit agent
│       │   │   ├── anomaly_detector.py
│       │   │   └── compliance_engine.py
│       │   └── reports/
│       │       └── por_report_generator.py
│       ├── tasks/
│       │   ├── celery_app.py          # Celery configuration
│       │   ├── verification_tasks.py  # On-chain verification
│       │   ├── report_tasks.py        # Report generation
│       │   └── reconciliation_tasks.py
│       ├── middleware/
│       │   ├── audit_log.py           # Action audit logging
│       │   └── tenant.py              # Tenant isolation
│       └── utils/
│           ├── pagination.py
│           └── validators.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── index.css
│       ├── App.jsx                    # Routes & layout
│       ├── store/
│       │   ├── index.js               # Redux store
│       │   └── slices/
│       │       ├── authSlice.js
│       │       ├── engagementSlice.js
│       │       ├── dashboardSlice.js
│       │       └── uiSlice.js
│       ├── services/
│       │   ├── api.js                 # Axios instance
│       │   ├── authService.js
│       │   ├── engagementService.js
│       │   ├── assetService.js
│       │   ├── merkleService.js
│       │   ├── reportService.js
│       │   ├── blockchainService.js
│       │   ├── aiService.js
│       │   └── adminService.js
│       ├── hooks/
│       │   ├── useAuth.js
│       │   ├── usePermissions.js
│       │   ├── useEngagement.js
│       │   └── useWebSocket.js
│       ├── components/
│       │   ├── common/
│       │   │   ├── Button.jsx
│       │   │   ├── Card.jsx
│       │   │   ├── DataTable.jsx
│       │   │   ├── Modal.jsx
│       │   │   ├── StatusBadge.jsx
│       │   │   ├── LoadingSpinner.jsx
│       │   │   ├── PermissionGate.jsx
│       │   │   └── StatCard.jsx
│       │   ├── layout/
│       │   │   ├── Sidebar.jsx
│       │   │   ├── Header.jsx
│       │   │   └── Layout.jsx
│       │   ├── dashboard/
│       │   │   └── ReserveRatioChart.jsx
│       │   └── audit/
│       │       ├── VerificationTimeline.jsx
│       │       └── ComplianceScorecard.jsx
│       ├── pages/
│       │   ├── dashboard/
│       │   │   ├── AuditorDashboard.jsx
│       │   │   └── VASPDashboard.jsx
│       │   ├── engagements/
│       │   │   └── EngagementDetail.jsx
│       │   ├── merkle/
│       │   │   └── MerkleTreeVisualization.jsx
│       │   ├── blockchain/
│       │   │   └── BlockchainExplorer.jsx
│       │   ├── reports/
│       │   │   └── ReportBuilder.jsx
│       │   ├── admin/
│       │   │   └── RoleBuilder.jsx
│       │   ├── onboarding/
│       │   │   └── OnboardingWizard.jsx
│       │   └── customer/
│       │       └── CustomerVerification.jsx
│       ├── types/
│       │   └── index.js
│       └── utils/
│           ├── formatters.js
│           ├── constants.js
│           └── validators.js
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── default.conf
│   └── scripts/
│       ├── init_db.py
│       └── seed_demo_data.py
│
└── docs/
```

---

## VARA Regulatory Compliance

This platform is designed to comply with:

| Regulation | Coverage |
|-----------|----------|
| Law No. 4 of 2022 (Dubai VA Law) | Full alignment |
| VARA CRM Rulebook Part V, Section B | Client VA treatment & segregation |
| VARA CRM Rulebook Part V, Section C | Proof of Reserves procedures |
| VARA CRM Rulebook Part V, Section D | Daily reconciliation |
| VARA Company Rulebook | Capital & prudential requirements |
| ISRS 4400 (Revised) | Agreed-Upon Procedures |
| ISAE 3000 (Revised) | Assurance engagements |

### Automated VARA Compliance Checks
1. 100% reserve requirement (1:1 same-asset backing)
2. Daily reconciliation monitoring
3. Client asset segregation verification
4. Quarterly reporting compliance
5. Semi-annual audit tracking
6. Audit trail maintenance
7. Wallet address reporting
8. Fraud prevention controls

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/login | User login |
| POST | /api/v1/auth/register | User registration |
| POST | /api/v1/auth/refresh | Refresh token |
| POST | /api/v1/auth/mfa/setup | Setup MFA |

### Engagements
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/engagements | List engagements |
| POST | /api/v1/engagements | Create engagement |
| GET | /api/v1/engagements/{id} | Get engagement detail |
| PUT | /api/v1/engagements/{id}/status | Update status |
| GET | /api/v1/engagements/{id}/summary | Get summary |

### Reserves
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/engagements/{id}/reserves | Get reserves |
| POST | /api/v1/engagements/{id}/reserves/calculate | Calculate ratios |
| GET | /api/v1/engagements/{id}/reserves/ratio-table | Ratio table |

### Merkle Tree
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/engagements/{id}/merkle/generate | Generate tree |
| GET | /api/v1/engagements/{id}/merkle/root | Get root hash |
| POST | /api/v1/merkle/verify | Verify customer proof |

### Blockchain
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/blockchain/verify-address | Verify address |
| POST | /api/v1/blockchain/verify-balance | Verify balance |
| GET | /api/v1/blockchain/supported-chains | List chains |

### AI Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/ai/analyze | Anomaly analysis |
| POST | /api/v1/ai/generate-narrative | Report narrative |
| POST | /api/v1/ai/compliance-check | VARA compliance |
| POST | /api/v1/ai/chat | Audit assistant |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/engagements/{id}/reports/por | Generate PoR report |
| POST | /api/v1/engagements/{id}/reports/assurance | Assurance report |
| GET | /api/v1/reports/{id}/download | Download report |

Full API documentation available at http://localhost:8000/docs (Swagger UI)

---

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Run Celery Workers
```bash
celery -A app.tasks.celery_app worker --loglevel=info
celery -A app.tasks.celery_app beat --loglevel=info
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Security Considerations

- JWT tokens with configurable expiration and refresh
- Multi-factor authentication (TOTP)
- bcrypt password hashing (12 rounds)
- Tenant data isolation at middleware level
- Full audit logging of all mutations
- Rate limiting per endpoint
- CORS configured per environment
- Security headers (HSTS, CSP, X-Frame-Options)
- Encrypted S3 storage for reports
- API key rotation support
- Session management with Redis

---

## License

Proprietary - SimplyFI Advisory | Assurance | Digital Assets

---

## Support

For technical support, contact the SimplyFI engineering team.
