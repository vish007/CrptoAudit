"""
OpenTelemetry instrumentation middleware for FastAPI.

Provides comprehensive observability for the SimplyFI PoR platform including:
- Request tracing with span creation
- Request/response metrics collection
- Custom business metrics
- Error tracking with stack traces
"""

import json
import logging
import time
import traceback
from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from opentelemetry import metrics, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPTraceExporter
from prometheus_client import Counter, Histogram, Gauge
import starlette.middleware.base
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

# Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0)
)

http_request_size_bytes = Histogram(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method', 'endpoint'],
    buckets=(100, 1000, 10000, 100000, 1000000)
)

http_response_size_bytes = Histogram(
    'http_response_size_bytes',
    'HTTP response size in bytes',
    ['method', 'endpoint'],
    buckets=(100, 1000, 10000, 100000, 1000000)
)

# Business metrics
por_active_engagements = Gauge(
    'por_active_engagements',
    'Number of active audit engagements'
)

por_blockchain_verifications_total = Counter(
    'por_blockchain_verifications_total',
    'Total blockchain verification attempts'
)

por_blockchain_verifications_successful = Counter(
    'por_blockchain_verifications_successful',
    'Successful blockchain verifications'
)

por_blockchain_verifications_failed = Counter(
    'por_blockchain_verifications_failed',
    'Failed blockchain verifications'
)

por_reserve_ratio = Gauge(
    'por_reserve_ratio',
    'Current reserve ratio',
    ['asset_type', 'tier']
)

por_merkle_tree_generation_duration_seconds = Histogram(
    'por_merkle_tree_generation_duration_seconds',
    'Merkle tree generation duration in seconds',
    ['tree_size'],
    buckets=(0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0)
)

por_merkle_tree_generation_failures_total = Counter(
    'por_merkle_tree_generation_failures_total',
    'Total merkle tree generation failures',
    ['reason']
)

por_reconciliation_variance = Gauge(
    'por_reconciliation_variance',
    'Reconciliation variance percentage'
)

por_ai_inference_duration_seconds = Histogram(
    'por_ai_inference_duration_seconds',
    'AI model inference duration in seconds',
    ['model_name'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0)
)

por_anomaly_detection_accuracy = Gauge(
    'por_anomaly_detection_accuracy',
    'Anomaly detection model accuracy'
)

por_compliance_engine_score = Gauge(
    'por_compliance_engine_score',
    'Compliance engine score',
    ['rule_set']
)

http_errors_total = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'status', 'error_type']
)

# OpenTelemetry setup
class TelemetrySetup:
    """Configure OpenTelemetry for the SimplyFI PoR platform."""

    def __init__(
        self,
        service_name: str = "simplyfi-por-platform",
        jaeger_host: str = "localhost",
        jaeger_port: int = 6831,
        otel_exporter_otlp_endpoint: Optional[str] = None,
        environment: str = "production"
    ):
        """
        Initialize telemetry setup.

        Args:
            service_name: Name of the service for traces
            jaeger_host: Jaeger collector host
            jaeger_port: Jaeger collector port
            otel_exporter_otlp_endpoint: OTLP exporter endpoint
            environment: Environment name (dev, staging, production)
        """
        self.service_name = service_name
        self.jaeger_host = jaeger_host
        self.jaeger_port = jaeger_port
        self.otel_exporter_otlp_endpoint = otel_exporter_otlp_endpoint or "localhost:4317"
        self.environment = environment

    def configure_tracing(self) -> TracerProvider:
        """Configure OpenTelemetry tracing."""
        resource = Resource.create({
            SERVICE_NAME: self.service_name,
            "environment": self.environment,
        })

        jaeger_exporter = JaegerExporter(
            agent_host_name=self.jaeger_host,
            agent_port=self.jaeger_port,
        )

        otlp_exporter = OTLPTraceExporter(
            endpoint=self.otel_exporter_otlp_endpoint,
            insecure=True,
        )

        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        trace.set_tracer_provider(tracer_provider)
        return tracer_provider

    def configure_metrics(self) -> MeterProvider:
        """Configure OpenTelemetry metrics."""
        otlp_exporter = OTLPMetricExporter(
            endpoint=self.otel_exporter_otlp_endpoint,
            insecure=True,
        )

        prometheus_reader = PrometheusMetricReader()

        metric_provider = MeterProvider(
            resource=Resource.create({
                SERVICE_NAME: self.service_name,
                "environment": self.environment,
            }),
            metric_readers=[
                prometheus_reader,
                PeriodicExportingMetricReader(otlp_exporter),
            ]
        )

        metrics.set_meter_provider(metric_provider)
        return metric_provider

    def setup(self) -> None:
        """Complete OpenTelemetry setup."""
        logger.info(f"Configuring telemetry for {self.service_name}")
        self.configure_tracing()
        self.configure_metrics()
        logger.info("Telemetry configured successfully")


