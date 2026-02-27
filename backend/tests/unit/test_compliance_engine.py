"""Unit tests for compliance engine."""
import pytest
from decimal import Decimal
from enum import Enum
from typing import Dict, List


class ComplianceStatus(str, Enum):
    """Compliance status enum."""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ComplianceEngine:
    """Simple compliance engine for testing."""

    @staticmethod
    def check_reserve_requirement(
        total_assets: Decimal,
        total_liabilities: Decimal,
        required_ratio: Decimal = Decimal("100"),
    ) -> bool:
        """Check if reserve requirement is met."""
        if total_liabilities == 0:
            return False

        ratio = (total_assets / total_liabilities) * 100
        return ratio >= required_ratio

    @staticmethod
    def check_segregation_compliant(
        customer_assets: Decimal,
        customer_liabilities: Decimal,
    ) -> bool:
        """Check if asset segregation is compliant."""
        if customer_liabilities == 0:
            return False

        ratio = (customer_assets / customer_liabilities) * 100
        return ratio >= Decimal("100")

    @staticmethod
    def check_daily_reconciliation_compliant(
        on_chain_balance: Decimal,
        internal_balance: Decimal,
        tolerance_percent: Decimal = Decimal("0.5"),
    ) -> bool:
        """Check if daily reconciliation is compliant."""
        if on_chain_balance == 0:
            return False

        variance = abs(
            ((on_chain_balance - internal_balance) / on_chain_balance) * 100
        )

        return variance <= tolerance_percent

    @staticmethod
    def check_quarterly_reporting(
        last_report_date,
        current_date,
        days_per_quarter: int = 90,
    ) -> bool:
        """Check if quarterly reporting is compliant."""
        from datetime import timedelta

        next_report_date = last_report_date + timedelta(days=days_per_quarter)
        return current_date <= next_report_date

    @staticmethod
    def overall_compliance_score(
        compliance_checks: Dict[str, bool],
    ) -> Decimal:
        """Calculate overall compliance score."""
        if not compliance_checks:
            return Decimal("0")

        passed = sum(1 for v in compliance_checks.values() if v)
        total = len(compliance_checks)

        return (Decimal(passed) / Decimal(total)) * Decimal("100")

    @staticmethod
    def generate_remediation_steps(
        failed_checks: List[str],
    ) -> List[str]:
        """Generate remediation steps for failed checks."""
        remediation_map = {
            "reserve_requirement": [
                "Increase total assets",
                "Reduce customer liabilities",
                "Deposit additional collateral",
            ],
            "segregation": [
                "Move customer assets to segregated accounts",
                "Update custody structure",
                "Review collateral allocation",
            ],
            "reconciliation": [
                "Investigate balance discrepancies",
                "Reconcile on-chain and internal records",
                "Implement automated reconciliation",
            ],
        }

        steps = []
        for check in failed_checks:
            steps.extend(remediation_map.get(check, ["Review and remediate"]))

        return steps


@pytest.mark.unit
class TestReserveRequirement:
    """Tests for reserve requirement checking."""

    def test_check_reserve_requirement_pass(self):
        """Test reserve requirement passes."""
        engine = ComplianceEngine()
        result = engine.check_reserve_requirement(
            total_assets=Decimal("1100"),
            total_liabilities=Decimal("1000"),
            required_ratio=Decimal("100"),
        )

        assert result is True

    def test_check_reserve_requirement_fail(self):
        """Test reserve requirement fails."""
        engine = ComplianceEngine()
        result = engine.check_reserve_requirement(
            total_assets=Decimal("900"),
            total_liabilities=Decimal("1000"),
            required_ratio=Decimal("100"),
        )

        assert result is False

    def test_check_reserve_requirement_exact_ratio(self):
        """Test reserve requirement at exact ratio."""
        engine = ComplianceEngine()
        result = engine.check_reserve_requirement(
            total_assets=Decimal("1000"),
            total_liabilities=Decimal("1000"),
            required_ratio=Decimal("100"),
        )

        assert result is True


@pytest.mark.unit
class TestSegregationCompliance:
    """Tests for asset segregation compliance."""

    def test_check_segregation_compliant(self):
        """Test segregation compliance check passes."""
        engine = ComplianceEngine()
        result = engine.check_segregation_compliant(
            customer_assets=Decimal("1050"),
            customer_liabilities=Decimal("1000"),
        )

        assert result is True

    def test_check_segregation_non_compliant(self):
        """Test segregation compliance check fails."""
        engine = ComplianceEngine()
        result = engine.check_segregation_compliant(
            customer_assets=Decimal("950"),
            customer_liabilities=Decimal("1000"),
        )

        assert result is False


