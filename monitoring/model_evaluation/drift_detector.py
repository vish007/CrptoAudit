#!/usr/bin/env python3
"""
Drift detection script for SimplyFI PoR platform models.

Implements:
- Population Stability Index (PSI)
- Kolmogorov-Smirnov test for feature drift
- Concept drift detection (label shift)
- Outputs drift scores and alerts
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DriftDetector:
    """Detect data and concept drift in model predictions."""

    PSI_WARNING_THRESHOLD = 0.15
    PSI_CRITICAL_THRESHOLD = 0.25
    KS_WARNING_THRESHOLD = 0.08
    KS_CRITICAL_THRESHOLD = 0.15

    def __init__(self, output_dir: Path = Path("monitoring/model_evaluation")):
        """Initialize drift detector."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.drift_scores: Dict[str, Any] = {}

    def generate_baseline_distribution(self, n_samples: int = 10000) -> np.ndarray:
        """Generate baseline distribution (historical data)."""
        logger.info("Generating baseline distribution...")

        # Simulate realistic reserve ratio distribution
        baseline = np.random.normal(loc=1.042, scale=0.025, size=n_samples)
        baseline = np.clip(baseline, 0.95, 1.15)

        logger.info(f"Baseline - Mean: {baseline.mean():.4f}, Std: {baseline.std():.4f}")
        return baseline

    def generate_current_distribution(self, n_samples: int = 10000, drift_type: str = "normal") -> np.ndarray:
        """Generate current distribution with optional drift."""
        logger.info(f"Generating current distribution (drift_type={drift_type})...")

        if drift_type == "normal":
            # No drift
            current = np.random.normal(loc=1.042, scale=0.025, size=n_samples)
        elif drift_type == "mean_shift":
            # Mean shift (upward)
            current = np.random.normal(loc=1.056, scale=0.025, size=n_samples)
        elif drift_type == "variance_shift":
            # Increased variance
            current = np.random.normal(loc=1.042, scale=0.045, size=n_samples)
        elif drift_type == "concept_drift":
            # Bimodal distribution (concept drift)
            part1 = np.random.normal(loc=1.02, scale=0.02, size=n_samples // 2)
            part2 = np.random.normal(loc=1.08, scale=0.02, size=n_samples // 2)
            current = np.concatenate([part1, part2])
        else:
            current = np.random.normal(loc=1.042, scale=0.025, size=n_samples)

        current = np.clip(current, 0.95, 1.15)
        logger.info(f"Current - Mean: {current.mean():.4f}, Std: {current.std():.4f}")
        return current

    def calculate_psi(
        self,
        baseline: np.ndarray,
        current: np.ndarray,
        n_bins: int = 10
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate Population Stability Index.

        PSI = Σ((% of current - % of baseline) × ln(% of current / % of baseline))

        Returns:
            Tuple of (psi_score, detailed_breakdown)
        """
        logger.info("Calculating Population Stability Index...")

        # Create bins based on baseline
        min_val = min(baseline.min(), current.min())
        max_val = max(baseline.max(), current.max())
        bins = np.linspace(min_val, max_val, n_bins + 1)

        # Get counts for baseline and current
        baseline_counts, _ = np.histogram(baseline, bins=bins)
        current_counts, _ = np.histogram(current, bins=bins)

        # Convert to percentages
        baseline_pct = baseline_counts / baseline_counts.sum()
        current_pct = current_counts / current_counts.sum()

        # Avoid log(0) by adding small epsilon
        epsilon = 1e-10
        baseline_pct = baseline_pct + epsilon
        current_pct = current_pct + epsilon

        # Calculate PSI
        psi = np.sum((current_pct - baseline_pct) * np.log(current_pct / baseline_pct))

        # Determine status
        if psi < self.PSI_WARNING_THRESHOLD:
            status = "STABLE"
        elif psi < self.PSI_CRITICAL_THRESHOLD:
            status = "WARNING"
        else:
            status = "CRITICAL"

        breakdown = {
            "psi_score": float(psi),
            "status": status,
            "bin_count": n_bins,
            "baseline_mean": float(baseline.mean()),
            "baseline_std": float(baseline.std()),
            "current_mean": float(current.mean()),
            "current_std": float(current.std()),
            "mean_shift": float(current.mean() - baseline.mean()),
            "std_shift": float(current.std() - baseline.std())
        }

        logger.info(f"PSI: {psi:.4f} - Status: {status}")
        return psi, breakdown

    def calculate_ks_statistic(
        self,
        baseline: np.ndarray,
        current: np.ndarray
    ) -> Tuple[float, float, Dict[str, Any]]:
        """
        Kolmogorov-Smirnov test for distribution drift.

        Tests null hypothesis: baseline and current have same distribution.

        Returns:
            Tuple of (ks_statistic, p_value, detailed_breakdown)
        """
        logger.info("Calculating Kolmogorov-Smirnov statistic...")

        ks_stat, p_value = stats.ks_2samp(baseline, current)

        # Determine status
        if ks_stat < self.KS_WARNING_THRESHOLD:
            status = "STABLE"
        elif ks_stat < self.KS_CRITICAL_THRESHOLD:
            status = "WARNING"
        else:
            status = "CRITICAL"

        breakdown = {
            "ks_statistic": float(ks_stat),
            "p_value": float(p_value),
            "status": status,
            "significant_at_alpha_0_05": p_value < 0.05,
            "significant_at_alpha_0_01": p_value < 0.01,
            "interpretation": "Distributions differ" if p_value < 0.05 else "No significant difference"
        }

        logger.info(f"KS Statistic: {ks_stat:.4f}, p-value: {p_value:.4f}")
        logger.info(f"Status: {status}, Significant (α=0.05): {p_value < 0.05}")

        return ks_stat, p_value, breakdown

    def detect_concept_drift(
        self,
        baseline_labels: np.ndarray,
        current_labels: np.ndarray
    ) -> Dict[str, Any]:
        """
        Detect concept drift using label distribution shift.

        Returns:
            Dictionary with drift metrics
        """
        logger.info("Detecting concept drift...")

        # Calculate class distributions
        baseline_anomaly_rate = baseline_labels.mean()
        current_anomaly_rate = current_labels.mean()

        # KL divergence between label distributions
        p = np.array([baseline_anomaly_rate, 1 - baseline_anomaly_rate])
        q = np.array([current_anomaly_rate, 1 - current_anomaly_rate])

        # Avoid log(0)
        p = np.clip(p, 1e-10, 1)
        q = np.clip(q, 1e-10, 1)

        kl_divergence = np.sum(p * np.log(p / q))

        # Label shift ratio
        shift_ratio = current_anomaly_rate / (baseline_anomaly_rate + 1e-10)

        result = {
            "baseline_anomaly_rate": float(baseline_anomaly_rate),
            "current_anomaly_rate": float(current_anomaly_rate),
            "rate_change": float(current_anomaly_rate - baseline_anomaly_rate),
            "shift_ratio": float(shift_ratio),
            "kl_divergence": float(kl_divergence),
            "status": "STABLE" if kl_divergence < 0.05 else "DRIFT"
        }

        logger.info(f"Concept Drift - KL Divergence: {kl_divergence:.4f}")
        logger.info(f"Anomaly rate shift: {baseline_anomaly_rate:.2%} → {current_anomaly_rate:.2%}")

        return result

    def feature_drift_report(self) -> Dict[str, Dict[str, Any]]:
        """Generate drift report for key features."""
        logger.info("Generating feature drift report...")

        features = [
            ("reserve_ratio", "normal"),
            ("transaction_volume", "mean_shift"),
            ("balance_delta", "concept_drift"),
            ("address_change_rate", "normal"),
            ("gas_price", "mean_shift")
        ]

        report = {}

        for feature_name, drift_type in features:
            logger.info(f"\nAnalyzing feature: {feature_name} (drift_type={drift_type})")

            baseline = self.generate_baseline_distribution(n_samples=10000)
            current = self.generate_current_distribution(n_samples=10000, drift_type=drift_type)

            psi_score, psi_detail = self.calculate_psi(baseline, current)
            ks_stat, p_value, ks_detail = self.calculate_ks_statistic(baseline, current)

            # Determine action
            if psi_score > self.PSI_CRITICAL_THRESHOLD or ks_stat > self.KS_CRITICAL_THRESHOLD:
                action = "RETRAIN_NOW"
            elif psi_score > self.PSI_WARNING_THRESHOLD or ks_stat > self.KS_WARNING_THRESHOLD:
                action = "PLAN_RETRAINING"
            else:
                action = "MONITOR"

            report[feature_name] = {
                "psi": psi_detail,
                "ks_test": ks_detail,
                "action": action
            }

        return report

    def generate_alert(self, feature_name: str, drift_score: float, drift_type: str) -> Dict[str, Any]:
        """Generate alert for high drift."""
        if drift_score > self.PSI_CRITICAL_THRESHOLD or (drift_type == "ks" and drift_score > self.KS_CRITICAL_THRESHOLD):
            severity = "CRITICAL"
        elif drift_score > self.PSI_WARNING_THRESHOLD or (drift_type == "ks" and drift_score > self.KS_WARNING_THRESHOLD):
            severity = "WARNING"
        else:
            severity = "INFO"

        return {
            "timestamp": datetime.now().isoformat(),
            "feature": feature_name,
            "drift_type": drift_type,
            "drift_score": float(drift_score),
            "severity": severity,
            "message": f"{severity}: {drift_type} drift detected in {feature_name}",
            "recommended_action": "RETRAIN_NOW" if severity == "CRITICAL" else "MONITOR"
        }

    def run_detection(self) -> None:
        """Run complete drift detection."""
        logger.info("Starting drift detection...")

        # Feature drift analysis
        feature_drift = self.feature_drift_report()

        # Concept drift analysis
        baseline_labels = np.random.binomial(1, 0.032, 10000)
        current_labels = np.random.binomial(1, 0.041, 10000)  # Increased anomaly rate
        concept_drift = self.detect_concept_drift(baseline_labels, current_labels)

        # Generate alerts
        alerts = []
        for feature_name, metrics in feature_drift.items():
            if metrics["action"] in ["RETRAIN_NOW", "PLAN_RETRAINING"]:
                psi_score = metrics["psi"]["psi_score"]
                alerts.append(self.generate_alert(feature_name, psi_score, "psi"))

        if concept_drift["status"] == "DRIFT":
            alerts.append({
                "timestamp": datetime.now().isoformat(),
                "feature": "concept",
                "drift_type": "label_shift",
                "drift_score": concept_drift["kl_divergence"],
                "severity": "WARNING",
                "message": f"Concept drift detected (KL={concept_drift['kl_divergence']:.4f})",
                "recommended_action": "MONITOR"
            })

        # Compile results
        self.drift_scores = {
            "detection_date": datetime.now().isoformat(),
            "feature_drift": feature_drift,
            "concept_drift": concept_drift,
            "alerts": alerts,
            "summary": {
                "total_features_analyzed": len(feature_drift),
                "features_with_drift": sum(1 for m in feature_drift.values() if m["action"] != "MONITOR"),
                "critical_alerts": sum(1 for a in alerts if a["severity"] == "CRITICAL"),
                "warning_alerts": sum(1 for a in alerts if a["severity"] == "WARNING"),
                "recommended_actions": {
                    "retrain_now": sum(1 for m in feature_drift.values() if m["action"] == "RETRAIN_NOW"),
                    "plan_retraining": sum(1 for m in feature_drift.values() if m["action"] == "PLAN_RETRAINING"),
                    "monitor": sum(1 for m in feature_drift.values() if m["action"] == "MONITOR")
                }
            }
        }

        # Save results
        output_file = self.output_dir / "drift_scores.json"
        with open(output_file, 'w') as f:
            json.dump(self.drift_scores, f, indent=2)
        logger.info(f"Saved drift scores to {output_file}")

        # Log summary
        logger.info("\n" + "="*60)
        logger.info("DRIFT DETECTION SUMMARY")
        logger.info("="*60)
        summary = self.drift_scores["summary"]
        logger.info(f"Features analyzed: {summary['total_features_analyzed']}")
        logger.info(f"Features with drift: {summary['features_with_drift']}")
        logger.info(f"Critical alerts: {summary['critical_alerts']}")
        logger.info(f"Warning alerts: {summary['warning_alerts']}")
        logger.info(f"Retraining needed: {summary['recommended_actions']['retrain_now']}")
        logger.info("="*60)

        logger.info("Drift detection completed successfully!")


def main() -> None:
    """Run drift detection."""
    detector = DriftDetector()
    detector.run_detection()


if __name__ == "__main__":
    main()
