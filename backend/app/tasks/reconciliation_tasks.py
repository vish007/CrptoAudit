"""
Celery tasks for daily balance reconciliation and reserve ratio monitoring.

This module handles daily reconciliation of on-chain balances against
customer liabilities, reserve ratio calculations, and alert generation
for under-reserved scenarios.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
from sqlalchemy import select, func
from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models import (
    Engagement,
    AssetBalance,
    CustomerLiability,
    ReserveRatio,
    ReconciliationRecord,
    WalletAddress,
    User,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="app.tasks.reconciliation_tasks.daily_reconciliation_task",
    queue="reconciliation",
)
def daily_reconciliation_task(
    self,
    engagement_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Run daily balance reconciliation for one or all engagements.

    Args:
        self: Celery task instance
        engagement_id: Optional specific engagement ID, if None reconciles all

    Returns:
        dict: Reconciliation results summary
    """
    try:
        logger.info(
            f"Starting daily reconciliation, "
            f"engagement_id={engagement_id or 'all'}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _daily_reconciliation_async(engagement_id)
            )
        finally:
            loop.close()

        logger.info(f"Daily reconciliation completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Daily reconciliation failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _daily_reconciliation_async(
    engagement_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Async implementation of daily reconciliation.

    Args:
        engagement_id: Optional specific engagement ID

    Returns:
        dict: Reconciliation results
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch engagements to reconcile
            stmt = select(Engagement)
            if engagement_id:
                stmt = stmt.where(Engagement.id == engagement_id)
            else:
                # Only reconcile active engagements
                stmt = stmt.where(Engagement.status == "active")

            result = await session.execute(stmt)
            engagements = result.scalars().all()

            if not engagements:
                return {
                    "status": "success",
                    "engagements_reconciled": 0,
                    "records_created": 0,
                    "error": "No engagements found",
                }

            total_records = 0
            reconciliation_results = []

            for engagement in engagements:
                try:
                    # Get all asset balances for this engagement
                    balance_stmt = select(func.sum(AssetBalance.on_chain_balance)).where(
                        AssetBalance.wallet_id.in_(
                            select(WalletAddress.id).where(
                                WalletAddress.engagement_id == engagement.id
                            )
                        )
                    )
                    balance_result = await session.execute(balance_stmt)
                    total_assets = balance_result.scalar() or 0

                    # Get all customer liabilities
                    liability_stmt = select(
                        func.sum(CustomerLiability.amount)
                    ).where(
                        CustomerLiability.engagement_id == engagement.id
                    )
                    liability_result = await session.execute(liability_stmt)
                    total_liabilities = liability_result.scalar() or 0

                    # Calculate reserve ratio
                    reserve_ratio = (
                        (total_assets / total_liabilities)
                        if total_liabilities > 0
                        else 0
                    )

                    # Create reconciliation record
                    reconciliation = ReconciliationRecord(
                        engagement_id=engagement.id,
                        recorded_date=datetime.utcnow().date(),
                        total_assets=total_assets,
                        total_liabilities=total_liabilities,
                        reserve_ratio=reserve_ratio,
                        status="completed",
                        reconciliation_notes=f"Automated daily reconciliation on {datetime.utcnow()}",
                    )
                    session.add(reconciliation)

                    # Update or create reserve ratio record
                    ratio_stmt = select(ReserveRatio).where(
                        (ReserveRatio.engagement_id == engagement.id) &
                        (ReserveRatio.recorded_date == datetime.utcnow().date())
                    )
                    ratio_record = (
                        await session.execute(ratio_stmt)
                    ).scalar_one_or_none()

                    if ratio_record:
                        ratio_record.total_assets = total_assets
                        ratio_record.total_liabilities = total_liabilities
                        ratio_record.ratio = reserve_ratio
                    else:
                        ratio_record = ReserveRatio(
                            engagement_id=engagement.id,
                            recorded_date=datetime.utcnow().date(),
                            total_assets=total_assets,
                            total_liabilities=total_liabilities,
                            ratio=reserve_ratio,
                        )
                        session.add(ratio_record)

                    total_records += 1
                    reconciliation_results.append({
                        "engagement_id": engagement.id,
                        "engagement_name": engagement.name,
                        "total_assets": total_assets,
                        "total_liabilities": total_liabilities,
                        "reserve_ratio": reserve_ratio,
                        "status": "reconciled",
                    })

                except Exception as e:
                    logger.error(
                        f"Error reconciling engagement {engagement.id}: "
                        f"{str(e)}"
                    )
                    reconciliation_results.append({
                        "engagement_id": engagement.id,
                        "status": "failed",
                        "error": str(e),
                    })

            await session.commit()

            return {
                "status": "success",
                "engagements_reconciled": len(engagements),
                "records_created": total_records,
                "timestamp": datetime.utcnow().isoformat(),
                "details": reconciliation_results,
            }

        except Exception as e:
            logger.error(
                f"Error in async reconciliation: {str(e)}", exc_info=True
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.reconciliation_tasks.check_reserve_ratios_task",
    queue="reconciliation",
)
def check_reserve_ratios_task(self) -> Dict[str, Any]:
    """
    Check all active engagements for reserve adequacy against VARA minimum.

    Returns:
        dict: Summary of reserve ratio checks
    """
    try:
        logger.info("Starting reserve ratio check")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _check_reserve_ratios_async()
            )
        finally:
            loop.close()

        logger.info(f"Reserve ratio check completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Reserve ratio check failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _check_reserve_ratios_async() -> Dict[str, Any]:
    """
    Async implementation of reserve ratio checking.

    Returns:
        dict: Summary of reserve ratio checks
    """
    async with AsyncSessionLocal() as session:
        try:
            min_reserve_ratio = float(settings.VARA_MIN_RESERVE_RATIO)

            # Get latest reserve ratios for all active engagements
            stmt = select(ReserveRatio).where(
                ReserveRatio.recorded_date == datetime.utcnow().date()
            )
            result = await session.execute(stmt)
            ratios = result.scalars().all()

            compliant = []
            non_compliant = []

            for ratio in ratios:
                if (ratio.ratio or 0) >= min_reserve_ratio:
                    compliant.append({
                        "engagement_id": ratio.engagement_id,
                        "ratio": ratio.ratio,
                    })
                else:
                    non_compliant.append({
                        "engagement_id": ratio.engagement_id,
                        "ratio": ratio.ratio,
                        "shortfall": min_reserve_ratio - (ratio.ratio or 0),
                    })

            return {
                "status": "success",
                "min_required_ratio": min_reserve_ratio * 100,
                "total_engagements": len(ratios),
                "compliant_count": len(compliant),
                "non_compliant_count": len(non_compliant),
                "timestamp": datetime.utcnow().isoformat(),
                "non_compliant_engagements": non_compliant[:10],  # First 10
            }

        except Exception as e:
            logger.error(
                f"Error in reserve ratio check: {str(e)}", exc_info=True
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.reconciliation_tasks.alert_under_reserved_task",
    queue="reconciliation",
)
def alert_under_reserved_task(self) -> Dict[str, Any]:
    """
    Send alerts for any engagements with under-reserved assets.

    Returns:
        dict: Alert status and count
    """
    try:
        logger.info("Starting under-reserved alert task")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _alert_under_reserved_async()
            )
        finally:
            loop.close()

        logger.info(f"Under-reserved alerts completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Under-reserved alert task failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _alert_under_reserved_async() -> Dict[str, Any]:
    """
    Async implementation of under-reserved alerting.

    Returns:
        dict: Alert summary
    """
    async with AsyncSessionLocal() as session:
        try:
            min_reserve_ratio = float(settings.VARA_MIN_RESERVE_RATIO)

            # Get latest reserve ratios
            stmt = select(ReserveRatio).where(
                ReserveRatio.recorded_date == datetime.utcnow().date()
            )
            result = await session.execute(stmt)
            ratios = result.scalars().all()

            alerts_sent = 0
            under_reserved = []

            for ratio in ratios:
                if (ratio.ratio or 0) < min_reserve_ratio:
                    under_reserved.append({
                        "engagement_id": ratio.engagement_id,
                        "actual_ratio": ratio.ratio,
                        "required_ratio": min_reserve_ratio,
                        "shortfall_pct": (min_reserve_ratio - (ratio.ratio or 0)) * 100,
                    })

                    # Get engagement details for alert
                    eng_stmt = select(Engagement).where(
                        Engagement.id == ratio.engagement_id
                    )
                    eng_result = await session.execute(eng_stmt)
                    engagement = eng_result.scalar_one_or_none()

                    if engagement and engagement.admin_id:
                        # Get admin user for notification
                        admin_stmt = select(User).where(
                            User.id == engagement.admin_id
                        )
                        admin_result = await session.execute(admin_stmt)
                        admin = admin_result.scalar_one_or_none()

                        if admin:
                            # In production, send actual email/notification
                            logger.warning(
                                f"ALERT: Engagement {engagement.name} "
                                f"({engagement.id}) is under-reserved. "
                                f"Ratio: {ratio.ratio*100:.2f}% "
                                f"(required: {min_reserve_ratio*100:.2f}%)"
                            )
                            alerts_sent += 1

            return {
                "status": "success",
                "alerts_sent": alerts_sent,
                "under_reserved_count": len(under_reserved),
                "timestamp": datetime.utcnow().isoformat(),
                "under_reserved": under_reserved[:10],  # First 10
            }

        except Exception as e:
            logger.error(
                f"Error in under-reserved alerting: {str(e)}",
                exc_info=True,
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.reconciliation_tasks.generate_reconciliation_report_task",
    queue="reconciliation",
)
def generate_reconciliation_report_task(
    self,
    engagement_id: int,
    date_range: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Generate a reconciliation report for a date range.

    Args:
        self: Celery task instance
        engagement_id: Database ID of the engagement
        date_range: Dict with 'start_date' and 'end_date' (YYYY-MM-DD format)

    Returns:
        dict: Report generation status
    """
    try:
        logger.info(
            f"Starting reconciliation report for engagement_id="
            f"{engagement_id}, date_range={date_range}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _generate_reconciliation_report_async(
                    engagement_id, date_range
                )
            )
        finally:
            loop.close()

        logger.info(f"Reconciliation report generated: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Reconciliation report failed: {str(e)}", exc_info=True
        )
        raise self.retry(exc=e, countdown=300, max_retries=2)


async def _generate_reconciliation_report_async(
    engagement_id: int,
    date_range: Optional[Dict[str, str]],
) -> Dict[str, Any]:
    """
    Async implementation of reconciliation report generation.

    Args:
        engagement_id: Database ID of the engagement
        date_range: Optional date range

    Returns:
        dict: Report generation result
    """
    async with AsyncSessionLocal() as session:
        try:
            # Fetch engagement
            stmt = select(Engagement).where(
                Engagement.id == engagement_id
            )
            result = await session.execute(stmt)
            engagement = result.scalar_one_or_none()

            if not engagement:
                return {
                    "engagement_id": engagement_id,
                    "status": "error",
                    "error": "Engagement not found",
                }

            # Build query for reconciliation records
            query = select(ReconciliationRecord).where(
                ReconciliationRecord.engagement_id == engagement_id
            )

            if date_range:
                start_date = datetime.strptime(
                    date_range.get("start_date", ""), "%Y-%m-%d"
                ).date()
                end_date = datetime.strptime(
                    date_range.get("end_date", ""), "%Y-%m-%d"
                ).date()
                query = query.where(
                    (ReconciliationRecord.recorded_date >= start_date) &
                    (ReconciliationRecord.recorded_date <= end_date)
                )
            else:
                # Default to last 30 days
                start_date = (datetime.utcnow() - timedelta(days=30)).date()
                query = query.where(
                    ReconciliationRecord.recorded_date >= start_date
                )

            query = query.order_by(ReconciliationRecord.recorded_date.desc())
            result = await session.execute(query)
            records = result.scalars().all()

            if not records:
                return {
                    "engagement_id": engagement_id,
                    "status": "no_data",
                    "error": "No reconciliation records found",
                }

            # Calculate summary statistics
            ratios = [r.reserve_ratio or 0 for r in records]
            avg_ratio = sum(ratios) / len(ratios) if ratios else 0
            min_ratio = min(ratios) if ratios else 0
            max_ratio = max(ratios) if ratios else 0

            return {
                "status": "success",
                "engagement_id": engagement_id,
                "engagement_name": engagement.name,
                "report_period": f"{records[-1].recorded_date} to {records[0].recorded_date}",
                "total_records": len(records),
                "average_reserve_ratio": avg_ratio,
                "min_reserve_ratio": min_ratio,
                "max_reserve_ratio": max_ratio,
                "average_assets": (
                    sum([r.total_assets or 0 for r in records]) / len(records)
                    if records
                    else 0
                ),
                "average_liabilities": (
                    sum([r.total_liabilities or 0 for r in records]) / len(records)
                    if records
                    else 0
                ),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(
                f"Error generating reconciliation report: {str(e)}",
                exc_info=True,
            )
            await session.rollback()
            raise


@celery_app.task(
    bind=True,
    name="app.tasks.reconciliation_tasks.cleanup_expired_tokens_task",
    queue="default",
)
def cleanup_expired_tokens_task(self) -> Dict[str, Any]:
    """
    Clean up expired authentication tokens from the database.

    Returns:
        dict: Cleanup summary
    """
    try:
        logger.info("Starting token cleanup task")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _cleanup_expired_tokens_async()
            )
        finally:
            loop.close()

        logger.info(f"Token cleanup completed: {result}")
        return result

    except Exception as e:
        logger.error(
            f"Token cleanup task failed: {str(e)}", exc_info=True
        )
        # Don't retry cleanup tasks
        return {
            "status": "error",
            "error": str(e),
            "tokens_deleted": 0,
        }


async def _cleanup_expired_tokens_async() -> Dict[str, Any]:
    """
    Async implementation of expired token cleanup.

    Returns:
        dict: Cleanup summary
    """
    async with AsyncSessionLocal() as session:
        try:
            # In a real implementation, this would query a token table
            # and delete expired tokens. For now, just log the operation.
            logger.info("Token cleanup check completed")

            return {
                "status": "success",
                "tokens_deleted": 0,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(
                f"Error in token cleanup: {str(e)}", exc_info=True
            )
            await session.rollback()
            raise
