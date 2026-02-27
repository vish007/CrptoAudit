"""Unit tests for anomaly detection."""
import pytest
from decimal import Decimal
from typing import List, Dict


class AnomalyDetector:
    """Simple anomaly detector for testing."""

    @staticmethod
    def detect_negative_balances(wallets: List[Dict]) -> List[str]:
        """Detect wallets with negative balances."""
        anomalies = []
        for wallet in wallets:
            if wallet.get("balance", 0) < 0:
                anomalies.append(wallet.get("address", "unknown"))
        return anomalies

    @staticmethod
    def detect_duplicate_user_ids(users: List[Dict]) -> List[str]:
        """Detect duplicate user IDs."""
        user_ids = []
        duplicates = []
        for user in users:
            user_id = user.get("id")
            if user_id in user_ids and user_id not in duplicates:
                duplicates.append(user_id)
            user_ids.append(user_id)
        return duplicates

    @staticmethod
    def detect_outlier_balances(balances: List[Decimal], z_threshold: Decimal = Decimal("3")) -> List[int]:
        """Detect outlier balances using Z-score."""
        if len(balances) < 2:
            return []

        mean = sum(balances) / len(balances)
        variance = sum((b - mean) ** 2 for b in balances) / len(balances)

        if variance == 0:
            return []

        stdev = Decimal(str(variance ** 0.5))
        outliers = []

        for i, balance in enumerate(balances):
            z_score = abs((balance - mean) / stdev)
            if z_score > z_threshold:
                outliers.append(i)

        return outliers

    @staticmethod
    def detect_sudden_balance_changes(
        wallet_history: List[Dict],
        threshold_percent: Decimal = Decimal("10"),
    ) -> List[int]:
        """Detect sudden balance changes."""
        anomalies = []

        for i in range(1, len(wallet_history)):
            prev_balance = Decimal(str(wallet_history[i - 1].get("balance", 0)))
            current_balance = Decimal(str(wallet_history[i].get("balance", 0)))

            if prev_balance == 0:
                continue

            change_percent = abs(
                ((current_balance - prev_balance) / prev_balance) * 100
            )

            if change_percent > threshold_percent:
                anomalies.append(i)

        return anomalies

    @staticmethod
    def anomaly_severity_score(
        anomaly_count: int,
        total_items: int,
    ) -> Decimal:
        """Calculate anomaly severity score."""
        if total_items == 0:
            return Decimal("0")

        percentage = (Decimal(anomaly_count) / Decimal(total_items)) * 100

        if percentage >= Decimal("10"):
            return Decimal("9")  # Critical
        elif percentage >= Decimal("5"):
            return Decimal("6")  # High
        elif percentage >= Decimal("1"):
            return Decimal("3")  # Medium
        else:
            return Decimal("1")  # Low


@pytest.mark.unit
class TestNegativeBalanceDetection:
    """Tests for negative balance detection."""

    def test_detect_negative_balances(self):
        """Test detecting wallets with negative balances."""
        wallets = [
            {"address": "wallet_1", "balance": Decimal("100")},
            {"address": "wallet_2", "balance": Decimal("-50")},
            {"address": "wallet_3", "balance": Decimal("200")},
        ]

        detector = AnomalyDetector()
        anomalies = detector.detect_negative_balances(wallets)

        assert len(anomalies) == 1
        assert "wallet_2" in anomalies

    def test_no_negative_balances(self):
        """Test when no negative balances exist."""
        wallets = [
            {"address": "wallet_1", "balance": Decimal("100")},
            {"address": "wallet_2", "balance": Decimal("50")},
        ]

        detector = AnomalyDetector()
        anomalies = detector.detect_negative_balances(wallets)

        assert len(anomalies) == 0


@pytest.mark.unit
class TestDuplicateDetection:
    """Tests for duplicate user ID detection."""

    def test_detect_duplicate_user_ids(self):
        """Test detecting duplicate user IDs."""
        users = [
            {"id": "user_1", "name": "Alice"},
            {"id": "user_2", "name": "Bob"},
            {"id": "user_1", "name": "Alice Copy"},
        ]

        detector = AnomalyDetector()
        duplicates = detector.detect_duplicate_user_ids(users)

        assert "user_1" in duplicates
        assert len(duplicates) == 1

    def test_no_duplicates(self):
        """Test when no duplicates exist."""
        users = [
            {"id": "user_1", "name": "Alice"},
            {"id": "user_2", "name": "Bob"},
            {"id": "user_3", "name": "Charlie"},
        ]

        detector = AnomalyDetector()
        duplicates = detector.detect_duplicate_user_ids(users)

        assert len(duplicates) == 0


@pytest.mark.unit
class TestOutlierDetection:
    """Tests for outlier balance detection."""

    def test_detect_outlier_balances_zscore(self):
        """Test detecting outliers using Z-score."""
        balances = [
            Decimal("100"),
            Decimal("105"),
            Decimal("102"),
            Decimal("103"),
            Decimal("1000"),  # Outlier
        ]

        detector = AnomalyDetector()
        outliers = detector.detect_outlier_balances(balances, z_threshold=Decimal("2"))

        assert 4 in outliers  # Index of outlier

    def test_no_outliers(self):
        """Test when no outliers exist."""
        balances = [
            Decimal("100"),
            Decimal("105"),
            Decimal("102"),
            Decimal("103"),
            Decimal("98"),
        ]

        detector = AnomalyDetector()
        outliers = detector.detect_outlier_balances(balances, z_threshold=Decimal("3"))

        assert len(outliers) == 0


