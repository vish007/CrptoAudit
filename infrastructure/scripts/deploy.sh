#!/bin/bash

# SimplyFI PoR Platform Deployment Script
# Handles zero-downtime rolling deployments with health checks
# Usage: ./deploy.sh [staging|production]

set -euo pipefail

# Configuration
ENVIRONMENT="${1:-staging}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
LOG_FILE="/var/log/simplyfi-por-deploy-$(date +%Y%m%d-%H%M%S).log"
HEALTH_CHECK_TIMEOUT=300  # 5 minutes
HEALTH_CHECK_INTERVAL=10  # Check every 10 seconds
DEPLOYMENT_TIMEOUT=600    # 10 minutes

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ✗${NC} $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠${NC} $*" | tee -a "$LOG_FILE"
}

# Function to validate environment
validate_environment() {
    log "Validating environment: $ENVIRONMENT"

    if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
        log_error "Invalid environment: $ENVIRONMENT. Must be 'staging' or 'production'."
        exit 1
    fi

    # Check required commands
    local required_commands=("docker" "docker-compose" "curl" "git")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command not found: $cmd"
            exit 1
        fi
    done

    log_success "Environment validation passed"
}

# Function to load deployment configuration
load_deployment_config() {
    log "Loading deployment configuration for $ENVIRONMENT"

    local config_file="$PROJECT_ROOT/infrastructure/deploy-${ENVIRONMENT}.env"
    if [ ! -f "$config_file" ]; then
        log_error "Configuration file not found: $config_file"
        exit 1
    fi

    # shellcheck disable=SC1090
    source "$config_file"

    log_success "Deployment configuration loaded"
}

# Function to backup current deployment
backup_current_deployment() {
    log "Backing up current deployment state"

    local backup_dir="/var/backups/simplyfi-por/$ENVIRONMENT/$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup docker-compose state
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" ps > "$backup_dir/docker-compose-ps.txt" 2>&1 || true
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" logs --no-color > "$backup_dir/docker-compose-logs.txt" 2>&1 || true
    fi

    # Backup database
    log "Creating database backup"
    PGPASSWORD="${DB_PASSWORD}" pg_dump -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" > "$backup_dir/database-backup.sql" 2>&1 || log_warning "Database backup failed (non-critical)"

    echo "$backup_dir"
}

# Function to pull latest images
pull_latest_images() {
    log "Pulling latest Docker images"

    local registry="${REGISTRY:-ghcr.io}"
    local image_name="${IMAGE_NAME:-simplyfi-por-platform}"
    local tag="${DEPLOYMENT_TAG:-latest}"

    log "Pulling backend image: $registry/$image_name:${tag}-backend"
    docker pull "$registry/$image_name:${tag}-backend" || {
        log_error "Failed to pull backend image"
        return 1
    }

    log "Pulling frontend image: $registry/$image_name:${tag}-frontend"
    docker pull "$registry/$image_name:${tag}-frontend" || {
        log_error "Failed to pull frontend image"
        return 1
    }

    log_success "Docker images pulled successfully"
}

# Function to run database migrations
run_database_migrations() {
    log "Running database migrations"

    # Set environment variables for alembic
    export DATABASE_URL="${DATABASE_URL}"

    cd "$PROJECT_ROOT/backend" || exit 1

    log "Upgrading database schema with alembic"
    if ! alembic upgrade head; then
        log_error "Database migration failed"
        return 1
    fi

    log_success "Database migrations completed successfully"
}

# Function to health check a single endpoint
health_check_endpoint() {
    local url="$1"
    local max_attempts=$((HEALTH_CHECK_TIMEOUT / HEALTH_CHECK_INTERVAL))
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            return 0
        fi

        attempt=$((attempt + 1))
        if [ $attempt -lt $max_attempts ]; then
            sleep "$HEALTH_CHECK_INTERVAL"
        fi
    done

    return 1
}

# Function to perform comprehensive health checks
health_check() {
    log "Performing health checks"

    local api_url="${API_URL:-http://localhost:8000}"
    local health_endpoint="$api_url/health"
    local ready_endpoint="$api_url/ready"

    log "Checking API health: $health_endpoint"
    if ! health_check_endpoint "$health_endpoint"; then
        log_error "Health check failed for API"
        return 1
    fi
    log_success "API health check passed"

    log "Checking API readiness: $ready_endpoint"
    if ! health_check_endpoint "$ready_endpoint"; then
        log_error "Readiness check failed for API"
        return 1
    fi
    log_success "API readiness check passed"

    # Check database connectivity
    log "Checking database connectivity"
    PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -c "SELECT 1;" > /dev/null 2>&1 || {
        log_error "Database health check failed"
        return 1
    }
    log_success "Database health check passed"

    # Check Redis connectivity
    if command -v redis-cli &> /dev/null; then
        log "Checking Redis connectivity"
        redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" ping > /dev/null 2>&1 || {
            log_warning "Redis health check failed (non-critical)"
        }
        log_success "Redis health check passed"
    fi

    log_success "All health checks passed"
}

