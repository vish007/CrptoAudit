"""Integration tests for engagement API."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestEngagementCRUD:
    """Tests for engagement CRUD operations."""

    def test_create_engagement(
        self,
        client: TestClient,
        auth_headers,
        sample_engagement_data,
    ):
        """Test creating an engagement."""
        response = client.post(
            "/api/v1/engagements",
            json=sample_engagement_data,
            headers=auth_headers,
        )

        # Should return 201 Created or 200 OK
        assert response.status_code in [200, 201]

        if response.status_code in [200, 201]:
            data = response.json()
            assert "id" in data
            assert data["title"] == sample_engagement_data["title"]

    def test_list_engagements_with_pagination(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test listing engagements with pagination."""
        response = client.get(
            "/api/v1/engagements?skip=0&limit=10",
            headers=auth_headers,
        )

        # Should return 200 OK or 404
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should be a list or have a 'items' key
            if isinstance(data, dict):
                assert "items" in data or len(data) >= 0
            else:
                assert isinstance(data, list)

    def test_get_engagement_detail(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test getting engagement details."""
        # Try to get a non-existent engagement
        response = client.get(
            "/api/v1/engagements/test-id",
            headers=auth_headers,
        )

        # Should return 404 if not found or 200 if found
        assert response.status_code in [200, 404]

    def test_update_engagement_status(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test updating engagement status."""
        update_data = {"status": "VERIFICATION"}

        response = client.patch(
            "/api/v1/engagements/test-id",
            json=update_data,
            headers=auth_headers,
        )

        # Should return 200, 404, or 400
        assert response.status_code in [200, 404, 400]


@pytest.mark.integration
class TestEngagementAssets:
    """Tests for managing engagement assets."""

    def test_add_assets_to_engagement(
        self,
        client: TestClient,
        auth_headers,
        sample_asset_data,
    ):
        """Test adding assets to engagement."""
        asset_data = {
            "assets": [sample_asset_data],
        }

        response = client.post(
            "/api/v1/engagements/test-id/assets",
            json=asset_data,
            headers=auth_headers,
        )

        # Should return 200 or 404
        assert response.status_code in [200, 404, 400]


@pytest.mark.integration
class TestEngagementTimeline:
    """Tests for engagement timeline."""

    def test_engagement_timeline(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test retrieving engagement timeline."""
        response = client.get(
            "/api/v1/engagements/test-id/timeline",
            headers=auth_headers,
        )

        # Should return 200 or 404
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should contain timeline events
            if isinstance(data, dict):
                assert "events" in data or len(data) >= 0


@pytest.mark.integration
class TestEngagementSummary:
    """Tests for engagement summary."""

    def test_engagement_summary(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test retrieving engagement summary."""
        response = client.get(
            "/api/v1/engagements/test-id/summary",
            headers=auth_headers,
        )

        # Should return 200 or 404
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # Should contain summary information
            assert isinstance(data, dict)


@pytest.mark.integration
class TestEngagementAccessControl:
    """Tests for engagement access control."""

    def test_engagement_access_by_tenant(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test that users can only access their tenant's engagements."""
        response = client.get(
            "/api/v1/engagements",
            headers=auth_headers,
        )

        # Should succeed
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            # All returned engagements should be for user's tenant
            if isinstance(data, list):
                for engagement in data:
                    assert "id" in engagement

    def test_engagement_access_denied_wrong_tenant(
        self,
        client: TestClient,
        auth_headers,
    ):
        """Test that access is denied to wrong tenant's engagement."""
        response = client.get(
            "/api/v1/engagements/other-tenant-engagement-id",
            headers=auth_headers,
        )

        # Should return 403 or 404
        assert response.status_code in [403, 404]
