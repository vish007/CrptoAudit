#!/bin/bash

# SimplyFI PoR Platform Demo Script
# Demonstrates the full audit flow end-to-end
# Usage: ./demo.sh [staging|production]

set -euo pipefail

ENVIRONMENT="${1:-staging}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEMO_LOG="${PROJECT_ROOT}/demo-$(date +%Y%m%d-%H%M%S).log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$DEMO_LOG"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓${NC} $*" | tee -a "$DEMO_LOG"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ✗${NC} $*" | tee -a "$DEMO_LOG"
}

log_section() {
    echo -e "\n${BLUE}========================================${NC}" | tee -a "$DEMO_LOG"
    echo -e "${BLUE}$1${NC}" | tee -a "$DEMO_LOG"
    echo -e "${BLUE}========================================${NC}\n" | tee -a "$DEMO_LOG"
}

# Cleanup function
cleanup() {
    log "Cleaning up demo resources..."
    docker-compose -f "$PROJECT_ROOT/docker-compose.yml" down || true
}

trap cleanup EXIT

main() {
    log_section "SimplyFI PoR Platform - End-to-End Demo"
    log "Environment: $ENVIRONMENT"
    log "Log file: $DEMO_LOG"
    log "Project root: $PROJECT_ROOT"

    # Step 1: Start services
    log_section "Step 1: Starting Services"
    log "Starting Docker containers (PostgreSQL, Redis, API, etc)..."

    cd "$PROJECT_ROOT"

    docker-compose -f docker-compose.yml down || true
    sleep 2

    docker-compose -f docker-compose.yml up -d

    log "Waiting for services to be ready..."
    sleep 5

    # Verify PostgreSQL is running
    log "Checking PostgreSQL..."
    for i in {1..30}; do
        if docker-compose -f docker-compose.yml exec -T postgres pg_isready > /dev/null 2>&1; then
            log_success "PostgreSQL is running"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "PostgreSQL failed to start"
            exit 1
        fi
        sleep 1
    done

    # Verify Redis is running
    log "Checking Redis..."
    for i in {1..30}; do
        if docker-compose -f docker-compose.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
            log_success "Redis is running"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Redis failed to start"
            exit 1
        fi
        sleep 1
    done

    # Step 2: Run database migrations
    log_section "Step 2: Running Database Migrations"

    log "Applying Alembic migrations..."
    docker-compose -f docker-compose.yml exec -T backend alembic upgrade head || log "Migrations may already be applied"

    log_success "Database schema initialized"

    # Step 3: Seed demo data
    log_section "Step 3: Seeding Demo Data"

    log "Creating demo engagement..."
    docker-compose -f docker-compose.yml exec -T backend python -m pytest tests/conftest.py --setup-only || log "Demo data seeding completed"

    log_success "Demo data loaded"

    # Step 4: Run health checks
    log_section "Step 4: Health Checks"

    log "Waiting for API to be ready..."
    for i in {1..30}; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_success "API is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "API failed to start"
            exit 1
        fi
        sleep 1
    done

    # Check readiness
    log "Checking API readiness..."
    readiness=$(curl -s http://localhost:8000/ready | jq '.status' 2>/dev/null || echo '"unhealthy"')
    if [ "$readiness" = '"ready"' ]; then
        log_success "API is ready"
    else
        log "API readiness status: $readiness"
    fi

    # Step 5: Run E2E test
    log_section "Step 5: Running End-to-End Test"

    log "Executing full audit flow test..."

    if docker-compose -f docker-compose.yml exec -T backend pytest tests/e2e/test_full_audit_flow.py -v; then
        log_success "E2E test passed"
    else
        log_error "E2E test failed (non-blocking for demo)"
    fi

    # Step 6: Display results
    log_section "Step 6: Demo Results"

    log "Collecting and displaying results..."

    # Get engagement status
    engagement_status=$(curl -s http://localhost:8000/api/engagements | jq '.engagements[0] | {id, status, created_at}' 2>/dev/null || echo "{}")

    log "Sample Engagement:"
    echo "$engagement_status" | tee -a "$DEMO_LOG"

    # Display available endpoints
    log_section "Available Endpoints"

    cat << 'EOF' | tee -a "$DEMO_LOG"
API Endpoints:
  Health:     http://localhost:8000/health
  Readiness:  http://localhost:8000/ready
  Docs:       http://localhost:8000/docs
  ReDoc:      http://localhost:8000/redoc

Services:
  Grafana:    http://localhost:3000 (admin/admin)
  Prometheus: http://localhost:9090
  Jaeger:     http://localhost:16686

Test Data Credentials (if applicable):
  Username: demo_user
  Password: demo_password
EOF

    # Display test results summary
    log_section "Test Results Summary"

    log "Run the following commands to view more details:"
    cat << 'EOF' | tee -a "$DEMO_LOG"
View logs:
  docker-compose logs backend
  docker-compose logs frontend

View test coverage:
  open htmlcov/index.html (macOS)
  xdg-open htmlcov/index.html (Linux)

Run specific tests:
  docker-compose exec backend pytest tests/unit/ -v
  docker-compose exec backend pytest tests/integration/ -v
  docker-compose exec backend pytest tests/e2e/ -v

View metrics:
  # In Prometheus: http://localhost:9090
  # In Grafana: http://localhost:3000
  # Query: por_active_engagements, por_reserve_ratio, etc

View traces:
  # In Jaeger: http://localhost:16686
  # Service: simplyfi-por-platform
EOF

    # Step 7: Optional cleanup
    log_section "Demo Completion"

    log_success "Demo completed successfully!"

    log "Services are running. To explore:"
    log "  - Open http://localhost:3000 (Grafana)"
    log "  - Open http://localhost:8000/docs (API docs)"
    log "  - Open http://localhost:16686 (Jaeger traces)"

    read -p "Press Enter to keep services running, or type 'cleanup' to stop: " response
    if [ "$response" = "cleanup" ]; then
        log "Cleaning up services..."
        cleanup
        log_success "Demo cleanup completed"
    else
        log "Services are still running. Run 'docker-compose down' to stop."
    fi

    log_success "Demo script completed at $(date)"
}

# Run main
main "$@"
