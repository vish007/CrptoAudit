#!/bin/bash
# Comprehensive test runner for SimplyFI PoR Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COVERAGE_MIN=80
FAILED_TESTS=0

# Helper functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if pytest is installed
check_pytest() {
    if ! command -v pytest &> /dev/null; then
        print_error "pytest not found. Installing dependencies..."
        pip install -r requirements-test.txt
    fi
}

# Run unit tests
run_unit_tests() {
    print_header "Running Unit Tests"

    if pytest tests/unit -m unit \
        --cov=app \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-fail-under=$COVERAGE_MIN \
        -v; then
        print_success "Unit tests passed"
    else
        print_error "Unit tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Run integration tests
run_integration_tests() {
    print_header "Running Integration Tests"

    if pytest tests/integration -m integration \
        --tb=short \
        -v; then
        print_success "Integration tests passed"
    else
        print_error "Integration tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Run E2E tests
run_e2e_tests() {
    print_header "Running E2E Tests"

    if pytest tests/e2e -m e2e \
        --tb=short \
        -v; then
        print_success "E2E tests passed"
    else
        print_error "E2E tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Run all tests with coverage
run_all_tests() {
    print_header "Running All Tests with Coverage"

    if pytest \
        --cov=app \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=xml \
        --cov-fail-under=$COVERAGE_MIN \
        -v \
        --tb=short; then
        print_success "All tests passed"
    else
        print_error "Some tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Run tests matching pattern
run_tests_matching() {
    local pattern=$1
    print_header "Running tests matching: $pattern"

    if pytest -k "$pattern" -v --tb=short; then
        print_success "Tests matching '$pattern' passed"
    else
        print_error "Tests matching '$pattern' failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Generate coverage report
generate_coverage_report() {
    print_header "Coverage Report"

    if [ -f "htmlcov/index.html" ]; then
        print_success "Coverage report generated: htmlcov/index.html"
    fi
}

# Run linting
run_linting() {
    print_header "Running Linting"

    if command -v flake8 &> /dev/null; then
        if flake8 app tests --max-line-length=100; then
            print_success "Linting passed"
        else
            print_warning "Linting issues found"
        fi
    fi

    if command -v black &> /dev/null; then
        if black --check app tests; then
            print_success "Code formatting check passed"
        else
            print_warning "Code formatting issues found"
            black app tests
        fi
    fi
}

# Main test runner
main() {
    print_header "SimplyFI PoR Platform - Test Suite"

    check_pytest

    # Parse command line arguments
    case "${1:-all}" in
        unit)
            run_unit_tests
            ;;
        integration)
            run_integration_tests
            ;;
        e2e)
            run_e2e_tests
            ;;
        all)
            run_all_tests
            generate_coverage_report
            ;;
        match)
            if [ -z "$2" ]; then
                print_error "Pattern required: $0 match <pattern>"
                exit 1
            fi
            run_tests_matching "$2"
            ;;
        lint)
            run_linting
            ;;
        coverage)
            run_unit_tests
            generate_coverage_report
            ;;
        *)
            echo "Usage: $0 {unit|integration|e2e|all|match <pattern>|lint|coverage}"
            exit 1
            ;;
    esac

    # Print summary
    echo ""
    print_header "Test Summary"

    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "All test suites passed!"
        exit 0
    else
        print_error "$FAILED_TESTS test suite(s) failed"
        exit 1
    fi
}

# Run main function
main "$@"
