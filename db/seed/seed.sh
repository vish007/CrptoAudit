#!/bin/bash
#
# SimplyFI PoR Platform Database Seeding Script
# Seeds all required data for development and testing
#

set -e

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-simplyfi_por}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
SEED_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Wait for PostgreSQL to be ready
wait_for_postgres() {
  log_info "Waiting for PostgreSQL to be ready at ${DB_HOST}:${DB_PORT}..."
  max_attempts=30
  attempt=1

  while [ $attempt -le $max_attempts ]; do
    if PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "SELECT 1" > /dev/null 2>&1; then
      log_success "PostgreSQL is ready!"
      return 0
    fi

    echo -n "."
    sleep 1
    attempt=$((attempt + 1))
  done

  log_error "PostgreSQL failed to become ready after $max_attempts attempts"
  return 1
}

# Execute a SQL file
execute_sql_file() {
  local file=$1
  local description=$2

  if [ ! -f "$file" ]; then
    log_error "File not found: $file"
    return 1
  fi

  log_info "Executing: $description"

  if PGPASSWORD=$DB_PASSWORD psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -f "$file" > /tmp/seed_output.log 2>&1; then
    log_success "Completed: $description"
    return 0
  else
    log_error "Failed: $description"
    log_error "Output: $(cat /tmp/seed_output.log)"
    return 1
  fi
}

# Get row count for a table
get_row_count() {
  local table=$1
  PGPASSWORD=$DB_PASSWORD psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -t -c "SELECT COUNT(*) FROM $table;" 2>/dev/null | tr -d ' '
}

# Validate seeded data
validate_seed_data() {
  log_info "Validating seeded data..."

  declare -A expected_counts
  expected_counts["tenants"]=6
  expected_counts["users"]=80
  expected_counts["roles"]=7
  expected_counts["crypto_assets"]=130
  expected_counts["engagements"]=5
  expected_counts["wallet_addresses"]=40
  expected_counts["customer_liabilities"]=250
  expected_counts["merkle_trees"]=1
  expected_counts["merkle_proofs"]=10
  expected_counts["reconciliation_records"]=31
  expected_counts["audit_logs"]=20

  local all_valid=true

  for table in "${!expected_counts[@]}"; do
    local expected=${expected_counts[$table]}
    local actual=$(get_row_count "$table")

    if [ "$actual" -ge "$expected" ]; then
      log_success "$table: $actual rows (expected >= $expected)"
    else
      log_warning "$table: $actual rows (expected >= $expected)"
      all_valid=false
    fi
  done

  if [ "$all_valid" = true ]; then
    log_success "All validation checks passed!"
    return 0
  else
    log_warning "Some validation checks had lower counts than expected"
    return 0
  fi
}

# Print summary
print_summary() {
  log_info "===== SEED DATA SUMMARY ====="

  local total_tables=$(PGPASSWORD=$DB_PASSWORD psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null)

  log_info "Database: $DB_NAME"
  log_info "Total tables: $total_tables"

  local tables=(
    "tenants"
    "users"
    "roles"
    "permissions"
    "user_roles"
    "role_permissions"
    "crypto_assets"
    "engagements"
    "wallet_addresses"
    "customer_liabilities"
    "merkle_trees"
    "merkle_proofs"
    "reconciliation_records"
    "audit_logs"
  )

  echo ""
  printf "${YELLOW}%-30s %s${NC}\n" "Table" "Rows"
  printf "%-30s %s\n" "----" "----"

  for table in "${tables[@]}"; do
    local count=$(get_row_count "$table")
    printf "%-30s %s\n" "$table" "$count"
  done

  echo ""
  log_success "Seeding completed successfully!"
}

# Main execution
main() {
  log_info "SimplyFI PoR Platform Database Seeding"
  log_info "Started at $(date)"
  echo ""

  # Wait for PostgreSQL
  if ! wait_for_postgres; then
    exit 1
  fi

  # Execute seed files in order
  echo ""
  log_info "===== EXECUTING SEED FILES ====="
  echo ""

  execute_sql_file "$SEED_DIR/01_tenants.sql" "Tenants" || exit 1
  execute_sql_file "$SEED_DIR/02_users.sql" "Users" || exit 1
  execute_sql_file "$SEED_DIR/03_roles_permissions.sql" "Roles and Permissions" || exit 1
  execute_sql_file "$SEED_DIR/04_crypto_assets.sql" "Crypto Assets (130 assets)" || exit 1
  execute_sql_file "$SEED_DIR/05_engagements.sql" "Engagements" || exit 1
  execute_sql_file "$SEED_DIR/06_wallets_balances.sql" "Wallet Addresses and Balances" || exit 1
  execute_sql_file "$SEED_DIR/07_customer_liabilities.sql" "Customer Liabilities (250+ records)" || exit 1
  execute_sql_file "$SEED_DIR/08_merkle_trees.sql" "Merkle Trees and Proofs" || exit 1
  execute_sql_file "$SEED_DIR/09_reconciliation.sql" "Reconciliation Records (30 days)" || exit 1
  execute_sql_file "$SEED_DIR/10_transactions_audit.sql" "Audit Logs" || exit 1

  # Validate and print summary
  echo ""
  validate_seed_data
  echo ""
  print_summary
  echo ""
  log_info "Completed at $(date)"
}

# Trap errors
trap 'log_error "Script failed at line $LINENO"' ERR

# Run main function
main "$@"
