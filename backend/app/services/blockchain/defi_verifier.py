"""DeFi position verification service."""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any
from eth_utils import is_checksum_address, to_checksum_address

logger = logging.getLogger(__name__)


class ProtocolRisk(str, Enum):
    """Risk level for DeFi protocols."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DeFiPosition:
    """DeFi position information."""
    protocol: str
    position_type: str  # lending, borrowing, staking, lp
    chain: str
    address: str
    amount: Decimal
    token: str
    apy: Optional[Decimal] = None
    health_factor: Optional[Decimal] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProtocolRiskScore:
    """Risk score for a DeFi protocol."""
    protocol: str
    risk_level: ProtocolRisk
    tvl: Optional[Decimal] = None
    audit_status: Optional[str] = None
    age_days: Optional[int] = None
    exploits: int = 0
    score: Decimal = field(default_factory=lambda: Decimal(0))


class DeFiVerifier:
    """DeFi position verification service."""

    # Protocol-specific configurations
    AAVE_V3_ORACLE = {
        "ethereum": "0x54586bE62e3c3580375aE3723C71986AD7d293cB",
        "polygon": "0xb023e499F5500d1f6D5a30Da6ea4ed0c9F0faaC0",
        "arbitrum": "0x1a96fce64d9f0670e1c2e4797f8eCC2fAfD8f9e0",
    }

    COMPOUND_COMPTROLLER = {
        "ethereum": "0x3d9819210A31b4961b30EF54fE2F2FFE3c3eAA38",
    }

    UNISWAP_SUBGRAPH = {
        "ethereum": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    }

    LIDO_STETH = {
        "ethereum": "0xae7ab96520DE3A18E5e111B5eaAb095312D7fE84",
    }

    ROCKET_POOL_STAKING = {
        "ethereum": "0xDD3Ce2c7aB5d0e7BcDFf2CEc2Fe8d0C8C8bFa50c",
    }

    # Protocol risk database
    PROTOCOL_RISKS: Dict[str, ProtocolRiskScore] = {
        "aave_v3": ProtocolRiskScore(
            protocol="Aave V3",
            risk_level=ProtocolRisk.LOW,
            tvl=Decimal("10000000000"),
            audit_status="audited",
            age_days=1500,
            exploits=0,
            score=Decimal("0.1"),
        ),
        "compound": ProtocolRiskScore(
            protocol="Compound",
            risk_level=ProtocolRisk.LOW,
            tvl=Decimal("3000000000"),
            audit_status="audited",
            age_days=1800,
            exploits=1,
            score=Decimal("0.15"),
        ),
        "uniswap_v3": ProtocolRiskScore(
            protocol="Uniswap V3",
            risk_level=ProtocolRisk.LOW,
            tvl=Decimal("4000000000"),
            audit_status="audited",
            age_days=1200,
            exploits=0,
            score=Decimal("0.12"),
        ),
        "lido": ProtocolRiskScore(
            protocol="Lido",
            risk_level=ProtocolRisk.LOW,
            tvl=Decimal("30000000000"),
            audit_status="audited",
            age_days=1500,
            exploits=0,
            score=Decimal("0.08"),
        ),
        "rocket_pool": ProtocolRiskScore(
            protocol="Rocket Pool",
            risk_level=ProtocolRisk.MEDIUM,
            tvl=Decimal("5000000000"),
            audit_status="audited",
            age_days=1000,
            exploits=0,
            score=Decimal("0.25"),
        ),
    }

    def __init__(self):
        """Initialize DeFi verifier."""
        self.logger = logging.getLogger(self.__class__.__name__)

    async def get_aave_v3_positions(
        self,
        address: str,
        chain: str = "ethereum",
        adapter=None,
    ) -> List[DeFiPosition]:
        """Get Aave V3 lending/borrowing positions.

        Args:
            address: User address
            chain: Blockchain chain
            adapter: Ethereum adapter instance

        Returns:
            List of DeFi positions
        """
        if not adapter:
            return []

        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            response = await adapter.get_aave_v3_positions(address)

            if not response.success:
                return []

            positions = []
            data = response.data

            if data.get("total_collateral", 0) > 0:
                positions.append(DeFiPosition(
                    protocol="Aave V3",
                    position_type="collateral",
                    chain=chain,
                    address=address,
                    amount=data["total_collateral"],
                    token="MULTIPLE",
                ))

            if data.get("total_debt", 0) > 0:
                positions.append(DeFiPosition(
                    protocol="Aave V3",
                    position_type="debt",
                    chain=chain,
                    address=address,
                    amount=data["total_debt"],
                    token="MULTIPLE",
                    health_factor=data.get("health_factor"),
                ))

            return positions

        except Exception as e:
            self.logger.error(f"Failed to get Aave V3 positions: {e}")
            return []

    async def get_lido_staking(
        self,
        address: str,
        chain: str = "ethereum",
        adapter=None,
    ) -> List[DeFiPosition]:
        """Get Lido staking position.

        Args:
            address: User address
            chain: Blockchain chain
            adapter: Ethereum adapter instance

        Returns:
            List of staking positions
        """
        if not adapter:
            return []

        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            response = await adapter.get_lido_staking(address)

            if not response.success or not response.data:
                return []

            positions = []
            for balance in response.data:
                positions.append(DeFiPosition(
                    protocol="Lido",
                    position_type="staking",
                    chain=chain,
                    address=address,
                    amount=balance.amount,
                    token="stETH",
                    apy=Decimal("3.5"),
                ))

            return positions

        except Exception as e:
            self.logger.error(f"Failed to get Lido staking: {e}")
            return []

    async def get_uniswap_v3_positions(
        self,
        address: str,
        chain: str = "ethereum",
        adapter=None,
    ) -> List[DeFiPosition]:
        """Get Uniswap V3 LP positions.

        Args:
            address: User address
            chain: Blockchain chain
            adapter: Ethereum adapter instance

        Returns:
            List of LP positions
        """
        if not adapter:
            return []

        try:
            if not is_checksum_address(address):
                address = to_checksum_address(address)

            response = await adapter.get_uniswap_v3_positions(address)

            if not response.success:
                return []

            data = response.data

            positions = []
            for position_id in data.get("position_ids", []):
                positions.append(DeFiPosition(
                    protocol="Uniswap V3",
                    position_type="lp",
                    chain=chain,
                    address=address,
                    amount=Decimal(0),  # Would need to calculate from position data
                    token="LP_TOKEN",
                ))

            return positions

        except Exception as e:
            self.logger.error(f"Failed to get Uniswap V3 positions: {e}")
            return []

    async def get_all_positions(
        self,
        address: str,
        chain: str = "ethereum",
        adapters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[DeFiPosition]]:
        """Get all DeFi positions for an address.

        Args:
            address: User address
            chain: Blockchain chain
            adapters: Dictionary of available adapters

        Returns:
            Dictionary of positions by protocol
        """
        adapters = adapters or {}
        eth_adapter = adapters.get("ethereum")

        tasks = []
        position_types = []

        if eth_adapter:
            tasks.append(self.get_aave_v3_positions(address, chain, eth_adapter))
            position_types.append("aave_v3")

            tasks.append(self.get_lido_staking(address, chain, eth_adapter))
            position_types.append("lido")

            tasks.append(self.get_uniswap_v3_positions(address, chain, eth_adapter))
            position_types.append("uniswap_v3")

        if not tasks:
            return {}

        results = await asyncio.gather(*tasks, return_exceptions=True)

        positions_by_protocol = {}
        for protocol_type, result in zip(position_types, results):
            if isinstance(result, list):
                positions_by_protocol[protocol_type] = result
            else:
                positions_by_protocol[protocol_type] = []

        return positions_by_protocol

    async def calculate_defi_exposure(
        self,
        positions: List[DeFiPosition],
    ) -> Dict[str, Any]:
        """Calculate total DeFi exposure from positions.

        Args:
            positions: List of DeFi positions

        Returns:
            Exposure summary
        """
        total_collateral = Decimal(0)
        total_debt = Decimal(0)
        total_staking = Decimal(0)
        total_lp = Decimal(0)

        protocols = set()

        for pos in positions:
            protocols.add(pos.protocol)

            if pos.position_type == "collateral":
                total_collateral += pos.amount
            elif pos.position_type == "debt":
                total_debt += pos.amount
            elif pos.position_type == "staking":
                total_staking += pos.amount
            elif pos.position_type == "lp":
                total_lp += pos.amount

        return {
            "total_collateral": total_collateral,
            "total_debt": total_debt,
            "total_staking": total_staking,
            "total_lp": total_lp,
            "net_exposure": total_collateral + total_staking - total_debt,
            "protocols": list(protocols),
            "position_count": len(positions),
        }

    def get_protocol_risk(self, protocol: str) -> ProtocolRiskScore:
        """Get risk score for a protocol.

        Args:
            protocol: Protocol name

        Returns:
            Risk score data
        """
        key = protocol.lower().replace(" ", "_")
        return self.PROTOCOL_RISKS.get(key, ProtocolRiskScore(
            protocol=protocol,
            risk_level=ProtocolRisk.HIGH,
            score=Decimal("0.5"),
        ))

    async def assess_position_risk(
        self,
        positions: List[DeFiPosition],
    ) -> Dict[str, Any]:
        """Assess risk for a set of DeFi positions.

        Args:
            positions: List of positions

        Returns:
            Risk assessment data
        """
        risk_by_protocol = {}
        total_risk_score = Decimal(0)

        for pos in positions:
            protocol_risk = self.get_protocol_risk(pos.protocol)

            if pos.protocol not in risk_by_protocol:
                risk_by_protocol[pos.protocol] = {
                    "risk_level": protocol_risk.risk_level.value,
                    "score": float(protocol_risk.score),
                    "tvl": float(protocol_risk.tvl) if protocol_risk.tvl else None,
                    "positions": [],
                }

            risk_by_protocol[pos.protocol]["positions"].append({
                "type": pos.position_type,
                "amount": float(pos.amount),
                "token": pos.token,
            })

            total_risk_score += protocol_risk.score * pos.amount

        # Normalize overall risk
        if positions:
            avg_risk = total_risk_score / len(positions)
        else:
            avg_risk = Decimal(0)

        # Determine overall risk level
        if avg_risk < Decimal("0.2"):
            overall_level = ProtocolRisk.MINIMAL
        elif avg_risk < Decimal("0.35"):
            overall_level = ProtocolRisk.LOW
        elif avg_risk < Decimal("0.55"):
            overall_level = ProtocolRisk.MEDIUM
        elif avg_risk < Decimal("0.75"):
            overall_level = ProtocolRisk.HIGH
        else:
            overall_level = ProtocolRisk.CRITICAL

        return {
            "overall_risk_level": overall_level.value,
            "overall_risk_score": float(avg_risk),
            "risk_by_protocol": risk_by_protocol,
            "position_count": len(positions),
            "recommendation": self._get_risk_recommendation(overall_level),
        }

    def _get_risk_recommendation(self, risk_level: ProtocolRisk) -> str:
        """Get risk mitigation recommendation.

        Args:
            risk_level: Risk level

        Returns:
            Recommendation text
        """
        recommendations = {
            ProtocolRisk.MINIMAL: "Position is low-risk. Continue monitoring.",
            ProtocolRisk.LOW: "Position is acceptable. Consider diversification.",
            ProtocolRisk.MEDIUM: "Position has moderate risk. Recommend hedging or reduction.",
            ProtocolRisk.HIGH: "Position is high-risk. Strong recommendation to reduce exposure.",
            ProtocolRisk.CRITICAL: "Position is critical-risk. Immediate action recommended.",
        }
        return recommendations.get(risk_level, "Unknown risk level")

    async def generate_defi_report(
        self,
        address: str,
        chain: str = "ethereum",
        adapters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate comprehensive DeFi report for an address.

        Args:
            address: User address
            chain: Blockchain chain
            adapters: Available adapters

        Returns:
            Comprehensive DeFi report
        """
        positions_by_protocol = await self.get_all_positions(address, chain, adapters)

        # Flatten positions
        all_positions = []
        for protocol_positions in positions_by_protocol.values():
            all_positions.extend(protocol_positions)

        exposure = await self.calculate_defi_exposure(all_positions)
        risk_assessment = await self.assess_position_risk(all_positions)

        return {
            "address": address,
            "chain": chain,
            "generated_at": datetime.utcnow().isoformat(),
            "positions_by_protocol": {
                k: [
                    {
                        "protocol": p.protocol,
                        "type": p.position_type,
                        "amount": float(p.amount),
                        "token": p.token,
                        "apy": float(p.apy) if p.apy else None,
                    }
                    for p in v
                ]
                for k, v in positions_by_protocol.items()
            },
            "exposure": exposure,
            "risk_assessment": risk_assessment,
        }
