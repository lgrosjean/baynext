"""Middleware configuration for the FastAPI application.

This module centralizes all middleware configuration to keep main.py clean
and make middleware management more organized.
"""

from typing import TYPE_CHECKING

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .settings import settings

if TYPE_CHECKING:
    from fastapi import FastAPI


def _add_cors_middleware(app: "FastAPI") -> None:
    """Add CORS middleware to the FastAPI application."""
    cors_origins = ["*"] if not settings.is_prod() else settings.ALLOWED_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )


def _add_security_middleware(app: "FastAPI") -> None:
    """Add security middleware to the FastAPI application."""
    trusted_hosts = (
        ["*"]
        if not settings.is_prod()
        else [
            "api.mycompany.com",
            "localhost",
            "*.mycompany.internal",
        ]
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=trusted_hosts,
    )


def add_middleware(app: "FastAPI") -> None:
    """Add all middleware to the FastAPI application.

    Middleware is added in reverse order of execution.
    Security middleware should be added first.

    Args:
        app: The FastAPI application instance

    """
    # Security middleware should be added after CORS (executed before CORS)
    _add_cors_middleware(app)
    _add_security_middleware(app)
