"""Statistical anomaly detection for PoR platform."""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Tuple
import statistics

logger = logging.getLogger(__name__)


class AnomalySeverity(str, Enum):
    """Anomaly severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Anomaly:
    """Detected anomaly."""
    type: str
    severity: AnomalySeverity
    asset: Optional[str]
    description: str
    value: Optional[float]
    threshold: Optional[float]
    z_score: Optional[float] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class AnomalyDetector:
    """Statistical anomaly detection service."""

    # Z-score thresholds for different severity levels
    Z_SCORE_WARNING = Decimal("2.0")  # 95% confidence
    Z_SCORE_CRITICAL = Decimal("3.0")  # 99.7% confidence

    # Change percentage thresholds
    CHANGE_WARNING_PERCENT = Decimal("10")  # 10% change
    CHANGE_CRITICAL_PERCENT = Decimal("25")  # 25% change

    def __init__(self):
        """Initialize anomaly detector."""
        self.logger = logging.getLogger(self.__class__.__name__)

    async def detect_balance_anomalies(
        self,
        current_balances: Dict[str, Decimal],
        historical_balances: List[Dict[str, Decimal]],
    ) -> List[Anomaly]:
        """Detect unusual balance changes.

        Args:
            current_balances: Current balance by asset
            historical_balances: List of historical snapshots

        Returns:
            List of detected anomalies
        """
        anomalies = []

        if len(historical_balances) < 2:
            return anomalies

        for asset, current_value in current_balances.items():
            # Extract historical values for this asset
            historical_values = [
                snapshot.get(asset, Decimal(0))
                for snapshot in historical_balances
                if asset in snapshot
            ]

            if not historical_values or len(historical_values) < 2:
                continue

            # Calculate statistics
            mean = statistics.mean(historical_values)
            if len(historical_values) >= 2:
                std_dev = statistics.stdev(historical_values)
            else:
                std_dev = Decimal(0)

            # Calculate Z-score
            if std_dev > 0:
                z_score = (current_value - mean) / std_dev
            else:
                z_score = Decimal(0)

            # Calculate percentage change
            if historical_values[-1] > 0:
                change_percent = (
                    (current_value - historical_values[-1]) / historical_values[-1] * 100
                )
            else:
                change_percent = Decimal(0)

            # Detect anomalies
            if abs(z_score) >= self.Z_SCORE_CRITICAL:
                anomalies.append(Anomaly(
                    type="extreme_balance_change",
                    severity=AnomalySeverity.CRITICAL,
                    asset=asset,
                    description=f"Extreme change in {asset} balance",
                    value=float(current_value),
                    threshold=float(mean),
                    z_score=float(z_score),
                ))
            elif abs(z_score) >= self.Z_SCORE_WARNING:
                anomalies.append(Anomaly(
                    type="unusual_balance_change",
                    severity=AnomalySeverity.WARNING,
                    asset=asset,
                    description=f"Unusual change in {asset} balance",
                    value=float(current_value),
                    threshold=float(mean),
                    z_score=float(z_score),
                ))

        return anomalies

    async def detect_reconciliation_outliers(
        self,
        liability_data: Dict[str, Decimal],
        on_chain_data: Dict[str, Decimal],
    ) -> List[Anomaly]:
        """Detect reconciliation outliers.

        Args:
            liability_data: Customer liability data
            on_chain_data: On-chain balance data

        Returns:
            List of anomalies
        """
        anomalies = []

        # Calculate variance for each asset
        variances = []
        for asset in liability_data.keys():
            liability = liability_data.get(asset, Decimal(0))
            on_chain = on_chain_data.get(asset, Decimal(0))

            if liability > 0:
                variance = ((on_chain - liability) / liability * 100)
            else:
                variance = Decimal(0)

            variances.append((asset, variance))

        if not variances:
            return anomalies

        # Calculate mean and std dev of variances
        variance_values = [v for _, v in variances]
        mean_variance = statistics.mean(variance_values)

        if len(variance_values) >= 2:
            std_variance = statistics.stdev(variance_values)
        else:
            std_variance = Decimal(0)

        # Identify outliers
        for asset, variance in variances:
            if std_variance > 0:
                z_score = (variance - mean_variance) / std_variance
            else:
                z_score = Decimal(0)

            # Critical if variance is significantly negative (under-reserved)
            if variance < Decimal(-20):
                anomalies.append(Anomaly(
                    type="under_reserved_asset",
                    severity=AnomalySeverity.CRITICAL,
                    asset=asset,
                    description=f"{asset} is under-reserved by {abs(variance):.2f}%",
                    value=float(variance),
                    threshold=0.0,
                    z_score=float(z_score),
                ))
            elif variance < Decimal(-5):
                anomalies.append(Anomaly(
                    type="reconciliation_variance",
                    severity=AnomalySeverity.WARNING,
                    asset=asset,
                    description=f"Negative variance for {asset}: {variance:.2f}%",
                    value=float(variance),
                    threshold=0.0,
                    z_score=float(z_score),
                ))

        return anomalies

    async def detect_duplicate_entries(
        self,
        liability_records: List[Dict[str, any]],
    ) -> List[Anomaly]:
        """Detect duplicate or suspicious liability entries.

        Args:
            liability_records: List of liability records

        Returns:
            List of detected anomalies
        """
        anomalies = []
        seen = {}

        for record in liability_records:
            # Create a fingerprint for duplicate detection
            key = (
                record.get("customer_id"),
                record.get("asset"),
                record.get("amount"),
            )

            if key in seen:
                # Potential duplicate
                anomalies.append(Anomaly(
                    type="duplicate_entry",
                    severity=AnomalySeverity.CRITICAL,
                    asset=record.get("asset"),
                    description=f"Duplicate entry detected for customer {record.get('customer_id')}",
                    value=float(record.get("amount", 0)),
                    threshold=None,
                ))
            else:
                seen[key] = True

        return anomalies

    async def detect_negative_balances(
        self,
        balance_data: Dict[str, Decimal],
    ) -> List[Anomaly]:
        """Detect negative or invalid balances.

        Args:
            balance_data: Balance data by asset

        Returns:
            List of detected anomalies
        """
        anomalies = []

        for asset, balance in balance_data.items():
            if balance < 0:
                anomalies.append(Anomaly(
                    type="negative_balance",
                    severity=AnomalySeverity.CRITICAL,
                    asset=asset,
                    description=f"Negative balance detected for {asset}",
                    value=float(balance),
                    threshold=0.0,
                ))

        return anomalies

    async def detect_correlation_anomalies(
        self,
        balance_history: List[Dict[str, Decimal]],
    ) -> List[Anomaly]:
        """Detect unusual correlation patterns.

        Args:
            balance_history: Historical balance snapshots

        Returns:
            List of detected anomalies
        """
        anomalies = []

        if len(balance_history) < 3:
            return anomalies

        # Simple correlation check: normally correlated assets
        # (e.g., stablecoin balances should move together)
        stablecoin_assets = ["USDT", "USDC", "DAI", "BUSD"]

        stablecoin_values = {}
        for asset in stablecoin_assets:
            values = [
                snapshot.get(asset, Decimal(0))
                for snapshot in balance_history
                if asset in snapshot
            ]
            if len(values) >= 2:
                stablecoin_values[asset] = values

        if len(stablecoin_values) >= 2:
            # Check if any stablecoin is moving significantly differently
            for asset, values in stablecoin_values.items():
                changes = [
                    (values[i] - values[i-1]) / values[i-1] if values[i-1] > 0 else Decimal(0)
                    for i in range(1, len(values))
                ]

                if changes:
                    mean_change = statistics.mean(changes)
                    if len(changes) >= 2:
                        std_change = statistics.stdev(changes)
                    else:
                        std_change = Decimal(0)

                    # Check current change
                    if std_change > 0 and len(changes) > 0:
                        z_score = (changes[-1] - mean_change) / std_change

                        if abs(z_score) > self.Z_SCORE_WARNING:
                            anomalies.append(Anomaly(
                                type="correlation_anomaly",
                                severity=AnomalySeverity.WARNING,
                                asset=asset,
                                description=f"{asset} movement deviates from expected correlation",
                                value=float(changes[-1] * 100),
                                threshold=float(mean_change * 100),
                                z_score=float(z_score),
                            ))

        return anomalies

    async def generate_anomaly_report(
        self,
        current_balances: Dict[str, Decimal],
        historical_balances: List[Dict[str, Decimal]],
        liability_data: Dict[str, Decimal],
        on_chain_data: Dict[str, Decimal],
    ) -> Dict[str, any]:
        """Generate comprehensive anomaly report.

        Args:
            current_balances: Current balances
            historical_balances: Historical balance snapshots
            liability_data: Liability data
            on_chain_data: On-chain balance data

        Returns:
            Anomaly report
        """
        # Detect various anomalies
        tasks = [
            self.detect_balance_anomalies(current_balances, historical_balances),
            self.detect_reconciliation_outliers(liability_data, on_chain_data),
            self.detect_negative_balances(current_balances),
            self.detect_correlation_anomalies(historical_balances),
        ]

        results = await asyncio.gather(*tasks)

        # Combine all anomalies
        all_anomalies = []
        for result in results:
            all_anomalies.extend(result)

        # Severity counts
        severity_counts = {
            AnomalySeverity.INFO: 0,
            AnomalySeverity.WARNING: 0,
            AnomalySeverity.CRITICAL: 0,
        }

        for anomaly in all_anomalies:
            severity_counts[anomaly.severity] += 1

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_anomalies": len(all_anomalies),
            "severity_summary": {
                "critical": severity_counts[AnomalySeverity.CRITICAL],
                "warning": severity_counts[AnomalySeverity.WARNING],
                "info": severity_counts[AnomalySeverity.INFO],
            },
            "anomalies": [
                {
                    "type": a.type,
                    "severity": a.severity.value,
                    "asset": a.asset,
                    "description": a.description,
                    "value": a.value,
                    "threshold": a.threshold,
                    "z_score": a.z_score,
                    "timestamp": a.timestamp.isoformat(),
                }
                for a in all_anomalies
            ],
            "summary": self._generate_summary(severity_counts),
        }

    def _generate_summary(self, severity_counts: Dict[AnomalySeverity, int]) -> str:
        """Generate summary text."""
        critical = severity_counts[AnomalySeverity.CRITICAL]
        warning = severity_counts[AnomalySeverity.WARNING]

        if critical > 0:
            return f"CRITICAL: {critical} critical issues require immediate attention"
        elif warning > 0:
            return f"WARNING: {warning} anomalies detected, further investigation recommended"
        else:
            return "No significant anomalies detected"
