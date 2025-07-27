from fastapi import status
from fastapi.exceptions import HTTPException

from app.core.exceptions import ForbiddenError, UnauthorizedError


def test_forbidden_error_inherits_http_exception():
    err = ForbiddenError("Invalid token")
    assert isinstance(err, HTTPException)
    assert err.status_code == status.HTTP_403_FORBIDDEN
    assert err.detail == "Invalid token"
    assert err.headers == {"WWW-Authenticate": "Bearer"}


def test_unauthorized_error_inherits_http_exception():
    err = UnauthorizedError("Missing credentials")
    assert isinstance(err, HTTPException)
    assert err.status_code == status.HTTP_401_UNAUTHORIZED
    assert err.detail == "Missing credentials"
    assert err.headers == {"WWW-Authenticate": "Bearer"}


def test_forbidden_error_str():
    err = ForbiddenError("Some details")
    assert "Some details" in str(err)


def test_unauthorized_error_str():
    err = UnauthorizedError("Other details")
    assert "Other details" in str(err)