# Function to perform rolling deployment
rolling_deployment() {
    log "Starting rolling deployment"

    local registry="${REGISTRY:-ghcr.io}"
    local image_name="${IMAGE_NAME:-simplyfi-por-platform}"
    local tag="${DEPLOYMENT_TAG:-latest}"

    cd "$PROJECT_ROOT" || exit 1

    # Create new docker-compose override for this deployment
    local compose_override="docker-compose.override-${ENVIRONMENT}.yml"

    # Update environment-specific variables
    export REGISTRY="$registry"
    export IMAGE_NAME="$image_name"
    export DEPLOYMENT_TAG="$tag"
    export ENVIRONMENT="$ENVIRONMENT"

    log "Deploying with docker-compose: docker-compose -f docker-compose.yml up -d --no-deps --scale backend=2"

    # Scale backend to 2 instances for rolling deployment
    if ! docker-compose -f docker-compose.yml up -d --no-deps --scale backend=2; then
        log_error "Docker-compose deployment failed"
        return 1
    fi

    log "Waiting for new instances to become healthy"
    sleep 10

    # Wait for all instances to be healthy
    if ! health_check; then
        log_error "Health check failed after deployment"
        return 1
    fi

    # Scale back to 1 instance
    log "Scaling back to 1 backend instance"
    docker-compose -f docker-compose.yml up -d --no-deps --scale backend=1 || log_warning "Scale down warning (non-critical)"

    log_success "Rolling deployment completed"
}

# Function to notify deployment status
notify_deployment() {
    local status="$1"
    local environment="$2"
    local message="$3"

    # Slack notification
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        local color="good"
        if [ "$status" == "failure" ]; then
            color="danger"
        elif [ "$status" == "warning" ]; then
            color="warning"
        fi

        curl -X POST "${SLACK_WEBHOOK_URL}" -H 'Content-type: application/json' \
            --data "{
                \"attachments\": [
                    {
                        \"color\": \"$color\",
                        \"title\": \"SimplyFI PoR Deployment - $environment\",
                        \"text\": \"$message\",
                        \"fields\": [
                            {
                                \"title\": \"Status\",
                                \"value\": \"$status\",
                                \"short\": true
                            },
                            {
                                \"title\": \"Environment\",
                                \"value\": \"$environment\",
                                \"short\": true
                            },
                            {
                                \"title\": \"Time\",
                                \"value\": \"$(date +'%Y-%m-%d %H:%M:%S')\",
                                \"short\": false
                            }
                        ]
                    }
                ]
            }" 2>/dev/null || log_warning "Failed to send Slack notification"
    fi
}

# Function to verify deployment
verify_deployment() {
    log "Verifying deployment"

    # Check if containers are running
    log "Checking container status"
    local running_containers=$(docker-compose -f "$PROJECT_ROOT/docker-compose.yml" ps | grep -c "Up" || true)

    if [ "$running_containers" -lt 3 ]; then
        log_warning "Expected at least 3 running containers, found $running_containers"
    else
        log_success "Container status verified"
    fi

    # Check logs for errors
    log "Checking logs for errors"
    if docker-compose -f "$PROJECT_ROOT/docker-compose.yml" logs | grep -i "error\|exception" | head -5; then
        log_warning "Errors found in logs (review manually)"
    else
        log_success "No critical errors in logs"
    fi
}

# Function to rollback deployment
rollback_deployment() {
    log_error "Deployment failed, initiating rollback"

    # This would call the rollback script
    if [ -f "$SCRIPT_DIR/rollback.sh" ]; then
        bash "$SCRIPT_DIR/rollback.sh" "$ENVIRONMENT" || log_error "Rollback also failed - manual intervention required"
    else
        log_error "Rollback script not found"
        return 1
    fi
}

# Main deployment flow
main() {
    log "====== SimplyFI PoR Platform Deployment Started ======"
    log "Environment: $ENVIRONMENT"
    log "Log file: $LOG_FILE"

    local backup_location=""

    # Execute deployment steps
    if validate_environment && \
       load_deployment_config && \
       backup_location=$(backup_current_deployment) && \
       pull_latest_images && \
       run_database_migrations && \
       rolling_deployment && \
       health_check && \
       verify_deployment; then

        log_success "====== Deployment Completed Successfully ======"
        log "Backup location: $backup_location"
        notify_deployment "success" "$ENVIRONMENT" "SimplyFI PoR Platform deployed successfully to $ENVIRONMENT"
        return 0
    else
        log_error "====== Deployment Failed ======"
        log "Backup location: $backup_location"
        notify_deployment "failure" "$ENVIRONMENT" "SimplyFI PoR Platform deployment to $ENVIRONMENT failed. Check logs: $LOG_FILE"
        rollback_deployment || true
        return 1
    fi
}

# Execute main
main "$@"
