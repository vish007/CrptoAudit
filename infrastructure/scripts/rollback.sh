#!/bin/bash

# SimplyFI PoR Platform Rollback Script
# Handles rollback to a previous version
# Usage: ./rollback.sh [staging|production] [version|tag]

set -euo pipefail

# Configuration
ENVIRONMENT="${1:-staging}"
TARGET_VERSION="${2:-previous}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
LOG_FILE="/var/log/simplyfi-por-rollback-$(date +%Y%m%d-%H%M%S).log"
HEALTH_CHECK_TIMEOUT=300
HEALTH_CHECK_INTERVAL=10

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
    log "Validating rollback environment: $ENVIRONMENT"

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

# Function to get previous version
get_previous_version() {
    log "Retrieving previous deployment version"

    local version_file="/var/lib/simplyfi-por/$ENVIRONMENT/deployment-history.txt"

    if [ ! -f "$version_file" ]; then
        log_error "Deployment history file not found: $version_file"
        return 1
    fi

    # Get second line (previous version)
    tail -2 "$version_file" | head -1 | awk '{print $1}' || {
        log_error "Could not determine previous version"
        return 1
    }
}

# Function to get deployment version by tag
get_version_by_tag() {
    local tag="$1"
    log "Looking up version for tag: $tag"

    # Query git for tag
    if git rev-parse "$tag" &> /dev/null; then
        git rev-parse "$tag" | head -c 8
    else
        log_error "Tag not found: $tag"
        return 1
    fi
}

# Function to determine rollback target version
determine_target_version() {
    log "Determining target version for rollback"

    local target_version
    if [ "$TARGET_VERSION" == "previous" ]; then
        target_version=$(get_previous_version) || return 1
        log "Rolling back to previous version: $target_version"
    else
        target_version=$(get_version_by_tag "$TARGET_VERSION") || return 1
        log "Rolling back to specified version: $target_version"
    fi

    echo "$target_version"
}

# Function to stop current containers
stop_containers() {
    log "Stopping current containers"

    cd "$PROJECT_ROOT" || exit 1

    if ! docker-compose -f docker-compose.yml down; then
        log_error "Failed to stop containers"
        return 1
    fi

    log_success "Containers stopped"
}

# Function to rollback Docker images
rollback_docker_images() {
    local target_version="$1"
    log "Rolling back Docker images to version: $target_version"

    local registry="${REGISTRY:-ghcr.io}"
    local image_name="${IMAGE_NAME:-simplyfi-por-platform}"

    log "Pulling backend image: $registry/$image_name:${target_version}-backend"
    if ! docker pull "$registry/$image_name:${target_version}-backend"; then
        log_error "Failed to pull previous backend image"
        return 1
    fi

    log "Pulling frontend image: $registry/$image_name:${target_version}-frontend"
    if ! docker pull "$registry/$image_name:${target_version}-frontend"; then
        log_error "Failed to pull previous frontend image"
        return 1
    fi

    log_success "Docker images rolled back successfully"
}

# Function to rollback database
rollback_database() {
    log "Rolling back database to previous state"

    local rollback_steps="${1:-1}"

    # Set environment variables for alembic
    export DATABASE_URL="${DATABASE_URL}"

    cd "$PROJECT_ROOT/backend" || exit 1

    log "Rolling back $rollback_steps database migration(s)"
    for ((i = 0; i < rollback_steps; i++)); do
        if ! alembic downgrade -1; then
            log_error "Database rollback failed at step $((i + 1))"
            return 1
        fi
    done

    log_success "Database rollback completed"
}

# Function to start containers with previous version
start_containers() {
    local target_version="$1"
    log "Starting containers with version: $target_version"

    cd "$PROJECT_ROOT" || exit 1

    # Set environment variables
    export DEPLOYMENT_TAG="$target_version"
    export ENVIRONMENT="$ENVIRONMENT"

    if ! docker-compose -f docker-compose.yml up -d; then
        log_error "Failed to start containers"
        return 1
    fi

    log "Waiting for containers to be ready"
    sleep 10

    log_success "Containers started"
}

