# SimplyFI PoR Platform - Docker Infrastructure & Celery Setup

This document describes the complete Docker infrastructure and Celery background task system for the SimplyFI Proof of Reserves (PoR) platform.

## Overview

The platform uses Docker Compose to orchestrate multiple services:

- **Backend**: FastAPI application with async database support
- **Frontend**: React application with Nginx reverse proxy
- **Database**: PostgreSQL 16 for persistent data
- **Cache**: Redis 7 for caching and message queue
- **Object Storage**: MinIO (S3-compatible) for report storage
- **Task Queue**: Celery workers for background jobs
- **Scheduler**: Celery Beat for periodic tasks
- **Reverse Proxy**: Nginx for routing and load balancing

## Quick Start

### 1. Initialize Environment

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Generate secure JWT secret (recommended)
python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))" >> backend/.env
```

### 2. Start All Services

```bash
# Build and start all containers
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f postgres
```

### 3. Initialize Database

```bash
# Option A: Automatic via Python script
docker-compose exec backend python /app/infrastructure/scripts/init_db.py

# Option B: Manual with Flask/Alembic migrations
docker-compose exec backend alembic upgrade head
```

### 4. Seed Demo Data (Optional)

```bash
docker-compose exec backend python /app/infrastructure/scripts/seed_demo_data.py
```

### 5. Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **PostgreSQL**: localhost:5432 (por_user/por_password)
- **Redis**: localhost:6379

## File Structure

### Docker Composition

```
docker-compose.yml           # Main orchestration file with all services
├── postgres                 # PostgreSQL 16 database
├── redis                    # Redis cache and message broker
├── minio                    # S3-compatible object storage
├── backend                  # FastAPI application
├── frontend                 # React SPA
├── celery_worker            # Task worker for async jobs
├── celery_beat              # Scheduler for periodic tasks
└── nginx                    # Reverse proxy and load balancer
```

### Backend Files

```
backend/
├── Dockerfile               # Production-ready Python 3.11 image
├── .env.example             # Complete environment variable template
├── requirements.txt         # Python dependencies
├── alembic.ini              # Database migration configuration
├── alembic/
│   └── env.py               # Async migration environment
└── app/
    ├── main.py              # FastAPI application entry
    ├── core/
    │   ├── config.py        # Settings management
    │   ├── database.py      # SQLAlchemy async setup
    │   └── security.py      # JWT and password hashing
    ├── models/              # SQLAlchemy ORM models
    ├── schemas/             # Pydantic request/response models
    ├── api/                 # API endpoints
    ├── services/            # Business logic
    ├── middleware/          # Custom middleware (audit, tenant)
    ├── utils/               # Utilities and validators
    └── tasks/               # Celery background tasks
        ├── __init__.py
        ├── celery_app.py    # Celery configuration and setup
        ├── verification_tasks.py  # Blockchain verification tasks
        ├── report_tasks.py        # Report generation tasks
        └── reconciliation_tasks.py # Daily reconciliation tasks
```

### Frontend Files

```
frontend/
├── Dockerfile               # Multi-stage build for Node + Nginx
├── nginx.conf               # Nginx configuration for SPA routing
└── [React application files]
```

### Infrastructure Files

```
infrastructure/
├── nginx/
│   ├── nginx.conf           # Main Nginx configuration with SSL support
│   └── default.conf         # Server block configuration template
└── scripts/
    ├── init_db.py           # Database initialization script
    ├── init_db.sql          # Initial database setup SQL
    └── seed_demo_data.py     # Demo data for testing
```

## Service Details

### PostgreSQL Database

```yaml
Image: postgres:16-alpine
Port: 5432
Credentials:
  - User: por_user
  - Password: por_password
  - Database: por_db
Volumes:
  - postgres_data: /var/lib/postgresql/data
Healthcheck: Every 10 seconds
```

**Key Features:**
- Async support via asyncpg
- Connection pooling (20 connections, 10 overflow)
- UUID and pgcrypto extensions
- Automatic initialization via init_db.sql

### Redis

```yaml
Image: redis:7-alpine
Port: 6379
Volumes:
  - redis_data: /data
Persistence:
  - AOF (Append-Only File) enabled
  - fsync: everysec
Healthcheck: Every 10 seconds
```

**Usage:**
- Cache (DB 0): General application caching
- Celery Broker (DB 1): Task queue messages
- Celery Backend (DB 2): Task result storage

### MinIO (Object Storage)

```yaml
Image: minio/latest
Ports:
  - 9000: API endpoint
  - 9001: Console (web UI)
Credentials:
  - Access Key: minioadmin
  - Secret Key: minioadmin
