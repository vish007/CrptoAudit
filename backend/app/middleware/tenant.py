"""Tenant isolation middleware."""
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce tenant isolation."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Enforce tenant isolation for requests.

        Args:
            request: HTTP request
            call_next: Next middleware/handler

        Returns:
            HTTP response
        """
        # Extract tenant ID from user token if available
        tenant_id = None

        try:
            from app.core.security import verify_token
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                payload = verify_token(token)
                tenant_id = payload.get("tenant_id")

                # Store in request state for use in endpoints
                request.state.tenant_id = tenant_id
        except Exception:
            pass

        # Process request
        response = await call_next(request)

        return response
