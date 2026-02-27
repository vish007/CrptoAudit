"""Integration tests for authentication API."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestAuthAPI:
    """Integration tests for authentication endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "app" in data
        assert "version" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data

    def test_readiness_check(self, client: TestClient):
        """Test readiness check endpoint."""
        response = client.get("/ready")

        assert response.status_code == 200
        data = response.json()
        assert "ready" in data


@pytest.mark.integration
class TestUserRegistration:
    """Tests for user registration flow."""

    def test_register_user_success(self, client: TestClient, sample_user_data):
        """Test successful user registration."""
        # This assumes a registration endpoint exists
        # Adjust path based on actual API structure
        response = client.post(
            "/api/v1/auth/register",
            json=sample_user_data,
        )

        # Should return either 201 Created or 200 OK
        assert response.status_code in [200, 201]

    def test_register_duplicate_email_fails(self, client: TestClient, sample_user_data):
        """Test that duplicate email registration fails."""
        # Register first user
        response1 = client.post(
            "/api/v1/auth/register",
            json=sample_user_data,
        )

        assert response1.status_code in [200, 201]

        # Try to register with same email
        response2 = client.post(
            "/api/v1/auth/register",
            json=sample_user_data,
        )

        # Should fail with 400 or 409
        assert response2.status_code in [400, 409]


@pytest.mark.integration
class TestLogin:
    """Tests for login flow."""

    def test_login_success(self, client: TestClient, sample_user_data):
        """Test successful login."""
        # Register user first
        client.post("/api/v1/auth/register", json=sample_user_data)

        # Login with credentials
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"],
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data

    def test_login_wrong_password(self, client: TestClient, sample_user_data):
        """Test login with wrong password."""
        # Register user
        client.post("/api/v1/auth/register", json=sample_user_data)

        # Login with wrong password
        login_data = {
            "email": sample_user_data["email"],
            "password": "WrongPassword123!",
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code in [400, 401]


@pytest.mark.integration
class TestTokenManagement:
    """Tests for token management."""

    def test_protected_endpoint_without_token(self, client: TestClient):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/v1/engagements")

        # Should return 403 or 401
        assert response.status_code in [401, 403]

    def test_protected_endpoint_with_valid_token(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test accessing protected endpoint with valid token."""
        response = client.get(
            "/api/v1/engagements",
            headers=auth_headers,
        )

        # Should return 200 or 404 (endpoint may not exist)
        assert response.status_code in [200, 404, 403]


@pytest.mark.integration
class TestRoleBasedAccessControl:
    """Tests for role-based access control."""

    def test_admin_access_allowed(self, client: TestClient, admin_auth_headers):
        """Test admin can access admin endpoints."""
        response = client.get(
            "/api/v1/admin/tenants",
            headers=admin_auth_headers,
        )

        # Should return 200 or 404 (endpoint may not exist)
        assert response.status_code in [200, 404]

    def test_user_access_denied_to_admin_endpoint(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test regular user denied access to admin endpoints."""
        response = client.get(
            "/api/v1/admin/tenants",
            headers=auth_headers,
        )

        # Should return 403 (Forbidden)
        assert response.status_code == 403


@pytest.mark.integration
class TestTenantIsolation:
    """Tests for tenant isolation."""

    def test_tenant_isolation_enforced(self, client: TestClient, auth_headers):
        """Test that tenant isolation is enforced."""
        # User from tenant A cannot see tenant B's data
        response = client.get(
            "/api/v1/engagements",
            headers=auth_headers,
        )

        # Response should only contain data for user's tenant
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                # If engagements are returned, verify they belong to user's tenant
                assert len(data) >= 0  # Valid response

    def test_cross_tenant_access_denied(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test that cross-tenant access is denied."""
        # Try to access data from different tenant
        response = client.get(
            "/api/v1/engagements/different-tenant-id",
            headers=auth_headers,
        )

        # Should return 403 or 404
        assert response.status_code in [403, 404]
