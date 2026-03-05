import pytest
import json
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from uuid import uuid4
from src.features.users.create.use_case import CreateUser
from src.features.users.create.schemas import CreateUserRequest, CreateUserResult
from src.features.users.services import UsersService
from src.features.users.models import User
from src.features.users.schemas import UserPublic
from src.security import PermissionsException


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
def mock_encryption():
    return Mock()

@pytest.fixture
def use_case(
    mock_users_repository,
    mock_users_service,
    mock_session_repository,
    mock_encryption
):
    return CreateUser(
        users_repository=mock_users_repository,
        users_service=mock_users_service,
        session_repository=mock_session_repository,
        encryption=mock_encryption
    )


@pytest.mark.asyncio
async def test_success(
    mock_users_repository,
    mock_users_service: UsersService,
    mock_session_repository,
    mock_encryption,
    use_case: CreateUser
):
    user_id = uuid4()
    verification_code = 123456
    session_expiration = 259200
    
    fake_user = User(
        user_id=user_id,
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed_email",
        profile_type="OWNER",
        password="hashed",
        created_at=datetime.now()
    )

    fake_request_data = CreateUserRequest(
        verification_code=verification_code,
        name="name",
        phone="phone",
        email="email",
        password="password",
        profile_type="OWNER"
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrypted",
        phone="decrypted",
        email="decrypted",
        profile_type="OWNER",
        created_at=datetime.now()
    )

    mock_users_service.prepare_new_user_data.return_value = User(
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed_email",
        profile_type="OWNER",
        password="hashed",
    )

    mock_session_repository.get_session.return_value = {
        "verification_code": "encrypted_123456",
        "attempts": 0
    }

    mock_encryption.decrypt.return_value = "123456"

    mock_users_service.get_public_schema.return_value = fake_public_schema

    mock_users_repository.create.return_value = fake_user

    result = await use_case.execute(
        data=fake_request_data,
        session_expiration=session_expiration
    )

    mock_users_service.prepare_new_user_data.assert_called_once_with(
        data=fake_request_data
    )
    
    mock_session_repository.get_session.assert_called_once_with("verification:hashed_email")
    
    mock_encryption.decrypt.assert_called_once_with("encrypted_123456")
    
    mock_session_repository.delete_session.assert_called_with(key="verification:hashed_email")
    
    mock_users_repository.create.assert_called_once()
    
    mock_users_service.get_public_schema.assert_called_once_with(fake_user)

    assert isinstance(result, CreateUserResult)
    assert result.user_public == fake_public_schema
    assert result.session_id is not None


@pytest.mark.asyncio
async def test_verification_code_not_found(
    mock_users_repository,
    mock_users_service: UsersService,
    mock_session_repository,
    mock_encryption,
    use_case: CreateUser
):
    fake_request_data = CreateUserRequest(
        verification_code=123456,
        name="name",
        phone="phone",
        email="email",
        password="password",
        profile_type="OWNER"
    )

    mock_users_service.prepare_new_user_data.return_value = User(
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed_email",
        profile_type="OWNER",
        password="hashed",
    )

    mock_session_repository.get_session.return_value = None

    with pytest.raises(PermissionsException) as exc_info:
        await use_case.execute(
            data=fake_request_data,
            session_expiration=259200
        )
    
    assert exc_info.value.detail == "Verification code expired or not found"
    assert exc_info.value.status_code == 401
    
    mock_users_repository.create.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()


@pytest.mark.asyncio
async def test_verification_code_mismatch(
    mock_users_repository,
    mock_users_service: UsersService,
    mock_session_repository,
    mock_encryption,
    use_case: CreateUser
):
    fake_request_data = CreateUserRequest(
        verification_code=999999,
        name="name",
        phone="phone",
        email="email",
        password="password",
        profile_type="OWNER"
    )

    mock_users_service.prepare_new_user_data.return_value = User(
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed_email",
        profile_type="OWNER",
        password="hashed",
    )

    mock_session_repository.get_session.return_value = {
        "verification_code": "encrypted_123456",
        "attempts": 0
    }

    mock_encryption.decrypt.return_value = "123456"

    with pytest.raises(PermissionsException) as exc_info:
        await use_case.execute(
            data=fake_request_data,
            session_expiration=259200
        )
    
    assert exc_info.value.detail == "Verification failed"
    assert exc_info.value.status_code == 401
    
    mock_session_repository.set_session.assert_called_once()
    
    mock_users_repository.create.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()


@pytest.mark.asyncio
async def test_too_many_attempts(
    mock_users_repository,
    mock_users_service: UsersService,
    mock_session_repository,
    mock_encryption,
    use_case: CreateUser
):
    fake_request_data = CreateUserRequest(
        verification_code=123456,
        name="name",
        phone="phone",
        email="email",
        password="password",
        profile_type="OWNER"
    )

    mock_users_service.prepare_new_user_data.return_value = User(
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed_email",
        profile_type="OWNER",
        password="hashed",
    )

    mock_session_repository.get_session.return_value = {
        "verification_code": "encrypted_123456",
        "attempts": 3
    }

    with pytest.raises(PermissionsException) as exc_info:
        await use_case.execute(
            data=fake_request_data,
            session_expiration=259200
        )
    
    assert exc_info.value.detail == "Limit reached please request new code"
    assert exc_info.value.status_code == 429
    
    mock_session_repository.delete_session.assert_called_once_with(key="verification:hashed_email")
    
    mock_users_repository.create.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()