"""E2E test configuration."""
import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def e2e_client():
    """Create E2E test client."""
    from app.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
def e2e_base_url():
    """Get base URL for E2E tests."""
    return os.getenv("E2E_BASE_URL", "http://localhost:8000")


@pytest.fixture
def e2e_user_creds():
    """Get E2E test user credentials."""
    return {
        "email": os.getenv("E2E_USER_EMAIL", "test@example.com"),
        "password": os.getenv("E2E_USER_PASSWORD", "TestPassword123!"),
    }


@pytest.fixture
def auth_token(e2e_client, e2e_user_creds):
    """Get authentication token for E2E tests."""
    response = e2e_client.post(
        "/api/v1/auth/login",
        json={
            "email": e2e_user_creds["email"],
            "password": e2e_user_creds["password"],
        },
    )

    if response.status_code == 200:
        return response.json().get("access_token")

    return None


@pytest.fixture
def e2e_cleanup():
    """Cleanup fixture for E2E tests."""
    cleanup_items = []

    def add_cleanup(item):
        cleanup_items.append(item)
        return item

    yield add_cleanup

    # Cleanup code here
    for item in cleanup_items:
        pass  # Perform cleanup


@pytest.fixture
def e2e_test_data_setup(e2e_client, auth_token):
    """Setup test data for E2E tests."""
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

    return {
        "client": e2e_client,
        "headers": headers,
        "tenant_id": None,
        "engagement_id": None,
    }
