import pytest
import hmac
import hashlib
import time
from fastapi import HTTPException, Request
from unittest.mock import AsyncMock
from src.security.fastapi.hmac import verify_hmac

@pytest.fixture
def mock_request():
    request = AsyncMock(spec=Request)
    request.headers = {}
    return request

@pytest.fixture
def hmac_secret(monkeypatch):
    secret = "test_secret"
    monkeypatch.setenv("HMAC_SECRET", secret)
    return secret

@pytest.fixture
def mock_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "PRODUCTION")

def test_verify_hmac_development_mode(mock_request, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "DEVELOPMENT")
    result = verify_hmac(mock_request)
    assert result is True


def test_verify_hmac_valid_signature(mock_request, hmac_secret, mock_environment):
    timestamp = str(int(time.time() * 1000))
    signature = hmac.new(
        hmac_secret.encode("utf-8"),
        timestamp.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    mock_request.headers = {
        "x-signature": signature,
        "x-payload": timestamp
    }

    result = verify_hmac(mock_request)
    assert result is True


def test_verify_hmac_missing_headers(mock_request, mock_environment, hmac_secret):
    mock_request.headers = {}
    with pytest.raises(HTTPException) as exc:
        verify_hmac(mock_request)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"


def test_verify_hmac_invalid_timestamp(mock_request, hmac_secret, mock_environment):
    mock_request.headers = {
        "x-signature": "invalid_signature",
        "x-payload": "invalid_timestamp"
    }
    with pytest.raises(HTTPException) as exc:
        verify_hmac(mock_request)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"


def test_verify_hmac_expired_timestamp(mock_request, hmac_secret, mock_environment):
    expired_timestamp = str(int(time.time() * 1000) - 60_001)
    signature = hmac.new(
        hmac_secret.encode("utf-8"),
        expired_timestamp.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    mock_request.headers = {
        "x-signature": signature,
        "x-payload": expired_timestamp
    }

    with pytest.raises(HTTPException) as exc:
        verify_hmac(mock_request)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"

def test_verify_hmac_invalid_signature(mock_request, hmac_secret, mock_environment):
    timestamp = str(int(time.time() * 1000))
    invalid_signature = "invalid_signature"

    mock_request.headers = {
        "x-signature": invalid_signature,
        "x-payload": timestamp
    }

    with pytest.raises(HTTPException) as exc:
        verify_hmac(mock_request)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"