# Function to perform health checks
health_check() {
    log "Performing health checks"

    local api_url="${API_URL:-http://localhost:8000}"
    local health_endpoint="$api_url/health"
    local max_attempts=$((HEALTH_CHECK_TIMEOUT / HEALTH_CHECK_INTERVAL))
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$health_endpoint" > /dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi

        attempt=$((attempt + 1))
        if [ $attempt -lt $max_attempts ]; then
            sleep "$HEALTH_CHECK_INTERVAL"
        fi
    done

    log_error "Health check failed after $HEALTH_CHECK_TIMEOUT seconds"
    return 1
}

# Function to verify rollback
verify_rollback() {
    local target_version="$1"
    log "Verifying rollback to version: $target_version"

    # Check if containers are running
    log "Checking container status"
    local running_containers=$(docker-compose -f "$PROJECT_ROOT/docker-compose.yml" ps | grep -c "Up" || true)

    if [ "$running_containers" -lt 3 ]; then
        log_warning "Expected at least 3 running containers, found $running_containers"
        return 1
    fi

    log_success "Container status verified"

    # Verify API version
    log "Verifying API version"
    if curl -s "${API_URL:-http://localhost:8000}/api/version" 2>/dev/null | grep -q "$target_version" 2>/dev/null || true; then
        log_success "API version verified"
    else
        log_warning "Could not verify API version (may be non-critical)"
    fi

    return 0
}

# Function to update deployment history
update_deployment_history() {
    local target_version="$1"
    log "Updating deployment history"

    local history_file="/var/lib/simplyfi-por/$ENVIRONMENT/deployment-history.txt"
    mkdir -p "$(dirname "$history_file")"

    # Add current version to history
    echo "$target_version $(date +'%Y-%m-%d %H:%M:%S') rollback" >> "$history_file"

    log_success "Deployment history updated"
}

# Function to notify about rollback
notify_rollback() {
    local status="$1"
    local target_version="$2"
    local message="$3"

    # Slack notification
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        local color="good"
        if [ "$status" == "failure" ]; then
            color="danger"
        fi

        curl -X POST "${SLACK_WEBHOOK_URL}" -H 'Content-type: application/json' \
            --data "{
                \"attachments\": [
                    {
                        \"color\": \"$color\",
                        \"title\": \"SimplyFI PoR Rollback - $ENVIRONMENT\",
                        \"text\": \"$message\",
                        \"fields\": [
                            {
                                \"title\": \"Status\",
                                \"value\": \"$status\",
                                \"short\": true
                            },
                            {
                                \"title\": \"Target Version\",
                                \"value\": \"$target_version\",
                                \"short\": true
                            },
                            {
                                \"title\": \"Environment\",
                                \"value\": \"$ENVIRONMENT\",
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

# Main rollback flow
main() {
    log "====== SimplyFI PoR Platform Rollback Started ======"
    log "Environment: $ENVIRONMENT"
    log "Target Version: $TARGET_VERSION"
    log "Log file: $LOG_FILE"

    local target_version

    # Determine target version
    if ! target_version=$(determine_target_version); then
        log_error "====== Rollback Failed ======"
        notify_rollback "failure" "$TARGET_VERSION" "Could not determine rollback target version"
        return 1
    fi

    # Execute rollback steps
    if validate_environment && \
       load_deployment_config && \
       stop_containers && \
       rollback_docker_images "$target_version" && \
       rollback_database 1 && \
       start_containers "$target_version" && \
       health_check && \
       verify_rollback "$target_version" && \
       update_deployment_history "$target_version"; then

        log_success "====== Rollback Completed Successfully ======"
        log "Rolled back to version: $target_version"
        notify_rollback "success" "$target_version" "SimplyFI PoR Platform successfully rolled back to $target_version on $ENVIRONMENT"
        return 0
    else
        log_error "====== Rollback Failed ======"
        notify_rollback "failure" "$target_version" "SimplyFI PoR Platform rollback to $target_version on $ENVIRONMENT failed. Check logs: $LOG_FILE"
        log_error "Manual intervention may be required. Contact the operations team."
        return 1
    fi
}

# Execute main
main "$@"
