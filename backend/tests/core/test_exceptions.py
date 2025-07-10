from fastapi import status
from fastapi.exceptions import HTTPException

from app.core.exceptions import AuthError, UnauthoriedError


def test_auth_error_inherits_http_exception():
    err = AuthError("Invalid token")
    assert isinstance(err, HTTPException)
    assert err.status_code == status.HTTP_403_FORBIDDEN
    assert err.detail == "Invalid token"
    assert err.headers == {"WWW-Authenticate": "Bearer"}


def test_unauthoried_error_inherits_http_exception():
    err = UnauthoriedError("Missing credentials")
    assert isinstance(err, HTTPException)
    assert err.status_code == status.HTTP_401_UNAUTHORIZED
    assert err.detail == "Missing credentials"
    assert err.headers == {"WWW-Authenticate": "Bearer"}


def test_auth_error_str():
    err = AuthError("Some details")
    assert "Some details" in str(err)


def test_unauthoried_error_str():
    err = UnauthoriedError("Other details")
    assert "Other details" in str(err)
