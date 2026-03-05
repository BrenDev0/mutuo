import pytest
from fastapi import HTTPException
from uuid import UUID, uuid4
from unittest.mock import MagicMock
from fastapi import Request
from src.security.fastapi.auth import user_authentication
from src.security.exceptions import ExpiredToken, InvalidToken

@pytest.fixture
def mock_injector():
    return MagicMock()

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.headers = {}
    return request

def test_user_authentication_valid_token(mock_request, mock_injector):
    mock_request.headers = {"Authorization": "Bearer valid_token"}
    mock_web_token_service = MagicMock()
    mock_web_token_service.decode.return_value = {"user_id": uuid4()}
    mock_injector.inject.return_value = mock_web_token_service

    user_id = user_authentication(mock_request, mock_injector)
    assert isinstance(user_id, UUID)

def test_user_authentication_missing_auth_header(mock_request, mock_injector):
    with pytest.raises(HTTPException) as exc:
        user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unautrhorized. Missing required auth headers"

def test_user_authentication_invalid_auth_header(mock_request, mock_injector):
    mock_request.headers = {"Authorization": "InvalidHeader"}
    with pytest.raises(HTTPException) as exc:
        user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unautrhorized. Missing required auth headers"

def test_user_authentication_invalid_token(mock_request, mock_injector):
    mock_request.headers = {"Authorization": "Bearer invalid_token"}
    mock_web_token_service = MagicMock()
    mock_web_token_service.decode.side_effect = InvalidToken("Invalid token")
    mock_injector.inject.return_value = mock_web_token_service

    with pytest.raises(HTTPException) as exc:
        user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"

def test_user_authentication_expired_token(mock_request, mock_injector):
    mock_request.headers = {"Authorization": "Bearer expired_token"}
    mock_web_token_service = MagicMock()
    mock_web_token_service.decode.side_effect = ExpiredToken("Token expired")
    mock_injector.inject.return_value = mock_web_token_service

    with pytest.raises(HTTPException) as exc:
        user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token expired"

def test_user_authentication_missing_user_id(mock_request, mock_injector):
    mock_request.headers = {"Authorization": "Bearer valid_token"}
    mock_web_token_service = MagicMock()
    mock_web_token_service.decode.return_value = {}
    mock_injector.inject.return_value = mock_web_token_service

    with pytest.raises(HTTPException) as exc:
        user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"