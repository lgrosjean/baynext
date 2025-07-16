"""Tests for middleware configuration."""

from typing import Any
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.middleware import (
    _add_cors_middleware,
    _add_security_middleware,
    add_middleware,
)
from app.core.settings import Env

# Constants for status codes
HTTP_200_OK = 200


def find_middleware_by_type(app: FastAPI, middleware_type: type) -> Any:
    """Find middleware by type in the FastAPI app."""
    for middleware in app.user_middleware:
        if middleware.cls == middleware_type:
            return middleware
    return None


class TestCORSMiddleware:
    """Test CORS middleware configuration."""

    def test_cors_middleware_development_mode(self) -> None:
        """Test CORS middleware in development mode allows all origins."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.development):
            _add_cors_middleware(app)

        cors_middleware = find_middleware_by_type(app, CORSMiddleware)

        # Verify middleware was added
        assert cors_middleware is not None, "CORS middleware was not added to the app"

        # Verify development configuration
        expected_origins = ["*"]
        actual_origins = cors_middleware.kwargs["allow_origins"]
        assert actual_origins == expected_origins, (
            f"Expected allow_origins={expected_origins}, got {actual_origins}"
        )

    def test_cors_middleware_production_mode(self) -> None:
        """Test CORS middleware in production mode uses specific domains."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.production):
            _add_cors_middleware(app)

        cors_middleware = find_middleware_by_type(app, CORSMiddleware)

        assert cors_middleware is not None, "CORS middleware was not added to the app"

        expected_origins = [
            "https://yourdomain.com",
            "https://www.yourdomain.com",
        ]
        actual_origins = cors_middleware.kwargs["allow_origins"]

        assert actual_origins == expected_origins, (
            f"Expected specific origins, got {actual_origins}"
        )

    def test_cors_middleware_methods_configuration(self) -> None:
        """Test CORS middleware allows required HTTP methods."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.development):
            _add_cors_middleware(app)

        cors_middleware = find_middleware_by_type(app, CORSMiddleware)

        assert cors_middleware is not None, "CORS middleware was not added to the app"

        methods = cors_middleware.kwargs["allow_methods"]
        required_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

        for method in required_methods:
            assert method in methods, (
                f"Required method {method} not in allowed methods: {methods}"
            )


class TestSecurityMiddleware:
    """Test security middleware configuration."""

    def test_security_middleware_development_mode(self) -> None:
        """Test security middleware in development mode allows all hosts."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.development):
            _add_security_middleware(app)

        trusted_host_middleware = find_middleware_by_type(app, TrustedHostMiddleware)

        assert trusted_host_middleware is not None, (
            "TrustedHost middleware was not added to the app"
        )

        expected_hosts = ["*"]
        actual_hosts = trusted_host_middleware.kwargs["allowed_hosts"]
        assert actual_hosts == expected_hosts, (
            f"Expected allowed_hosts={expected_hosts}, got {actual_hosts}"
        )

    def test_security_middleware_production_mode(self) -> None:
        """Test security middleware in production mode uses specific hosts."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.production):
            _add_security_middleware(app)

        trusted_host_middleware = find_middleware_by_type(app, TrustedHostMiddleware)

        assert trusted_host_middleware is not None, (
            "TrustedHost middleware was not added to the app"
        )

        expected_hosts = [
            "api.mycompany.com",
            "localhost",
            "*.mycompany.internal",
        ]
        actual_hosts = trusted_host_middleware.kwargs["allowed_hosts"]

        assert actual_hosts == expected_hosts, (
            f"Expected specific hosts, got {actual_hosts}"
        )


class TestMiddlewareIntegration:
    """Test complete middleware integration."""

    def test_add_middleware_adds_both_types(self) -> None:
        """Test that add_middleware adds both CORS and security middleware."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.development):
            add_middleware(app)

        cors_middleware = find_middleware_by_type(app, CORSMiddleware)
        trusted_host_middleware = find_middleware_by_type(app, TrustedHostMiddleware)

        assert cors_middleware is not None, "CORS middleware was not added"
        assert trusted_host_middleware is not None, (
            "TrustedHost middleware was not added"
        )

    def test_middleware_execution_order(self) -> None:
        """Test middleware is added in correct order."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", Env.development):
            add_middleware(app)

        middleware_classes = [middleware.cls for middleware in app.user_middleware]

        cors_index = None
        trusted_host_index = None

        for i, cls in enumerate(middleware_classes):
            if cls == CORSMiddleware:
                cors_index = i
            elif cls == TrustedHostMiddleware:
                trusted_host_index = i

        assert cors_index is not None and trusted_host_index is not None, (
            "Both middleware types should be present"
        )

        # Security middleware should be added after CORS (executed before CORS)
        # Since we add CORS first, then security, security has index 0 and CORS has index 1
        assert trusted_host_index < cors_index, (
            "Security middleware should be executed before CORS (lower index)"
        )


class TestMiddlewareBehavior:
    """Test middleware behavior with actual requests."""

    def test_cors_headers_in_response(self) -> None:
        """Test that CORS headers are present in cross-origin API responses."""
        app = FastAPI()

        # Add middleware first
        with patch("app.core.middleware.settings.environment", Env.development):
            add_middleware(app)

        @app.get("/test")
        async def test_endpoint() -> dict[str, str]:
            return {"message": "test"}

        client = TestClient(app)
        # Make a cross-origin request to trigger CORS headers
        response = client.get("/test", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == HTTP_200_OK, (
            f"Expected status {HTTP_200_OK}, got {response.status_code}"
        )
        assert "access-control-allow-origin" in response.headers, (
            "CORS headers not present in cross-origin response"
        )

    def test_cors_preflight_handling(self) -> None:
        """Test CORS preflight OPTIONS request handling."""
        app = FastAPI()

        @app.get("/test")
        async def test_endpoint() -> dict[str, str]:
            return {"message": "test"}

        with patch("app.core.middleware.settings.environment", Env.development):
            add_middleware(app)

        client = TestClient(app)
        response = client.options(
            "/test",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert response.status_code == HTTP_200_OK, (
            f"CORS preflight failed with status {response.status_code}"
        )

        required_headers = [
            "access-control-allow-origin",
            "access-control-allow-methods",
        ]
        for header in required_headers:
            assert header in response.headers, f"Missing CORS header: {header}"

    def test_trusted_host_allows_localhost(self) -> None:
        """Test that localhost is allowed as a trusted host."""
        app = FastAPI()

        @app.get("/test")
        async def test_endpoint() -> dict[str, str]:
            return {"message": "test"}

        with patch("app.core.middleware.settings.environment", Env.development):
            add_middleware(app)

        client = TestClient(app)
        response = client.get("/test", headers={"Host": "localhost"})

        assert response.status_code == HTTP_200_OK, (
            f"Localhost should be allowed, got status {response.status_code}"
        )


class TestEnvironmentVariations:
    """Test middleware behavior across environments."""

    @pytest.mark.parametrize("environment", [Env.production, Env.development])
    def test_cors_configuration_by_environment(self, environment: Env) -> None:
        """Test CORS configuration varies by environment."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", environment):
            _add_cors_middleware(app)

        cors_middleware = find_middleware_by_type(app, CORSMiddleware)

        assert cors_middleware is not None, "CORS middleware should be present"

        origins = cors_middleware.kwargs["allow_origins"]

        if environment == Env.production:
            # Production should NOT allow all origins
            assert "*" not in origins, "Production should not allow all origins (*)"
        else:
            # Development should allow all origins
            assert origins == ["*"], "Development should allow all origins (*)"

    @pytest.mark.parametrize("environment", [Env.production, Env.development])
    def test_security_configuration_by_environment(self, environment: Env) -> None:
        """Test security configuration varies by environment."""
        app = FastAPI()

        with patch("app.core.middleware.settings.environment", environment):
            _add_security_middleware(app)

        trusted_host_middleware = find_middleware_by_type(app, TrustedHostMiddleware)

        assert trusted_host_middleware is not None, (
            "Security middleware should be present"
        )

        hosts = trusted_host_middleware.kwargs["allowed_hosts"]

        if environment == Env.production:
            # Production should NOT allow all hosts
            assert "*" not in hosts, "Production should not allow all hosts (*)"
            assert "api.mycompany.com" in hosts, (
                "Production should include api.mycompany.com"
            )
        else:
            # Development should allow all hosts
            assert hosts == ["*"], "Development should allow all hosts (*)"