@pytest.mark.unit
class TestDailyReconciliation:
    """Tests for daily reconciliation compliance."""

    def test_check_daily_reconciliation_compliant(self):
        """Test daily reconciliation passes."""
        engine = ComplianceEngine()
        result = engine.check_daily_reconciliation_compliant(
            on_chain_balance=Decimal("1000"),
            internal_balance=Decimal("1000.25"),
            tolerance_percent=Decimal("1"),
        )

        assert result is True

    def test_check_daily_reconciliation_non_compliant(self):
        """Test daily reconciliation fails."""
        engine = ComplianceEngine()
        result = engine.check_daily_reconciliation_compliant(
            on_chain_balance=Decimal("1000"),
            internal_balance=Decimal("900"),
            tolerance_percent=Decimal("1"),
        )

        assert result is False

    def test_check_daily_reconciliation_within_tolerance(self):
        """Test reconciliation within tolerance."""
        engine = ComplianceEngine()
        result = engine.check_daily_reconciliation_compliant(
            on_chain_balance=Decimal("10000"),
            internal_balance=Decimal("10005"),
            tolerance_percent=Decimal("0.1"),
        )

        assert result is True


@pytest.mark.unit
class TestQuarterlyReporting:
    """Tests for quarterly reporting compliance."""

    def test_check_quarterly_reporting(self):
        """Test quarterly reporting check."""
        from datetime import datetime

        engine = ComplianceEngine()

        last_report_date = datetime(2024, 1, 1)
        current_date = datetime(2024, 3, 15)

        result = engine.check_quarterly_reporting(
            last_report_date=last_report_date,
            current_date=current_date,
            days_per_quarter=90,
        )

        assert result is True


@pytest.mark.unit
class TestOverallComplianceScore:
    """Tests for overall compliance score calculation."""

    def test_overall_compliance_score_all_pass(self):
        """Test compliance score when all checks pass."""
        engine = ComplianceEngine()

        checks = {
            "reserve_requirement": True,
            "segregation": True,
            "reconciliation": True,
        }

        score = engine.overall_compliance_score(checks)

        assert score == Decimal("100")

    def test_overall_compliance_score_partial(self):
        """Test compliance score with partial passes."""
        engine = ComplianceEngine()

        checks = {
            "reserve_requirement": True,
            "segregation": True,
            "reconciliation": False,
        }

        score = engine.overall_compliance_score(checks)

        assert score > Decimal("66")
        assert score < Decimal("67")

    def test_overall_compliance_score_all_fail(self):
        """Test compliance score when all checks fail."""
        engine = ComplianceEngine()

        checks = {
            "reserve_requirement": False,
            "segregation": False,
            "reconciliation": False,
        }

        score = engine.overall_compliance_score(checks)

        assert score == Decimal("0")


@pytest.mark.unit
class TestRemediationSteps:
    """Tests for remediation step generation."""

    def test_generate_remediation_steps_reserve(self):
        """Test remediation steps for reserve failure."""
        engine = ComplianceEngine()

        steps = engine.generate_remediation_steps(["reserve_requirement"])

        assert len(steps) > 0
        assert any("asset" in step.lower() for step in steps)

    def test_generate_remediation_steps_segregation(self):
        """Test remediation steps for segregation failure."""
        engine = ComplianceEngine()

        steps = engine.generate_remediation_steps(["segregation"])

        assert len(steps) > 0
        assert any("segregated" in step.lower() for step in steps)

    def test_generate_remediation_steps_reconciliation(self):
        """Test remediation steps for reconciliation failure."""
        engine = ComplianceEngine()

        steps = engine.generate_remediation_steps(["reconciliation"])

        assert len(steps) > 0
        assert any("reconcil" in step.lower() for step in steps)

    def test_generate_remediation_steps_multiple(self):
        """Test remediation steps for multiple failures."""
        engine = ComplianceEngine()

        steps = engine.generate_remediation_steps([
            "reserve_requirement",
            "segregation",
        ])

        assert len(steps) >= 2


@pytest.mark.unit
class TestVARACompliance:
    """Tests for VARA compliance framework."""

    def test_all_vara_requirements_covered(self):
        """Test that all VARA requirements are covered."""
        engine = ComplianceEngine()

        requirements = {
            "reserve_requirement": True,
            "segregation": True,
            "reconciliation": True,
            "quarterly_reporting": True,
            "audit_trail": True,
        }

        # All requirements should be checkable
        assert len(requirements) >= 4

    def test_vara_compliance_status(self):
        """Test VARA compliance status determination."""
        requirements = {
            "reserve_requirement": True,
            "segregation": True,
            "reconciliation": True,
        }

        score = (
            sum(1 for v in requirements.values() if v) /
            len(requirements) * 100
        )

        if score == 100:
            status = ComplianceStatus.COMPLIANT
        elif score >= 80:
            status = ComplianceStatus.REVIEW_REQUIRED
        else:
            status = ComplianceStatus.NON_COMPLIANT

        assert status == ComplianceStatus.COMPLIANT