Volumes:
  - minio_data: /data
```

**Buckets Created:**
- `simplyfi-por-reports`: For PDF/CSV/XLSX report exports

### Backend (FastAPI)

```yaml
Image: Build from backend/Dockerfile
Port: 8000
Environment: 60+ configuration variables
Depends On: postgres, redis, minio (healthy)
Command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Features:**
- Async request handling
- Database connection pooling
- JWT authentication with refresh tokens
- Rate limiting (10 req/s general, 30 req/s API)
- WebSocket support for real-time updates
- CORS configured for frontend
- Health check endpoint at `/health`

### Frontend (React + Nginx)

```yaml
Build: Multi-stage (Node builder + Nginx runtime)
Port: 3000
Environment:
  - REACT_APP_API_URL=http://localhost:8000
  - REACT_APP_WS_URL=ws://localhost:8000
```

**Features:**
- SPA routing via Nginx try_files
- Gzip compression
- Security headers (HSTS, CSP, X-Frame-Options)
- Cache control for static assets
- 1-year expiry for versioned assets

### Celery Worker

```yaml
Image: Same as backend
Command: celery -A app.tasks.celery_app worker -l info --concurrency=4
Queue: verification, reports, reconciliation (priority-based)
Retry Settings:
  - Max retries: 3
  - Retry delay: 5 minutes
  - Hard timeout: 30 minutes
  - Soft timeout: 25 minutes
```

**Task Types:**
1. **Verification Tasks** (priority: 20)
   - `verify_wallet_balance_task`: Single wallet on-chain verification
   - `bulk_verify_engagement_task`: Bulk wallet verification
   - `verify_defi_positions_task`: DeFi position verification
   - `verify_proof_of_control_task`: Proof of control validation
   - `blockchain_health_check_task`: API health monitoring

2. **Report Tasks** (priority: 15)
   - `generate_por_report_task`: Full PoR report generation
   - `generate_merkle_tree_task`: Merkle tree construction
   - `generate_vara_compliance_report_task`: VARA compliance assessment
   - `export_reserve_ratio_table_task`: Data export (CSV/XLSX/PDF)

3. **Reconciliation Tasks** (priority: 5-10)
   - `daily_reconciliation_task`: Daily balance reconciliation
   - `check_reserve_ratios_task`: Reserve adequacy checks
   - `alert_under_reserved_task`: Under-reserve alerts
   - `generate_reconciliation_report_task`: Reconciliation reports
   - `cleanup_expired_tokens_task`: Token cleanup

### Celery Beat (Scheduler)

```yaml
Image: Same as backend
Command: celery -A app.tasks.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Beat Schedule:
  - blockchain_health_check: Every 15 minutes
  - reserve_ratio_check: Every 6 hours
  - daily_reconciliation: Every day at 00:00 UTC
  - cleanup_expired_tokens: Every hour
  - alert_under_reserved: Every 6 hours
```

### Nginx Reverse Proxy

```yaml
Image: nginx:alpine
Ports:
  - 80: HTTP (main)
  - 443: HTTPS (SSL-ready)
Routing:
  - /api/*      → backend:8000 (API requests)
  - /ws/*       → backend:8000 (WebSocket)
  - /           → frontend:3000 (SPA)
Rate Limiting:
  - /api/*:     30 req/s
  - /auth/*:    5 req/min
  - general:    10 req/s
Security Headers:
  - HSTS (31536000s)
  - CSP: strict-origin-when-cross-origin
  - X-Frame-Options: SAMEORIGIN
  - X-Content-Type-Options: nosniff
```

## Environment Configuration

### Backend Environment Variables

See `backend/.env.example` for complete list. Key sections:

```bash
# Application
APP_NAME=SimplyFI Proof of Reserves Platform
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# Database (Async PostgreSQL)
DATABASE_URL=postgresql+asyncpg://por_user:por_password@postgres:5432/por_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# S3 / MinIO
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=simplyfi-por-reports

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# VARA Compliance
VARA_COMPLIANCE_LEVEL=LEVEL_3
VARA_MIN_RESERVE_RATIO=0.95

# Blockchain APIs
ETHERSCAN_API_KEY=your_api_key
INFURA_API_KEY=your_api_key
ALCHEMY_API_KEY=your_api_key
```

## Celery Task System

### Task Execution Flow

```
User/API Request
    ↓
API Endpoint
    ↓
Task Enqueue to Redis
    ↓
Celery Worker Dequeue
    ↓
Task Execution
    ↓
Result Storage in Redis
    ↓
Database Update + WebSocket Notification
```

### Task Configuration (celery_app.py)

