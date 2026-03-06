import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from uuid import uuid4
from src.features.users.delete.use_case import DeleteUser
from src.features.users.models import User
from src.features.users.schemas import UserPublic
from src.persistence import ResourceNotFoundException


@pytest.fixture
def mock_users_repository():
    return AsyncMock()


@pytest.fixture
def mock_users_service():
    return Mock()


@pytest.fixture
def mock_session_repository():
    return AsyncMock()


@pytest.fixture
def use_case(
    mock_users_repository,
    mock_users_service,
    mock_session_repository
):
    return DeleteUser(
        users_repository=mock_users_repository,
        users_service=mock_users_service,
        session_repository=mock_session_repository
    )


@pytest.mark.asyncio
@patch('src.features.users.delete.use_case.require_resource_exists')
async def test_delete_user_success(
    mock_require_exists,
    mock_users_repository,
    mock_users_service,
    mock_session_repository,
    use_case: DeleteUser
):
    user_id = uuid4()
    session_id = uuid4()
    
    fake_deleted_user = User(
        user_id=user_id,
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed",
        profile_type="OWNER",
        password="hashed",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrypted",
        phone="decrypted",
        email="decrypted",
        profile_type="OWNER",
        created_at=datetime.now()
    )

    mock_require_exists.return_value = fake_deleted_user
    mock_users_repository.delete_one.return_value = fake_deleted_user
    mock_users_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(session_id=session_id, user_id=user_id)

    mock_require_exists.assert_called_once_with(
        repository=mock_users_repository,
        key="user_id",
        value=user_id
    )
    
    mock_users_repository.delete_one.assert_called_once_with(
        key="user_id",
        value=user_id
    )
    
    mock_session_repository.delete_session.assert_called_once_with(
        key=str(session_id)
    )
    
    mock_users_service.get_public_schema.assert_called_once_with(entity=fake_deleted_user)

    assert isinstance(result, UserPublic)
    assert result.user_id == user_id
    assert result.name == "decrypted"
    assert result.phone == "decrypted"
    assert result.email == "decrypted"
    assert result.profile_type == "OWNER"


@pytest.mark.asyncio
@patch('src.features.users.delete.use_case.require_resource_exists')
async def test_delete_user_not_found(
    mock_require_exists,
    mock_users_repository,
    mock_users_service,
    mock_session_repository,
    use_case: DeleteUser
):
    user_id = uuid4()
    session_id = uuid4()

    mock_require_exists.side_effect = ResourceNotFoundException(
        detail=f"Resource with user_id: {user_id} not found"
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        await use_case.execute(session_id=session_id, user_id=user_id)
    
    assert f"Resource with user_id: {user_id} not found" in str(exc_info.value)
    
    mock_require_exists.assert_called_once_with(
        repository=mock_users_repository,
        key="user_id",
        value=user_id
    )
    
    mock_users_repository.delete_one.assert_not_called()
    mock_session_repository.delete_session.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()


@pytest.mark.asyncio
@patch('src.features.users.delete.use_case.require_resource_exists')
async def test_delete_user_repository_error(
    mock_require_exists,
    mock_users_repository,
    mock_users_service,
    mock_session_repository,
    use_case: DeleteUser
):
    user_id = uuid4()
    session_id = uuid4()
    
    fake_user = User(
        user_id=user_id,
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed",
        profile_type="OWNER",
        password="hashed",
        created_at=datetime.now()
    )

    mock_require_exists.return_value = fake_user
    mock_users_repository.delete_one.side_effect = Exception("Database error")

    with pytest.raises(Exception) as exc_info:
        await use_case.execute(session_id=session_id, user_id=user_id)
    
    assert "Database error" in str(exc_info.value)
    
    mock_require_exists.assert_called_once_with(
        repository=mock_users_repository,
        key="user_id",
        value=user_id
    )
    
    mock_users_repository.delete_one.assert_called_once_with(
        key="user_id",
        value=user_id
    )
    
    mock_session_repository.delete_session.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()