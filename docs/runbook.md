# SimplyFI PoR Platform: Operations Runbook

**Document Version**: 1.0
**Last Updated**: February 2026
**Target Audience**: DevOps, Platform Engineers, On-Call Engineers

---

## Table of Contents

1. [Deployment](#deployment)
2. [Scaling](#scaling)
3. [Incident Response](#incident-response)
4. [Rollback Procedures](#rollback-procedures)
5. [Backup & Recovery](#backup--recovery)
6. [Health Checks](#health-checks)
7. [Maintenance Windows](#maintenance-windows)

---

## Deployment

### Pre-Deployment Checklist

Before deploying to production, complete the following:

- [ ] Code merged to `main` branch with ≥2 approvals
- [ ] All automated tests passing (unit, integration, E2E)
- [ ] Security scan passed (SAST, dependency check)
- [ ] Performance regression testing completed
- [ ] Database migrations tested on staging
- [ ] API documentation updated
- [ ] Changelog updated with breaking changes noted
- [ ] Deployment plan reviewed by tech lead
- [ ] On-call engineer notified of deployment window
- [ ] Rollback procedure documented and tested
- [ ] Monitoring dashboards confirmed operational
- [ ] Feature flags prepared (if applicable)
- [ ] Customer communication drafted (if needed)

### Docker Compose Deployment (Development/Staging)

**Prerequisites**:
- Docker 24.0+
- Docker Compose 2.0+
- 8GB RAM minimum
- Network ports 5432, 6379, 9000, 8000 available

**Steps**:

1. **Clone repository and checkout target branch**:
```bash
git clone https://github.com/simplyfi/por-platform.git
cd simplyfi-por-platform
git checkout main
```

2. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env with deployment-specific values
nano .env

# Key variables:
# DATABASE_URL=postgresql+asyncpg://por_user:por_password@postgres:5432/por_db
# REDIS_URL=redis://redis:6379/0
# JWT_SECRET=<generate-strong-secret>
# AWS_ACCESS_KEY_ID=<minio-or-aws-key>
# AWS_SECRET_ACCESS_KEY=<minio-or-aws-secret>
# VARA_LICENSE_NUMBER=VARA-001-2024
# LOG_LEVEL=INFO
```

3. **Build and start services**:
```bash
docker-compose up -d

# Verify services are healthy
docker-compose ps

# Expected output:
# simplyfi-postgres   postgres:16-alpine       healthy
# simplyfi-redis      redis:7-alpine           healthy
# simplyfi-minio      minio:latest             healthy
# simplyfi-backend    (custom image)           up
```

4. **Initialize database**:
```bash
# Run migrations
docker exec simplyfi-backend alembic upgrade head

# Seed initial data (optional)
docker exec simplyfi-backend python -m app.scripts.seed_data
```

5. **Verify application**:
```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "database": "connected",
#   "redis": "connected",
#   "timestamp": "2024-01-15T10:30:00Z"
# }
```

6. **Check logs**:
```bash
# View backend logs
docker logs -f simplyfi-backend

# Check for startup errors
docker logs simplyfi-backend | grep -i error
```

### Kubernetes Deployment (Production)

**Prerequisites**:
- Kubernetes cluster 1.24+
- Helm 3.0+
- kubectl configured
- Resource quotas set (CPU, memory, storage)

**Helm Chart Structure**:
```
simplyfi-por-helm/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
├── templates/
│   ├── postgres-statefulset.yaml
│   ├── redis-statefulset.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── backend-hpa.yaml
│   ├── celery-worker-deployment.yaml
│   ├── celery-beat-deployment.yaml
│   ├── minio-statefulset.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
└── charts/
    └── postgresql/
```

**Installation Steps**:

1. **Create namespace**:
```bash
kubectl create namespace simplyfi-por
kubectl config set-context --current --namespace=simplyfi-por
```

2. **Create secrets**:
```bash
kubectl create secret generic simplyfi-secrets \
  --from-literal=jwt-secret=$(openssl rand -base64 32) \
  --from-literal=postgres-password=$(openssl rand -base64 32) \
  --from-literal=s3-key=$(aws configure get aws_access_key_id) \
  --from-literal=s3-secret=$(aws configure get aws_secret_access_key) \
  -n simplyfi-por

# Or use sealed secrets for GitOps
kubeseal -f secrets.yaml -w sealed-secrets.yaml
```

3. **Deploy using Helm**:
```bash
# Add Helm repository (if applicable)
helm repo add simplyfi https://charts.simplyfi.com
helm repo update

# Deploy to production
helm upgrade --install simplyfi-por simplyfi/por \
  --namespace simplyfi-por \
  --values values-prod.yaml \
  --set image.tag=v1.0.0 \
  --set replicas=3 \
  --wait

# Monitor rollout
kubectl rollout status deployment/simplyfi-backend -n simplyfi-por
```

4. **Verify deployment**:
```bash
# Check pod status
kubectl get pods -n simplyfi-por

# Check service endpoints
kubectl get svc -n simplyfi-por

# Test application
kubectl port-forward svc/simplyfi-backend 8000:8000 -n simplyfi-por &
curl http://localhost:8000/health
```

5. **Setup ingress** (if not already done):
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simplyfi-ingress
  namespace: simplyfi-por
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.simplyfi.com
    secretName: simplyfi-tls
  rules:
  - host: app.simplyfi.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: simplyfi-backend
            port:
              number: 8000
```

### Database Migration Procedure

**Before Running Migrations**:
- Backup current database
- Test migrations on staging environment
- Plan downtime window (if needed)
- Notify stakeholders

**Running Migrations**:

```bash
# Check current migration version
alembic current

# See pending migrations
alembic upgrade --sql head | head -20

# Run migrations
alembic upgrade head

# If error occurs, check migration status
alembic history

# Rollback if needed
alembic downgrade -1
```

**Alembic Configuration** (`backend/alembic.ini`):
```ini
[alembic]
script_location = alembic
sqlalchemy.url = driver://user:password@localhost/dbname
version_path_separator = :

[loggers]
keys = root,sqlalchemy

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
```

**Common Migrations**:

```python
# backend/alembic/versions/001_initial_schema.py
"""Initial schema creation."""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email')
    op.drop_table('users')
```

### Environment Variable Configuration

**Production Environment**:
```bash
# Application
APP_NAME=SimplyFI Proof of Reserves Platform
APP_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://user:password@postgres-rds.c3iq7vqhz.us-east-1.rds.amazonaws.com:5432/por_db
DB_POOL_SIZE=30
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600

# Redis
REDIS_URL=redis://redis-cluster.cache.amazonaws.com:6379/0
CELERY_BROKER_URL=redis://redis-cluster.cache.amazonaws.com:6379/1
CELERY_RESULT_BACKEND=redis://redis-cluster.cache.amazonaws.com:6379/2

# S3/Storage
S3_BUCKET=simplyfi-por-reports-prod
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=<production-key>
AWS_SECRET_ACCESS_KEY=<production-secret>
S3_ENDPOINT_URL=https://s3.amazonaws.com

# JWT
JWT_SECRET=<strong-random-secret-min-32-chars>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
PASSWORD_MIN_LENGTH=12
PASSWORD_REQUIRE_SPECIAL=True
MFA_ENABLED_BY_DEFAULT=True
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
CORS_ORIGINS=https://app.simplyfi.com

# Blockchain APIs
BLOCKCHAIN_API_TIMEOUT=30
ETHEREUM_INFURA_KEY=<key>
ETHEREUM_ETHERSCAN_KEY=<key>
BITCOIN_BLOCKSTREAM_API=https://blockstream.info/api
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# VARA Compliance
VARA_LICENSE_NUMBER=VARA-001-2024
VARA_COMPLIANCE_LEVEL=LEVEL_3
VARA_MIN_RESERVE_RATIO=0.95
VARA_AUDIT_RETENTION_YEARS=7

# Email
SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=<ses-user>
SMTP_PASSWORD=<ses-password>
EMAIL_FROM=noreply@simplyfi.com

# AI/ML
ENABLE_LOCAL_LLM=False
MAX_TOKENS_PER_REQUEST=4096

# Monitoring
OPENTELEMETRY_ENABLED=True
OPENTELEMETRY_ENDPOINT=http://localhost:4317
PROMETHEUS_METRICS_ENABLED=True
PAGERDUTY_API_KEY=<key>
PAGERDUTY_ESCALATION_POLICY=<policy-id>
```

### SSL/TLS Certificate Setup

**Let's Encrypt with Cert-Manager** (Kubernetes):

```yaml
# cert-manager-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@simplyfi.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Manual Certificate Setup** (Docker Compose):

```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out /etc/nginx/certs/cert.pem \
  -keyout /etc/nginx/certs/key.pem \
  -days 365 \
  -subj "/CN=app.simplyfi.com"

# Or use Let's Encrypt with Certbot
certbot certonly --standalone -d app.simplyfi.com

# Copy to nginx directory
cp /etc/letsencrypt/live/app.simplyfi.com/fullchain.pem /etc/nginx/certs/
cp /etc/letsencrypt/live/app.simplyfi.com/privkey.pem /etc/nginx/certs/
```

**NGINX Configuration** (`infrastructure/nginx/nginx.conf`):

```nginx
server {
    listen 443 ssl http2;
    server_name app.simplyfi.com;

    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name app.simplyfi.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Scaling

### Horizontal Scaling: Backend Replicas

**Kubernetes HPA (Horizontal Pod Autoscaler)**:

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: simplyfi-backend-hpa
  namespace: simplyfi-por
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: simplyfi-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

**Manual Scaling**:
```bash
# Scale backend to 5 replicas
kubectl scale deployment simplyfi-backend --replicas=5 -n simplyfi-por

# Monitor scaling
kubectl rollout status deployment/simplyfi-backend -n simplyfi-por
kubectl get hpa -n simplyfi-por -w
```

### Horizontal Scaling: Celery Workers

**Multi-Queue Setup**:
```yaml
# celery-workers-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-verification-worker
spec:
  replicas: 5  # 5 workers for verification queue
  template:
    spec:
      containers:
      - name: celery-worker
        image: simplyfi-por:latest
        args:
        - celery
        - -A
        - app.tasks.celery_app
        - worker
        - -l
        - info
        - -Q
        - verification
        - -c
        - 4  # 4 concurrent tasks per worker
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-report-worker
spec:
  replicas: 3  # Fewer workers for report queue (lower volume)
  template:
    spec:
      containers:
      - name: celery-worker
        image: simplyfi-por:latest
        args:
        - celery
        - -A
        - app.tasks.celery_app
        - worker
        - -l
        - info
        - -Q
        - reports
        - -c
        - 2
```

**Monitor Task Queue Depth**:
```bash
# Connect to Redis
redis-cli -h redis.simplyfi.com

# Check queue sizes
LLEN celery:verification
LLEN celery:reports
LLEN celery:reconciliation

# If queue depth high, scale workers
kubectl scale deployment celery-verification-worker --replicas=10
```

### Vertical Scaling: Pod Resource Limits

**Resource Requests & Limits**:
```yaml
# Increase resources during high-load periods
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simplyfi-backend
spec:
  template:
    spec:
      containers:
      - name: backend
        resources:
          requests:
            cpu: 2
            memory: 4Gi
          limits:
            cpu: 4
            memory: 8Gi
```

**Apply resource changes**:
```bash
# Update deployment with new resource limits
kubectl set resources deployment simplyfi-backend \
  --requests=cpu=2,memory=4Gi \
  --limits=cpu=4,memory=8Gi \
  -n simplyfi-por

# Pods will be recreated with new limits
```

### Database Scaling: Read Replicas

**Streaming Replication Setup**:
```bash
# Primary database writes
PRIMARY_DB="postgresql://user@primary.rds.amazonaws.com:5432/por_db"

# Read-only replicas
READ_REPLICA_1="postgresql://user@replica-1.rds.amazonaws.com:5432/por_db"
READ_REPLICA_2="postgresql://user@replica-2.rds.amazonaws.com:5432/por_db"
```

**Connection Pooling with PgBouncer**:
```ini
# pgbouncer.ini
[databases]
por_db = host=primary.rds.amazonaws.com port=5432 user=por_user

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 100
max_user_connections = 100
```

**Setup read replicas for reporting**:
```python
# backend/app/core/database.py
class DatabaseConnections:
    # Write operations go to primary
    WRITE_ENGINE = create_engine(
        "postgresql://user:password@primary.rds:5432/por_db"
    )

    # Read operations can use replicas
    READ_ENGINES = [
        create_engine("postgresql://user:password@replica-1.rds:5432/por_db"),
        create_engine("postgresql://user:password@replica-2.rds:5432/por_db")
    ]

    @staticmethod
    def get_read_connection():
        """Round-robin between read replicas."""
        import random
        return random.choice(DatabaseConnections.READ_ENGINES)

# Use in queries
async def get_verification_results(engagement_id: str):
    # Read from replica
    async with DatabaseConnections.get_read_connection() as session:
        results = await session.execute(
            select(AssetBalance).where(
                AssetBalance.engagement_id == engagement_id
            )
        )
        return results.all()
```

### Redis Scaling: Cluster Mode

**Redis Cluster Setup**:
```bash
# Create Redis cluster (6 nodes: 3 primary + 3 replica)
redis-server --port 6379 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 6380 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 6381 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 6382 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 6383 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 6384 --cluster-enabled yes --cluster-config-file nodes.conf

# Create cluster
redis-cli --cluster create 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 \
  127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384 --cluster-replicas 1
```

**Update Application Configuration**:
```python
# backend/app/core/config.py
REDIS_CLUSTER_NODES = [
    {"host": "redis-node-1", "port": 6379},
    {"host": "redis-node-2", "port": 6379},
    {"host": "redis-node-3", "port": 6379},
    {"host": "redis-node-4", "port": 6379},
    {"host": "redis-node-5", "port": 6379},
    {"host": "redis-node-6", "port": 6379}
]

# Use redis-py with cluster support
from rediscluster import RedisCluster
redis_cluster = RedisCluster(startup_nodes=REDIS_CLUSTER_NODES)
```

### Load Balancer Configuration

**AWS Application Load Balancer (ALB)**:
```hcl
# terraform/alb.tf
resource "aws_lb" "simplyfi" {
  name               = "simplyfi-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  enable_deletion_protection = true
}

resource "aws_lb_target_group" "backend" {
  name        = "simplyfi-backend-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.simplyfi.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
}
```

---

## Incident Response

### Severity Levels

| Level | Definition | Response Time | Escalation |
|-------|-----------|---------------|------------|
| **P1 (Critical)** | Service unavailable, data loss risk, under-reserved | 15 min | VP Engineering + CEO |
| **P2 (High)** | Partial service degradation, 1+ hours impact | 1 hour | Tech Lead + On-Call |
| **P3 (Medium)** | Non-critical feature broken, workaround exists | 4 hours | On-Call Engineer |
| **P4 (Low)** | Minor bug, cosmetic issue, no workaround needed | 24 hours | Team backlog |

### Incident Triage

**Triage Decision Tree**:

```
Is the platform completely down?
├─ YES → P1 (Critical)
│       └─ Page on-call immediately
│
└─ NO
    ├─ Is a VASP's audit under-reserved?
    │  ├─ YES → P1 (Critical)
    │  │       └─ Page Legal + Compliance
    │  │
    │  └─ NO
    │      ├─ Is a core feature broken for >10% of users?
    │      │  ├─ YES → P2 (High)
    │      │  │
    │      │  └─ NO
    │      │      ├─ Is a feature partially broken or slow?
    │      │      │  ├─ YES → P3 (Medium)
    │      │      │  │
    │      │      │  └─ NO → P4 (Low)
```

### Common Incident Types & Resolution

#### 1. Under-Reserved Assets Detected

**Symptoms**:
- Alert triggered: "BTC reserve ratio dropped to 93%"
- Email notification to VASP Compliance
- Dashboard shows red flag

**Diagnosis Steps**:
1. Check alert timestamp and reserve ratio value
2. Query recent blockchain balance: `GET /api/v1/blockchain/verify-balance/{address}`
3. Check customer liability data for changes
4. Review recent wallet transactions (Blockstream, Etherscan, etc.)
5. Contact VASP Finance for explanation

**Resolution Options**:
- **Option A**: Timing issue (blockchain confirmation pending)
  - Trigger immediate manual balance verification
  - Reserve ratio should recover within 1-2 hours
- **Option B**: Actual shortfall (customer fund loss)
  - ESCALATE to P1 (Critical)
  - Notify SimplyFI leadership + VARA regulator
  - Prepare incident report and remediation plan

**Post-Incident**:
```python
# Log incident investigation
POST /api/v1/incidents/under_reserved
{
  "engagement_id": "eng-123",
  "asset": "BTC",
  "reported_ratio": 0.93,
  "detected_at": "2024-01-15T10:30:00Z",
  "investigation": "Timing issue - blockchain confirmation pending",
  "resolved": true,
  "resolution_time_minutes": 45
}
```

#### 2. Blockchain API Failure

**Symptoms**:
- Verification task fails with "Etherscan API timeout"
- Blockchain adapter reports degraded status
- Auditor sees error message when trying to verify balance

**Diagnosis Steps**:
1. Check API provider status page (Etherscan, Infura, etc.)
2. Test direct API call: `curl https://api.etherscan.io/api?module=block&action=blocknumber`
3. Check platform logs for timeout errors: `docker logs simplyfi-backend | grep -i etherscan`
4. Monitor circuit breaker status: `redis-cli GET circuit-breaker:etherscan`
5. Check if fallback provider is working

**Resolution**:

**Option A**: Provider is down (temporary)
```bash
# System automatically falls back to secondary provider
# Monitor recovery
watch -n 5 'curl https://api.etherscan.io/api?module=block&action=blocknumber'

# Once recovered, circuit breaker auto-resets after timeout period
# Typically: 5 minutes after last error
```

**Option B**: Provider is down (prolonged, >30 min)
```python
# Manually trigger fallback and notify team
POST /api/v1/admin/fallback-api
{
  "blockchain": "ethereum",
  "primary_provider": "etherscan",
  "fallback_provider": "infura",
  "reason": "Primary API persistent failure"
}

# Log ticket for on-call to investigate
POST /api/v1/admin/escalate
{
  "incident_type": "API_FAILURE",
  "severity": "HIGH",
  "message": "Etherscan API down for 45 minutes, fallback engaged"
}
```

**Prevention**:
- Monitor provider health continuously
- Maintain at least 2 fallback providers per blockchain
- Set low circuit breaker failure thresholds (5 errors in 10 min)

#### 3. Database Connection Pool Exhaustion

**Symptoms**:
- API requests timeout with "could not connect to database"
- Error logs show "max_overflow exceeded"
- Response time degrades to 30+ seconds

**Diagnosis Steps**:
1. Check database connection pool status:
```bash
# Connect to database
psql postgresql://user:password@localhost:5432/por_db

# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Check connection limits
SHOW max_connections;
```

2. Check platform logs for connection leaks:
```bash
docker logs simplyfi-backend | grep "max_overflow\|pool_size\|connection"
```

3. Monitor Prometheus metrics:
```
db_pool_size{status="active"} / db_pool_size{status="total"} > 0.95
```

**Resolution**:

**Option A**: Connection leak (connections not being returned)
```python
# Restart backend to clear stale connections
docker restart simplyfi-backend

# Or graceful restart in Kubernetes
kubectl rollout restart deployment/simplyfi-backend -n simplyfi-por

# Monitor pool usage recovery
watch 'curl http://localhost:8000/metrics | grep db_pool'
```

**Option B**: Legitimate high load (many concurrent requests)
```bash
# Temporarily increase pool size
# Edit .env or Kubernetes ConfigMap
DB_POOL_SIZE=40  # Increase from 30
DB_MAX_OVERFLOW=20  # Increase from 10

# Restart services
docker-compose restart backend
# or
kubectl rollout restart deployment/simplyfi-backend

# Then scale horizontally
kubectl scale deployment simplyfi-backend --replicas=5 -n simplyfi-por
```

**Prevention**:
- Set connection pool timeout: 30 seconds
- Enable pool_pre_ping: True (verify connection before use)
- Monitor pool usage with alerts at 80% full

#### 4. Celery Worker Failure

**Symptoms**:
- Tasks stuck in queue (status: PENDING for >10 min)
- Reconciliation not running at scheduled time
- Error: "No workers available"

**Diagnosis Steps**:
1. Check worker processes:
```bash
# Check running workers
celery -A app.tasks.celery_app inspect active

# Check worker stats
celery -A app.tasks.celery_app inspect stats

# Check queue length
redis-cli LLEN celery:default
redis-cli LLEN celery:verification
redis-cli LLEN celery:reports
```

2. Check Celery logs:
```bash
docker logs simplyfi-celery-worker | tail -100
```

3. Check Redis connectivity:
```bash
redis-cli ping
redis-cli DBSIZE
```

**Resolution**:

**Option A**: Worker process crashed
```bash
# Restart Celery worker
docker restart simplyfi-celery-worker

# Or in Kubernetes
kubectl rollout restart deployment/celery-worker -n simplyfi-por

# Monitor for recovery
kubectl logs -f deployment/celery-worker -n simplyfi-por
```

**Option B**: Worker deadlocked (no CPU response)
```bash
# Kill and restart worker (may lose tasks in progress)
docker kill -s KILL simplyfi-celery-worker
docker restart simplyfi-celery-worker

# Retask any lost items from queue
# Tasks auto-retry if configured with acks_late=True
```

**Option C**: Redis broker connection lost
```bash
# Verify Redis is running
redis-cli ping

# Restart Redis if needed
docker restart simplyfi-redis

# Restart workers after Redis is back
docker restart simplyfi-celery-worker
```

#### 5. Authentication System Failure

**Symptoms**:
- "Invalid token" errors on all API requests
- JWT verification failing
- Users cannot log in

**Diagnosis Steps**:
1. Check JWT secret is correct:
```python
# Verify secret hasn't been rotated accidentally
echo $JWT_SECRET
# Compare with what's in code/config
```

2. Check token expiry:
```python
# Decode token and check exp claim
import jwt
token = "eyJ..."
decoded = jwt.decode(token, options={"verify_signature": False})
# Check "exp" is > current time
```

3. Check MFA issues:
```bash
# Verify MFA secrets are accessible
docker exec simplyfi-backend \
  psql -U por_user -d por_db -c \
  "SELECT id, mfa_enabled FROM users LIMIT 5;"
```

**Resolution**:

**Option A**: Token expired (normal)
```bash
# User should refresh token
POST /api/v1/auth/refresh
{
  "refresh_token": "eyJ..."
}
```

**Option B**: JWT secret incorrect
```bash
# Emergency: Generate new secret and rotate
export JWT_SECRET=$(openssl rand -base64 32)
docker-compose restart backend

# All existing tokens invalid - users must log in again
# Notify users of forced re-authentication
```

**Option C**: MFA system broken
```bash
# Disable MFA temporarily if broken
# Update config: MFA_ENABLED_BY_DEFAULT=False

# Re-enable after fixing
# Notify affected users
```

#### 6. Data Reconciliation Mismatch

**Symptoms**:
- Merkle tree verification fails: "Root hash mismatch"
- Report cannot be generated: "Liability data integrity check failed"
- Engagement stuck in VERIFICATION phase

**Diagnosis Steps**:
1. Compare original liability file with current data:
```bash
# Get original file hash
SELECT file_hash FROM liability_uploads
WHERE engagement_id='eng-123'
ORDER BY created_at DESC LIMIT 1;

# Verify uploaded file against hash
sha256sum uploaded_liability_file.csv
```

2. Check for data modifications:
```sql
SELECT * FROM audit_logs
WHERE resource='CustomerLiability' AND action='UPDATE'
AND engagement_id='eng-123'
ORDER BY created_at DESC;
```

3. Validate liability data integrity:
```python
# Sum totals should match
SELECT asset_id, SUM(balance) FROM customer_liabilities
WHERE engagement_id='eng-123'
GROUP BY asset_id;

# Compare with reported totals in engagement
```

**Resolution**:

**Option A**: File accidentally re-uploaded with wrong data
```bash
# Restore original liability file from backup
# Check S3 backup: s3://simplyfi-por-backups/liability/{engagement_id}/

# Delete mismatched records
DELETE FROM customer_liabilities
WHERE engagement_id='eng-123'
AND created_at > '2024-01-15T10:00:00';

# Re-generate Merkle tree
POST /api/v1/merkle/generate-tree
{
  "engagement_id": "eng-123"
}
```

**Option B**: Data corruption (database issue)
```bash
# CRITICAL - escalate immediately
# Run full database integrity check
REINDEX DATABASE por_db;

# Restore from backup if needed
# See Backup & Recovery section below
```

#### 7. DDoS or Rate Limiting Triggered

**Symptoms**:
- Requests returning HTTP 429 (Too Many Requests)
- Legitimate users blocked (high false positive rate)
- Spiky traffic pattern in logs

**Diagnosis Steps**:
1. Check rate limiter status:
```python
# Get current rate limiter state
redis-cli GET rate_limit:*
```

2. Analyze traffic pattern:
```bash
# Check logs for IPs being rate limited
docker logs simplyfi-backend | grep "429\|rate_limit"

# Count requests per IP
docker logs simplyfi-backend | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

3. Determine if legitimate or attack:
- Legitimate spike: Sudden audit engagement, batch job started
- Attack: Random IPs from different locations, invalid payloads

**Resolution**:

**Option A**: Legitimate traffic spike
```bash
# Temporarily increase rate limits
# Edit config or environment
RATE_LIMIT_PER_MINUTE=200  # Increase from 60
RATE_LIMIT_PER_HOUR=5000   # Increase from 1000

# Restart backend
docker restart simplyfi-backend

# Add IP whitelist for known batch jobs
POST /api/v1/admin/rate-limit-whitelist
{
  "ip": "203.0.113.0",
  "reason": "Batch liability upload from VASP"
}
```

**Option B**: DDoS attack
```bash
# Enable CloudFlare or WAF rules at LB level
# Temporary: IP whitelist only trusted networks
POST /api/v1/admin/ip-whitelist
{
  "cidrs": ["203.0.113.0/24"],  # VASP networks
  "reason": "Temporary DDoS mitigation"
}

# Monitor attack
watch 'docker logs simplyfi-backend | grep -c "429"'

# Once attack subsides, remove whitelist
```

---

## Rollback Procedures

### Application Rollback (Docker Image)

**Identify Previous Working Version**:
```bash
# Check image tags in registry
aws ecr describe-images --repository-name simplyfi-por --query 'sort_by(imageDetails, &imagePushedAt)' | tail -10

# Expected output:
# v1.0.0 (current)
# v0.9.9 (previous - stable)
# v0.9.8
```

**Rollback Steps**:

1. **Stop current version**:
```bash
docker-compose down  # Or kubectl delete deployment
```

2. **Start previous version**:
```bash
# Update docker-compose.yml
# Change image tag from v1.0.0 to v0.9.9
sed -i 's/simplyfi-por:v1.0.0/simplyfi-por:v0.9.9/g' docker-compose.yml

# Restart services
docker-compose up -d

# Or in Kubernetes
kubectl set image deployment/simplyfi-backend \
  simplyfi-backend=simplyfi-por:v0.9.9 \
  -n simplyfi-por

# Monitor rollout
kubectl rollout status deployment/simplyfi-backend -n simplyfi-por
```

3. **Verify health**:
```bash
# Health check endpoint
curl http://localhost:8000/health

# Check logs for errors
docker logs simplyfi-backend | head -50
```

4. **Test critical features**:
```bash
# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@simplyfi.com","password":"..."}' -

# Test verification
curl -X GET http://localhost:8000/api/v1/blockchain/verify-balance/0x123... \
  -H "Authorization: Bearer $TOKEN"
```

### Database Rollback (Alembic)

**Identify Failed Migration**:
```bash
# Check current version
alembic current

# Check migration history
alembic history | head -20
```

**Rollback Migration**:

1. **Single revision down**:
```bash
# Rollback one migration
alembic downgrade -1

# Verify current state
alembic current
```

2. **Multiple revisions down**:
```bash
# Rollback to specific revision
alembic downgrade ae1027a

# Or down N migrations
alembic downgrade -5
```

3. **Verify data integrity**:
```bash
# Check table structure after rollback
\d users
\d engagements
\d asset_balances

# Verify key data intact
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM engagements;
```

4. **If rollback fails**:
```bash
# CRITICAL: Restore from backup
# See Backup & Recovery section
```

### Configuration Rollback

**Environment Variables**:
```bash
# Previous version env file
cp .env.prod.v0.9.9 .env

# Restart with old config
docker-compose restart backend

# Verify
curl http://localhost:8000/health
```

**Feature Flags**:
```python
# If new feature broken, disable it
POST /api/v1/admin/feature-flags
{
  "flag": "new_merkle_algorithm",
  "enabled": false
}

# Or via environment
export FEATURE_FLAG_NEW_MERKLE=false
docker-compose restart backend
```

---

## Backup & Recovery

### Database Backup Schedule

**Automated Daily Backups**:
```bash
# Backup script: infrastructure/scripts/backup_db.sh
#!/bin/bash

BACKUP_DIR=/backups/database
BACKUP_DATE=$(date +%Y-%m-%d-%H%M%S)
DATABASE_URL="postgresql://user:password@localhost:5432/por_db"

# Perform backup
pg_dump "$DATABASE_URL" | gzip > "$BACKUP_DIR/por_db_$BACKUP_DATE.sql.gz"

# Upload to S3
aws s3 cp "$BACKUP_DIR/por_db_$BACKUP_DATE.sql.gz" s3://simplyfi-por-backups/database/

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
```

**Cron Schedule**:
```bash
# /etc/cron.d/simplyfi-backup
0 2 * * * /app/infrastructure/scripts/backup_db.sh  # 2 AM UTC daily
0 */6 * * * /app/infrastructure/scripts/backup_redis.sh  # Every 6 hours
```

### Point-in-Time Recovery (PITR)

**Single Engagement Restore**:
```bash
# 1. Identify backup closest to incident time
aws s3 ls s3://simplyfi-por-backups/database/ | grep 2024-01-15

# 2. Download backup
aws s3 cp s3://simplyfi-por-backups/database/por_db_2024-01-15-013000.sql.gz .

# 3. Restore to temporary database
createdb por_db_restore
gunzip -c por_db_2024-01-15-013000.sql.gz | psql por_db_restore

# 4. Verify data is as expected
psql por_db_restore -c "SELECT COUNT(*) FROM customer_liabilities WHERE engagement_id='eng-123';"

# 5. Copy specific tables back to production (if needed)
pg_dump -t customer_liabilities por_db_restore | psql por_db

# 6. Cleanup temporary database
dropdb por_db_restore
```

**Full Database Restore**:

```bash
# WARNING: This will overwrite current database!

# 1. Stop application
docker-compose down

# 2. Backup current database (safety)
pg_dump postgresql://user:password@localhost:5432/por_db | gzip > current_backup.sql.gz

# 3. Drop all tables
psql postgresql://user:password@localhost:5432/por_db \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 4. Restore from backup
gunzip -c por_db_2024-01-15-013000.sql.gz | \
  psql postgresql://user:password@localhost:5432/por_db

# 5. Verify integrity
psql -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM engagements;"

# 6. Start application
docker-compose up -d

# 7. Verify health
curl http://localhost:8000/health
```

### S3 Report Backup & Recovery

**S3 Lifecycle Policy** (auto-archive old reports):
```json
{
  "Rules": [
    {
      "Id": "ArchiveOldReports",
      "Status": "Enabled",
      "Prefix": "audit-reports/",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 365,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 2555  # 7 years per VARA regulations
      }
    }
  ]
}
```

**Restore Report from S3**:
```bash
# List backups for engagement
aws s3 ls s3://simplyfi-por-reports/audit-reports/eng-123/

# Download specific report
aws s3 cp s3://simplyfi-por-reports/audit-reports/eng-123/report-2024-01-15.pdf .

# Or restore to VASP if lost
aws s3 cp s3://simplyfi-por-reports/audit-reports/eng-123/report-2024-01-15.pdf \
  /var/www/reports/ && chmod 644 /var/www/reports/report-2024-01-15.pdf
```

### Redis Persistence & Recovery

**Redis RDB (Snapshot)**:
```bash
# Enabled in redis.conf
save 900 1      # Save after 900s if 1+ change
save 300 10     # Save after 300s if 10+ changes
save 60 10000   # Save after 60s if 10000+ changes

# Manual snapshot
redis-cli BGSAVE

# Backup RDB file
cp /data/dump.rdb /backups/redis/dump.rdb.$(date +%Y%m%d-%H%M%S)

# Upload to S3
aws s3 cp /backups/redis/dump.rdb.* s3://simplyfi-por-backups/redis/
```

**Recover Redis**:
```bash
# 1. Stop Redis
docker stop simplyfi-redis

# 2. Restore RDB file
aws s3 cp s3://simplyfi-por-backups/redis/dump.rdb.YYYYMMDD-HHMMSS /data/dump.rdb

# 3. Start Redis (loads from dump.rdb automatically)
docker start simplyfi-redis

# 4. Verify
redis-cli DBSIZE
redis-cli KEYS "*" | head
```

---

## Health Checks

### Application Health Endpoint

**GET /health**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "checks": {
    "database": {
      "status": "connected",
      "latency_ms": 5,
      "pool_size": 20,
      "active_connections": 8
    },
    "redis": {
      "status": "connected",
      "latency_ms": 2,
      "memory_used": 52428800
    },
    "blockchains": {
      "ethereum": {"status": "healthy", "latency_ms": 150},
      "bitcoin": {"status": "healthy", "latency_ms": 200},
      "solana": {"status": "degraded", "latency_ms": 1000}
    }
  }
}
```

**Implementation**:
```python
# backend/app/api/v1/endpoints/health.py
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    import time

    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "blockchains": await check_blockchains(),
        "celery": await check_celery()
    }

    # Determine overall status
    statuses = [check["status"] for check in checks.values()]
    if "down" in statuses:
        overall_status = "unhealthy"
    elif "degraded" in statuses:
        overall_status = "degraded"
    else:
        overall_status = "healthy"

    return {
        "status": overall_status,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }

async def check_database():
    """Test database connectivity."""
    try:
        start = time.time()
        async with get_session() as session:
            await session.execute(select(1))
        latency = (time.time() - start) * 1000

        # Check pool usage
        pool = engine.pool
        return {
            "status": "connected",
            "latency_ms": int(latency),
            "pool_size": len(pool._all_conns),
            "active_connections": len(pool._checkedout)
        }
    except Exception as e:
        return {"status": "down", "error": str(e)}
```

### Monitoring Dashboards

**Grafana Dashboard Queries**:

```promql
# API request rate
rate(api_requests_total[5m])

# API error rate
rate(api_errors_total[5m]) / rate(api_requests_total[5m])

# Database query latency
histogram_quantile(0.95, db_query_duration_seconds)

# Celery task queue depth
celery_queue_size{queue="verification"}

# Reserve ratio trend
reserve_ratio{engagement_id="eng-123"}

# Blockchain API availability
blockchain_api_up{provider="etherscan"}
```

### Alert Rules

**PrometheusRules** (`infrastructure/prometheus/rules.yml`):

```yaml
groups:
- name: simplyfi.rules
  interval: 30s
  rules:
  # Database alerts
  - alert: DatabaseDown
    expr: database_up == 0
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Database is down"

  - alert: PoolExhausted
    expr: db_pool_used / db_pool_size > 0.95
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Database pool nearly exhausted"

  # Blockchain API alerts
  - alert: BlockchainAPIDown
    expr: blockchain_api_up{provider="etherscan"} == 0
    for: 5m
    labels:
      severity: high
    annotations:
      summary: "Etherscan API down"

  # Celery alerts
  - alert: CeleryQueueBacklog
    expr: celery_queue_size > 1000
    for: 10m
    labels:
      severity: high
    annotations:
      summary: "Celery queue depth excessive"

  # Reserve ratio alerts
  - alert: UnderReserved
    expr: reserve_ratio < 0.95
    labels:
      severity: critical
    annotations:
      summary: "Asset {{ $labels.asset }} under-reserved"

  # API errors
  - alert: HighErrorRate
    expr: rate(api_errors_total[5m]) > 0.05
    for: 5m
    labels:
      severity: high
    annotations:
      summary: "API error rate > 5%"
```

---

## Maintenance Windows

### Scheduling Maintenance

**Announce Planned Downtime**:
```markdown
## Scheduled Maintenance

**Date & Time**: Saturday, Feb 15, 2024, 2:00-4:00 AM UTC
**Duration**: ~2 hours
**Affected Services**: Complete platform (UI, API, background jobs)
**Reason**: Database schema upgrade, optimization

**Action Required**:
- Plan audits around this window
- No new engagement start dates during maintenance window
- Save work in progress before 2 AM UTC

**Updates**: Updates will be posted on @simplyfi_status
```

**Customer Notification**:
```python
# Send notification emails 1 week, 3 days, 1 day before
@celery_app.task
def notify_maintenance_window():
    for tenant in Tenant.query.all():
        if tenant.type in ["VASP", "AUDITOR"]:
            send_email(
                to=tenant.admin_email,
                subject="Scheduled Maintenance Notification",
                template="maintenance_notice",
                variables={
                    "maintenance_start": "2024-02-15T02:00:00Z",
                    "maintenance_duration": "2 hours",
                    "reason": "Database optimization"
                }
            )
```

### Zero-Downtime Deployments

**Blue-Green Deployment**:
```bash
# Deploy new version to "green" environment
# Keep "blue" (current) running

# Run migrations and warm-up tests on green
# If successful, switch traffic to green
# Keep blue as instant rollback target

# Steps:
1. Deploy v1.0.1 to green-backend
2. Run smoke tests on green
3. Gradually shift traffic to green (via load balancer)
4. Monitor green for errors
5. If OK, decommission blue
6. If error, shift traffic back to blue immediately
```

**Kubernetes Rolling Update**:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simplyfi-backend
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # One extra pod during update
      maxUnavailable: 0  # Zero pods down (no downtime)
  template:
    spec:
      containers:
      - name: backend
        image: simplyfi-por:v1.0.1
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Canary Deployment**:
```bash
# Deploy v1.0.1 to 10% of traffic
kubectl set image deployment/simplyfi-backend \
  backend=simplyfi-por:v1.0.1 \
  --record

# Monitor canary for 30 minutes
# If error rate < 0.1%, continue rollout
# Otherwise, rollback immediately

watch 'kubectl rollout status deployment/simplyfi-backend'
```

### Cache Invalidation During Maintenance

```python
# Before deployment, clear caches that might cause issues
redis_client = redis.Redis(host="localhost", port=6379)

# Clear sensitive caches
redis_client.delete("cache:merkle_roots:*")
redis_client.delete("cache:reserve_ratios:*")
redis_client.delete("cache:verification_results:*")

# Keep session cache to avoid forcing re-login
# Keep blockchain balance cache for quick recovery

print("Caches cleared. Safe to deploy.")
```

---

## Summary

This runbook provides:
- Complete deployment procedures (Docker Compose, Kubernetes, Helm)
- Database migration and initialization steps
- Environment configuration and SSL/TLS setup
- Scaling strategies (horizontal, vertical, database, cache)
- Load balancer configuration (ALB, NGINX)
- Incident response procedures and resolutions for 7+ common incident types
- Rollback procedures for application, database, and configuration
- Backup and recovery procedures with point-in-time restore
- Health check endpoints and monitoring dashboards
- Alert rules and on-call escalation
- Maintenance windows and zero-downtime deployment strategies

Teams can use this document to:
- Deploy to development, staging, and production environments
- Scale applications and databases under load
- Respond to and resolve common incidents
- Recover from failures and data loss
- Schedule maintenance with minimal user impact
- Monitor application health and performance
- Train new on-call engineers on incident response

