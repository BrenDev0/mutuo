import pytest
from fastapi import HTTPException
from uuid import UUID, uuid4
from unittest.mock import MagicMock, AsyncMock
from fastapi import Request
from src.security.fastapi.auth import user_authentication


@pytest.fixture
def mock_injector():
    return MagicMock()

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.cookies = {}
    return request

@pytest.mark.asyncio
async def test_user_authentication_valid_session(mock_request, mock_injector):
    session_id = str(uuid4())
    user_id = str(uuid4())
    
    mock_request.cookies = {"session_id": session_id}
    
    mock_session_repository = AsyncMock()
    mock_session_repository.get_session.return_value = {
        "user_id": user_id,
        "is_authenticated": True
    }
    mock_injector.inject.return_value = mock_session_repository

    result = await user_authentication(mock_request, mock_injector)
    
    assert isinstance(result, UUID)
    assert str(result) == user_id
    mock_session_repository.get_session.assert_called_once_with(session_id)

@pytest.mark.asyncio
async def test_user_authentication_missing_cookie(mock_request, mock_injector):
    with pytest.raises(HTTPException) as exc:
        await user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"

@pytest.mark.asyncio
async def test_user_authentication_invalid_session(mock_request, mock_injector):
    session_id = str(uuid4())
    mock_request.cookies = {"session_id": session_id}
    
    mock_session_repository = AsyncMock()
    mock_session_repository.get_session.return_value = None
    mock_injector.inject.return_value = mock_session_repository

    with pytest.raises(HTTPException) as exc:
        await user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"

@pytest.mark.asyncio
async def test_user_authentication_expired_session(mock_request, mock_injector):
    session_id = str(uuid4())
    mock_request.cookies = {"session_id": session_id}
    
    mock_session_repository = AsyncMock()
    mock_session_repository.get_session.return_value = None
    mock_injector.inject.return_value = mock_session_repository

    with pytest.raises(HTTPException) as exc:
        await user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"

@pytest.mark.asyncio
async def test_user_authentication_missing_user_id(mock_request, mock_injector):
    session_id = str(uuid4())
    mock_request.cookies = {"session_id": session_id}
    
    mock_session_repository = AsyncMock()
    mock_session_repository.get_session.return_value = {
        "is_authenticated": True
    }
    mock_injector.inject.return_value = mock_session_repository

    with pytest.raises(HTTPException) as exc:
        await user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"

@pytest.mark.asyncio
async def test_user_authentication_not_authenticated(mock_request, mock_injector):
    session_id = str(uuid4())
    user_id = str(uuid4())
    mock_request.cookies = {"session_id": session_id}
    
    mock_session_repository = AsyncMock()
    mock_session_repository.get_session.return_value = {
        "user_id": user_id,
        "is_authenticated": False
    }
    mock_injector.inject.return_value = mock_session_repository

    with pytest.raises(HTTPException) as exc:
        await user_authentication(mock_request, mock_injector)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"