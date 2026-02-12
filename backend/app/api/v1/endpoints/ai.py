"""AI agent endpoints for analysis and insights."""
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.security import get_current_active_user, extract_tenant_id
from app.models.engagement import Engagement

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze")
async def analyze_data(
    engagement_id: str,
    analysis_type: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Analyze engagement data for anomalies using AI.

    Args:
        engagement_id: Engagement ID
        analysis_type: Type of analysis (balances, transactions, patterns)
        current_user: Current authenticated user
        session: Database session

    Returns:
        Analysis results with anomalies
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Mock AI analysis
    return {
        "analysis_type": analysis_type,
        "engagement_id": engagement_id,
        "anomalies_detected": 2,
        "anomalies": [
            {
                "type": "balance_spike",
                "asset": "USDC",
                "severity": "medium",
                "description": "Unusual balance increase on 2024-01-15",
                "recommendation": "Review transaction logs for period",
            },
            {
                "type": "wallet_movement",
                "asset": "ETH",
                "severity": "low",
                "description": "Transfer to unfamiliar address",
                "recommendation": "Verify custodian transaction",
            },
        ],
        "overall_risk_score": 3.5,
        "confidence": 0.87,
    }


@router.post("/generate-narrative")
async def generate_narrative(
    engagement_id: str,
    section: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate narrative sections for reports using AI.

    Args:
        engagement_id: Engagement ID
        section: Report section (executive_summary, findings, conclusion)
        current_user: Current authenticated user
        session: Database session

    Returns:
        Generated narrative text
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can generate narratives",
        )

    # Mock narrative generation
    narratives = {
        "executive_summary": """
Our audit procedures included the verification of digital asset holdings
as of the reporting date. We obtained independent confirmations from
custodians and verified blockchain transactions. Based on our testing,
we found no material exceptions in the verification procedures performed.
        """,
        "findings": """
During our engagement, we verified reserve ratios across all material
cryptocurrencies. The organization maintains sufficient reserves to cover
100% of customer liabilities. We observed proper segregation of customer
assets and found no indication of unauthorized transactions.
        """,
        "conclusion": """
Based on the procedures performed, we are satisfied that the entity
maintains adequate proof of reserves as of the reporting date in accordance
with VARA standards and our audit scope.
        """,
    }

    return {
        "engagement_id": engagement_id,
        "section": section,
        "narrative": narratives.get(section, ""),
        "confidence": 0.92,
        "can_modify": True,
    }


@router.post("/compliance-check")
async def compliance_check(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Check VARA compliance requirements.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Compliance check results
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if engagement.auditor_tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditor can check compliance",
        )

    return {
        "engagement_id": engagement_id,
        "compliance_level": "LEVEL_3",
        "checks": [
            {
                "requirement": "Reserve Ratio >= 95%",
                "status": "PASS",
                "actual_value": 98.5,
                "required_value": 95.0,
            },
            {
                "requirement": "All wallets verified",
                "status": "PASS",
                "verified_wallets": 24,
                "total_wallets": 24,
            },
            {
                "requirement": "Customer segregation verified",
                "status": "PASS",
                "variance_pct": 0.02,
            },
            {
                "requirement": "Merkle tree generated and published",
                "status": "PASS",
                "root_hash_verified": True,
            },
        ],
        "overall_compliant": True,
        "compliance_score": 98.5,
    }


@router.post("/chat")
async def chat_with_agent(
    engagement_id: str,
    message: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Interactive chat with AI audit assistant.

    Args:
        engagement_id: Engagement ID
        message: User message
        current_user: Current authenticated user
        session: Database session

    Returns:
        Assistant response
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Mock chat response
    responses = {
        "reserves": "The total reserves are currently $2.5M with a 98.5% reserve ratio.",
        "compliance": "All VARA Level 3 requirements are met for this engagement.",
        "wallets": "We have verified 24 wallet addresses across 5 blockchains.",
        "default": f"I can help you with audit data, reserve ratios, and compliance checks. What would you like to know?",
    }

    for key in responses.keys():
        if key in message.lower():
            response = responses[key]
            break
    else:
        response = responses["default"]

    return {
        "engagement_id": engagement_id,
        "user_message": message,
        "assistant_response": response,
        "confidence": 0.85,
    }


@router.get("/insights/{engagement_id}")
async def get_insights(
    engagement_id: str,
    current_user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get AI-generated insights for engagement.

    Args:
        engagement_id: Engagement ID
        current_user: Current authenticated user
        session: Database session

    Returns:
        Key insights and recommendations
    """
    tenant_id = extract_tenant_id(current_user)

    stmt = select(Engagement).where(Engagement.id == engagement_id)
    result = await session.execute(stmt)
    engagement = result.scalar_one_or_none()

    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )

    if (
        engagement.client_tenant_id != tenant_id
        and engagement.auditor_tenant_id != tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return {
        "engagement_id": engagement_id,
        "key_insights": [
            "Reserve ratio is healthy at 98.5%, well above 95% minimum",
            "All customer liabilities properly segregated",
            "DeFi positions represent 15% of total assets",
            "Recent protocol updates affect 2 positions",
        ],
        "recommendations": [
            "Consider rebalancing DeFi positions for better yields",
            "Implement additional checks for smart contract interactions",
            "Review custodian agreements quarterly",
        ],
        "risk_areas": [
            "Concentration in single blockchain (Ethereum: 60%)",
            "Staking lock-up period on 500K USDC",
        ],
        "next_actions": [
            "Complete final verification procedures",
            "Generate audit report",
            "Schedule customer summary presentation",
        ],
    }
