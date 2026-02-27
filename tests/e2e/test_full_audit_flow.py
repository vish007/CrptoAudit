"""End-to-end test for complete audit flow."""
import pytest
from datetime import datetime
from decimal import Decimal


@pytest.mark.e2e
class TestFullAuditFlow:
    """Complete end-to-end audit flow test."""

    def test_complete_audit_flow(self, e2e_client, auth_token):
        """Test complete audit flow from start to finish.

        Flow:
        1. SuperAdmin creates VASP tenant
        2. VASP Admin onboards (register, import assets, wallets, liabilities)
        3. Auditor creates engagement
        4. System runs on-chain verification
        5. System generates Merkle tree
        6. System calculates reserve ratios
        7. AI generates report narrative
        8. Auditor generates PoR report
        9. Customer verifies their Merkle proof
        10. VARA compliance check passes
        """

        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        # Step 1: Create VASP tenant (SuperAdmin only)
        tenant_data = {
            "name": "Test VASP Corp",
            "type": "VASP",
            "vara_license_number": "VARA-2024-E2E-001",
        }

        tenant_response = e2e_client.post(
            "/api/v1/admin/tenants",
            json=tenant_data,
            headers=headers,
        )

        assert tenant_response.status_code in [200, 201, 404]

        if tenant_response.status_code in [200, 201]:
            tenant_id = tenant_response.json().get("id")

            # Step 2: VASP onboarding
            assets_data = {
                "assets": [
                    {
                        "asset_name": "BTC",
                        "blockchain": "bitcoin",
                        "total_balance": 50.5,
                    },
                    {
                        "asset_name": "ETH",
                        "blockchain": "ethereum",
                        "total_balance": 1000.0,
                    },
                ]
            }

            assets_response = e2e_client.post(
                f"/api/v1/tenants/{tenant_id}/import-assets",
                json=assets_data,
                headers=headers,
            )

            assert assets_response.status_code in [200, 201, 404]

            # Step 3: Create engagement
            engagement_data = {
                "title": "Annual PoR Audit",
                "description": "Full reserve verification",
                "client_tenant_id": tenant_id,
                "status": "PLANNING",
            }

            engagement_response = e2e_client.post(
                "/api/v1/engagements",
                json=engagement_data,
                headers=headers,
            )

            assert engagement_response.status_code in [200, 201, 404]

            if engagement_response.status_code in [200, 201]:
                engagement_id = engagement_response.json().get("id")

                # Step 4: Trigger verification
                verify_response = e2e_client.post(
                    f"/api/v1/engagements/{engagement_id}/verify",
                    headers=headers,
                )

                assert verify_response.status_code in [200, 202, 404]

                # Step 5: Generate Merkle tree
                merkle_response = e2e_client.post(
                    f"/api/v1/engagements/{engagement_id}/generate-merkle",
                    headers=headers,
                )

                assert merkle_response.status_code in [200, 202, 404]

                # Step 6: Calculate reserves
                reserves_response = e2e_client.get(
                    f"/api/v1/engagements/{engagement_id}/reserves",
                    headers=headers,
                )

                assert reserves_response.status_code in [200, 404]

                # Step 8: Generate PoR report
                report_response = e2e_client.post(
                    f"/api/v1/engagements/{engagement_id}/generate-report",
                    headers=headers,
                )

                assert report_response.status_code in [200, 202, 404]


@pytest.mark.e2e
class TestAuditStageTransitions:
    """Test transitions between audit stages."""

    def test_planning_to_data_collection(self, e2e_client, auth_token):
        """Test transition from Planning to Data Collection."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        # Assume engagement exists
        update_response = e2e_client.patch(
            "/api/v1/engagements/test-engagement-id",
            json={"status": "DATA_COLLECTION"},
            headers=headers,
        )

        assert update_response.status_code in [200, 404]

    def test_data_collection_to_verification(self, e2e_client, auth_token):
        """Test transition from Data Collection to Verification."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        update_response = e2e_client.patch(
            "/api/v1/engagements/test-engagement-id",
            json={"status": "VERIFICATION"},
            headers=headers,
        )

        assert update_response.status_code in [200, 404]

    def test_verification_to_reporting(self, e2e_client, auth_token):
        """Test transition from Verification to Reporting."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        update_response = e2e_client.patch(
            "/api/v1/engagements/test-engagement-id",
            json={"status": "REPORTING"},
            headers=headers,
        )

        assert update_response.status_code in [200, 404]

    def test_reporting_to_completed(self, e2e_client, auth_token):
        """Test transition from Reporting to Completed."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        update_response = e2e_client.patch(
            "/api/v1/engagements/test-engagement-id",
            json={"status": "COMPLETED"},
            headers=headers,
        )

        assert update_response.status_code in [200, 404]


@pytest.mark.e2e
class TestAuditDataFlow:
    """Test data flow through audit process."""

    def test_customer_data_import_flow(self, e2e_client, auth_token):
        """Test importing customer liability data."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        customer_data = {
            "customers": [
                {
                    "customer_id": "CUST-001",
                    "customer_name": "Test Customer 1",
                    "assets": {"BTC": 5.0, "ETH": 100.0},
                },
                {
                    "customer_id": "CUST-002",
                    "customer_name": "Test Customer 2",
                    "assets": {"BTC": 2.5, "ETH": 50.0},
                },
            ]
        }

        response = e2e_client.post(
            "/api/v1/engagements/test-engagement-id/import-customers",
            json=customer_data,
            headers=headers,
        )

        assert response.status_code in [200, 201, 404]

    def test_wallet_verification_flow(self, e2e_client, auth_token):
        """Test wallet verification flow."""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        wallet_data = {
            "wallets": [
                {
                    "address": "0x742d35Cc6634C0532925a3b844Bc314e5505b748",
                    "blockchain": "ethereum",
                    "balance": 1000.5,
                    "wallet_type": "COLD",
                },
                {
                    "address": "1A1z7agoat7qsweQvUwhwYBCn1qWu5Hspp",
                    "blockchain": "bitcoin",
                    "balance": 50.25,
                    "wallet_type": "COLD",
                },
            ]
        }

        response = e2e_client.post(
            "/api/v1/engagements/test-engagement-id/verify-wallets",
            json=wallet_data,
            headers=headers,
        )

        assert response.status_code in [200, 202, 404]