```python
# Serialization
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

# Execution
task_track_started = True
task_time_limit = 30 * 60  # Hard limit
task_soft_time_limit = 25 * 60  # Soft limit
task_acks_late = True

# Retry
task_autoretry_for = (Exception,)
task_max_retries = 3
task_default_retry_delay = 300  # 5 minutes

# Queues (priority-based)
- default: priority 10
- verification: priority 20 (highest)
- reports: priority 15
- reconciliation: priority 5 (lowest)
```

### Example Task Usage

```python
# In an API endpoint
from app.tasks.verification_tasks import verify_wallet_balance_task

# Fire and forget
task = verify_wallet_balance_task.delay(
    wallet_id=123,
    blockchain="ethereum",
    asset="ETH"
)

# Get result later
result = task.get(timeout=600)  # Wait up to 10 minutes

# Check status
if task.ready():
    print("Task completed with result:", task.result)
elif task.failed():
    print("Task failed:", task.traceback)
else:
    print("Task is still running...")
```

## Database Initialization

### Script-Based Initialization (init_db.py)

Automatically creates:
1. All SQLAlchemy models as tables
2. System roles (SuperAdmin, Auditor, VASP Admin, etc.)
3. System permissions (CRUD operations, compliance, etc.)
4. Default superadmin user (admin@simplyfi.com/ChangeMe123!@)
5. Top 40+ cryptocurrencies with blockchain info

```bash
docker-compose exec backend python /app/infrastructure/scripts/init_db.py
```

### Demo Data Seeding (seed_demo_data.py)

Creates testing data:
- 2 demo tenants (auditor + VASP)
- 3 demo users per tenant
- 1 complete engagement with wallets
- 100 customers with 4 assets each
- Merkle tree with 100 leaves
- 30 days of reconciliation records
- 30 days of reserve ratio history

```bash
docker-compose exec backend python /app/infrastructure/scripts/seed_demo_data.py
```

## Monitoring & Logs

### View Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat

# Last 100 lines
docker-compose logs --tail=100 backend

# Follow with timestamps
docker-compose logs -f --timestamps backend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker-compose exec postgres pg_isready -U por_user

# Redis health
docker-compose exec redis redis-cli ping

# MinIO health
curl http://localhost:9000/minio/health/live
```

### Monitor Celery Tasks

```bash
# Install celery monitoring (optional)
pip install flower

# Start Flower (task monitoring UI)
celery -A app.tasks.celery_app flower --port=5555

# Access at http://localhost:5555
```

## Production Deployment

### SSL/HTTPS Configuration

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update `infrastructure/nginx/nginx.conf`:
   ```nginx
   server {
       listen 443 ssl http2;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       # ... rest of configuration
   }
   ```

3. Redirect HTTP to HTTPS:
   ```nginx
   server {
       listen 80;
       return 301 https://$host$request_uri;
   }
   ```

### Environment Variables

1. Generate strong JWT secret:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Configure production database (RDS/Cloud SQL):
   ```bash
   DATABASE_URL=postgresql+asyncpg://user:password@prod-db-host:5432/por_db
   ```

3. Configure production Redis (ElastiCache/MemoryStore):
   ```bash
   REDIS_URL=redis://:password@prod-redis-host:6379/0
   ```

4. Configure production S3:
   ```bash
   S3_ENDPOINT=https://s3.amazonaws.com
   AWS_ACCESS_KEY_ID=***
   AWS_SECRET_ACCESS_KEY=***
   ```

5. Set blockchain API keys from production providers

### Docker Compose Override

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://...
      - REDIS_URL=redis://...
      - ENVIRONMENT=production
      # ... more production variables
    # Remove development mounts
```

Deploy with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U por_user -d por_db -c "SELECT 1"
```

### Redis Connection Issues

```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Check Redis keys
docker-compose exec redis redis-cli KEYS "*"
```

### Celery Worker Issues

```bash
# Check worker is running
docker-compose ps celery_worker

# View worker logs
docker-compose logs -f celery_worker

# Check Celery status
docker-compose exec celery_worker celery -A app.tasks.celery_app inspect active
```

### Task Stuck in Queue

```bash
# Purge all pending tasks (CAREFUL!)
docker-compose exec celery_worker celery -A app.tasks.celery_app purge

# Restart workers
docker-compose restart celery_worker
```

## Additional Resources

- FastAPI: https://fastapi.tiangolo.com/
- Celery: https://docs.celeryproject.org/
- SQLAlchemy: https://docs.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Redis: https://redis.io/documentation
- Nginx: https://nginx.org/en/docs/
- Docker Compose: https://docs.docker.com/compose/

## Support

For issues or questions, contact the SimplyFI development team.