def setup_instrumentation() -> None:
    """Set up automatic instrumentation for common libraries."""
    try:
        FastAPIInstrumentor().instrument()
        RequestsInstrumentor().instrument()
        SQLAlchemyInstrumentor().instrument()
        RedisInstrumentor().instrument()
        CeleryInstrumentor().instrument()
        logger.info("Auto-instrumentation setup completed")
    except Exception as e:
        logger.error(f"Error setting up auto-instrumentation: {e}")


class TelemetryMiddleware(starlette.middleware.base.BaseHTTPMiddleware):
    """Custom middleware for detailed telemetry collection."""

    def __init__(
        self,
        app: ASGIApp,
        tracer_provider: Optional[TracerProvider] = None,
    ):
        """
        Initialize telemetry middleware.

        Args:
            app: ASGI application
            tracer_provider: OpenTelemetry tracer provider
        """
        super().__init__(app)
        self.tracer = (tracer_provider or trace.get_tracer_provider()).get_tracer(__name__)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """
        Process request with telemetry.

        Args:
            request: Incoming request
            call_next: Next middleware/handler

        Returns:
            Response with telemetry data
        """
        start_time = time.time()
        request_size = 0

        # Get request body size if available
        try:
            body = await request.body()
            request_size = len(body)
        except Exception:
            pass

        # Extract relevant information
        method = request.method
        endpoint = request.url.path
        tenant_id = request.headers.get("X-Tenant-ID", "unknown")
        user_role = request.headers.get("X-User-Role", "unknown")
        engagement_id = request.headers.get("X-Engagement-ID")

        # Create span with custom attributes
        with self.tracer.start_as_current_span(f"{method} {endpoint}") as span:
            span.set_attribute("http.method", method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http.client_ip", request.client.host if request.client else "unknown")
            span.set_attribute("tenant_id", tenant_id)
            span.set_attribute("user_role", user_role)
            if engagement_id:
                span.set_attribute("engagement_id", engagement_id)

            try:
                response = await call_next(request)

                # Record metrics
                duration = time.time() - start_time
                status_code = response.status_code

                http_requests_total.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status_code
                ).inc()

                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status_code
                ).observe(duration)

                http_request_size_bytes.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(request_size)

                # Estimate response size
                response_size = response.headers.get("content-length")
                if response_size:
                    http_response_size_bytes.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(int(response_size))

                # Set span attributes
                span.set_attribute("http.status_code", status_code)
                span.set_attribute("http.duration_ms", duration * 1000)

                # Log errors
                if status_code >= 400:
                    error_type = "client_error" if status_code < 500 else "server_error"
                    http_errors_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=status_code,
                        error_type=error_type
                    ).inc()
                    span.set_attribute("error", True)
                    span.set_attribute("error.status_code", status_code)

                return response

            except Exception as e:
                duration = time.time() - start_time

                # Record error metrics
                http_errors_total.labels(
                    method=method,
                    endpoint=endpoint,
                    status="error",
                    error_type="exception"
                ).inc()

                # Record exception in span
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                span.set_attribute("error.stack", traceback.format_exc())

                logger.error(
                    f"Request failed: {method} {endpoint}",
                    exc_info=True,
                    extra={
                        "tenant_id": tenant_id,
                        "duration": duration,
                        "error": str(e)
                    }
                )

                raise


def setup_telemetry(
    app: FastAPI,
    service_name: str = "simplyfi-por-platform",
    jaeger_host: str = "localhost",
    jaeger_port: int = 6831,
    otel_exporter_otlp_endpoint: Optional[str] = None,
    environment: str = "production"
) -> None:
    """
    Complete telemetry setup for FastAPI application.

    Args:
        app: FastAPI application instance
        service_name: Name of the service
        jaeger_host: Jaeger collector host
        jaeger_port: Jaeger collector port
        otel_exporter_otlp_endpoint: OTLP exporter endpoint
        environment: Environment name
    """
    # Configure OpenTelemetry
    telemetry = TelemetrySetup(
        service_name=service_name,
        jaeger_host=jaeger_host,
        jaeger_port=jaeger_port,
        otel_exporter_otlp_endpoint=otel_exporter_otlp_endpoint,
        environment=environment
    )
    telemetry.setup()

    # Setup auto-instrumentation
    setup_instrumentation()

    # Add custom middleware
    tracer_provider = trace.get_tracer_provider()
    app.add_middleware(TelemetryMiddleware, tracer_provider=tracer_provider)

    logger.info(f"Telemetry setup completed for {service_name}")
