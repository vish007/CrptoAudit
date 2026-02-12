"""
Celery application configuration for background task processing.

This module sets up Celery with Redis as broker and result backend,
configures beat schedules for periodic tasks, and initializes all task
handlers for blockchain verification, report generation, and reconciliation.
"""
from celery import Celery
from celery.schedules import crontab, schedule
from kombu import Exchange, Queue
from datetime import timedelta
import logging
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Celery app
celery_app = Celery(
    "simplyfi_por",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configuration
celery_app.conf.update(
    # Task configuration
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Task execution settings
    task_track_started=True,
    task_time_limit=30 * 60,  # Hard limit: 30 minutes
    task_soft_time_limit=25 * 60,  # Soft limit: 25 minutes
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,

    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_persistent=True,

    # Broker settings
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,

    # Task retry settings
    task_autoretry_for=(Exception,),
    task_max_retries=3,
    task_default_retry_delay=300,  # 5 minutes

    # Routing
    task_routes={
        "app.tasks.verification_tasks.*": {"queue": "verification"},
        "app.tasks.report_tasks.*": {"queue": "reports"},
        "app.tasks.reconciliation_tasks.*": {"queue": "reconciliation"},
    },

    # Queue configuration
    task_queues=(
        Queue(
            "default",
            Exchange("default", type="direct"),
            routing_key="default",
            priority=10,
        ),
        Queue(
            "verification",
            Exchange("verification", type="direct"),
            routing_key="verification",
            priority=20,
        ),
        Queue(
            "reports",
            Exchange("reports", type="direct"),
            routing_key="reports",
            priority=15,
        ),
        Queue(
            "reconciliation",
            Exchange("reconciliation", type="direct"),
            routing_key="reconciliation",
            priority=5,
        ),
    ),

    # Beat schedule for periodic tasks
    beat_schedule={
        # Blockchain health check - every 15 minutes
        "blockchain_health_check": {
            "task": "app.tasks.verification_tasks.blockchain_health_check_task",
            "schedule": timedelta(minutes=15),
            "options": {"queue": "verification", "priority": 10},
            "kwargs": {},
        },
        # Reserve ratio check - every 6 hours
        "reserve_ratio_check": {
            "task": "app.tasks.reconciliation_tasks.check_reserve_ratios_task",
            "schedule": timedelta(hours=6),
            "options": {"queue": "reconciliation", "priority": 8},
            "kwargs": {},
        },
        # Daily reconciliation - every day at 00:00 UTC
        "daily_reconciliation": {
            "task": "app.tasks.reconciliation_tasks.daily_reconciliation_task",
            "schedule": crontab(hour=0, minute=0),
            "options": {"queue": "reconciliation", "priority": 8},
            "kwargs": {},
        },
        # Cleanup expired tokens - every hour
        "cleanup_expired_tokens": {
            "task": "app.tasks.reconciliation_tasks.cleanup_expired_tokens_task",
            "schedule": timedelta(hours=1),
            "options": {"queue": "default", "priority": 5},
            "kwargs": {},
        },
        # Alert check for under-reserved - every 6 hours
        "alert_under_reserved": {
            "task": "app.tasks.reconciliation_tasks.alert_under_reserved_task",
            "schedule": timedelta(hours=6),
            "options": {"queue": "reconciliation", "priority": 9},
            "kwargs": {},
        },
    },
)


@celery_app.task(bind=True, name="app.tasks.health_check")
def health_check(self):
    """
    Health check task to verify Celery worker is operational.

    Returns:
        dict: Status information
    """
    try:
        return {
            "status": "healthy",
            "worker": self.request.hostname,
            "timestamp": str(__import__("datetime").datetime.utcnow()),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise


@celery_app.task(bind=True)
def debug_task(self):
    """
    Debug task for testing Celery configuration.

    Returns:
        str: Debug message
    """
    return f"Request: {self.request!r}"


def register_signal_handlers():
    """Register Celery signal handlers for logging and monitoring."""
    from celery.signals import task_prerun, task_postrun, task_failure

    @task_prerun.connect
    def task_prerun_handler(task_id, task, args, kwargs, **kw):
        """Log before task execution."""
        logger.info(
            f"Task started: {task.name}[{task_id}] "
            f"Args: {args} Kwargs: {kwargs}"
        )

    @task_postrun.connect
    def task_postrun_handler(task_id, task, args, kwargs, retval, **kw):
        """Log after task execution."""
        logger.info(f"Task completed: {task.name}[{task_id}] Result: {retval}")

    @task_failure.connect
    def task_failure_handler(task_id, exception, args, kwargs, traceback, **kw):
        """Log task failures."""
        logger.error(
            f"Task failed: {task_id} Exception: {exception} "
            f"Traceback: {traceback}",
            exc_info=True,
        )


# Register signal handlers on module load
register_signal_handlers()

logger.info("Celery app initialized successfully")
logger.info(f"Broker: {settings.CELERY_BROKER_URL}")
logger.info(f"Backend: {settings.CELERY_RESULT_BACKEND}")