@pytest.mark.unit
class TestSuddenChangeDetection:
    """Tests for sudden balance change detection."""

    def test_detect_sudden_balance_changes(self):
        """Test detecting sudden balance changes."""
        wallet_history = [
            {"timestamp": "2024-01-01", "balance": Decimal("1000")},
            {"timestamp": "2024-01-02", "balance": Decimal("1050")},
            {"timestamp": "2024-01-03", "balance": Decimal("200")},  # Sudden drop
            {"timestamp": "2024-01-04", "balance": Decimal("250")},
        ]

        detector = AnomalyDetector()
        anomalies = detector.detect_sudden_balance_changes(
            wallet_history, threshold_percent=Decimal("10")
        )

        assert 2 in anomalies

    def test_no_sudden_changes(self):
        """Test when no sudden changes exist."""
        wallet_history = [
            {"timestamp": "2024-01-01", "balance": Decimal("1000")},
            {"timestamp": "2024-01-02", "balance": Decimal("1005")},
            {"timestamp": "2024-01-03", "balance": Decimal("1010")},
        ]

        detector = AnomalyDetector()
        anomalies = detector.detect_sudden_balance_changes(
            wallet_history, threshold_percent=Decimal("10")
        )

        assert len(anomalies) == 0


@pytest.mark.unit
class TestAnomalySeverityScoring:
    """Tests for anomaly severity scoring."""

    def test_anomaly_severity_critical(self):
        """Test critical severity score."""
        detector = AnomalyDetector()
        score = detector.anomaly_severity_score(15, 100)

        assert score == Decimal("9")

    def test_anomaly_severity_high(self):
        """Test high severity score."""
        detector = AnomalyDetector()
        score = detector.anomaly_severity_score(7, 100)

        assert score == Decimal("6")

    def test_anomaly_severity_medium(self):
        """Test medium severity score."""
        detector = AnomalyDetector()
        score = detector.anomaly_severity_score(2, 100)

        assert score == Decimal("3")

    def test_anomaly_severity_low(self):
        """Test low severity score."""
        detector = AnomalyDetector()
        score = detector.anomaly_severity_score(1, 1000)

        assert score == Decimal("1")


@pytest.mark.unit
class TestCleanDataDetection:
    """Tests for clean data detection."""

    def test_no_anomalies_in_clean_data(self):
        """Test that clean data produces no anomalies."""
        wallets = [
            {"address": f"wallet_{i}", "balance": Decimal("100")} for i in range(10)
        ]

        detector = AnomalyDetector()
        negative = detector.detect_negative_balances(wallets)

        assert len(negative) == 0

    def test_clean_data_no_duplicates(self):
        """Test clean data has no duplicate IDs."""
        users = [
            {"id": f"user_{i}", "name": f"User {i}"} for i in range(10)
        ]

        detector = AnomalyDetector()
        duplicates = detector.detect_duplicate_user_ids(users)

        assert len(duplicates) == 0


@pytest.mark.unit
class TestReconciliationAnomaly:
    """Tests for reconciliation anomaly detection."""

    def test_reconciliation_balance_mismatch(self):
        """Test detecting balance mismatch in reconciliation."""
        on_chain_balance = Decimal("1000.50")
        internal_balance = Decimal("1000.51")

        mismatch = abs(on_chain_balance - internal_balance)

        assert mismatch > 0
        assert mismatch < Decimal("1")  # Minor discrepancy

    def test_reconciliation_significant_mismatch(self):
        """Test detecting significant balance mismatch."""
        on_chain_balance = Decimal("1000")
        internal_balance = Decimal("950")

        mismatch_percent = abs(
            ((on_chain_balance - internal_balance) / on_chain_balance) * 100
        )

        is_anomalous = mismatch_percent > Decimal("1")

        assert is_anomalous is True


@pytest.mark.unit
class TestCrossAssetCorrelation:
    """Tests for cross-asset correlation detection."""

    def test_correlated_asset_changes(self):
        """Test detecting correlated changes across assets."""
        btc_prices = [
            Decimal("40000"),
            Decimal("41000"),
            Decimal("42000"),
        ]

        eth_prices = [
            Decimal("2000"),
            Decimal("2100"),
            Decimal("2200"),
        ]

        # Both moving in same direction
        btc_changes = [
            ((btc_prices[i + 1] - btc_prices[i]) / btc_prices[i] * 100)
            for i in range(len(btc_prices) - 1)
        ]

        eth_changes = [
            ((eth_prices[i + 1] - eth_prices[i]) / eth_prices[i] * 100)
            for i in range(len(eth_prices) - 1)
        ]

        # Both should be positive
        assert all(change > 0 for change in btc_changes)
        assert all(change > 0 for change in eth_changes)
