"""Audit logging middleware."""
import json
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import AuditLog
from app.core.database import async_session_maker


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Middleware to log all API actions."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log to audit trail.

        Args:
            request: HTTP request
            call_next: Next middleware/handler

        Returns:
            HTTP response
        """
        # Extract user info from token if available
        user_id = None
        ip_address = request.client.host if request.client else None

        # Try to get user ID from JWT token
        try:
            from app.core.security import verify_token
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                payload = verify_token(token)
                user_id = payload.get("sub")
        except Exception:
            pass

        # Process request
        response = await call_next(request)

        # Log to database (async, non-blocking)
        try:
            # Only log mutations (POST, PUT, DELETE)
            if request.method in ["POST", "PUT", "DELETE"]:
                async with async_session_maker() as session:
                    # Extract resource from path
                    path_parts = request.url.path.split("/")
                    resource = path_parts[-1] if path_parts else "unknown"

                    audit_log = AuditLog(
                        user_id=user_id,
                        action=request.method,
                        resource=resource,
                        resource_id="",
                        ip_address=ip_address,
                        user_agent=request.headers.get("User-Agent", ""),
                        status="SUCCESS" if response.status_code < 400 else "FAILURE",
                    )

                    session.add(audit_log)
                    await session.commit()
        except Exception:
            # Don't fail the request if logging fails
            pass

        return response
