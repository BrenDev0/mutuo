import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from uuid import uuid4
from src.features.users.create.use_case import CreateUser
from src.features.users.create.schemas import CreateUserRequest
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
def use_case(
    mock_users_repository,
    mock_users_service
):
    return CreateUser(
        users_repository=mock_users_repository,
        users_service=mock_users_service
    )


@pytest.mark.asyncio
async def test_success(
    mock_users_repository,
    mock_users_service: UsersService,
    use_case: CreateUser
):
    user_id = uuid4()
    verification_code = 123456
    
    fake_user = User(
        user_id=user_id,
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashed",
        profile_type="OWNER",
        password="hashed",
        last_login=datetime.now(),
        created_at=datetime.now()
    )

    fake_request_data = CreateUserRequest(
        verification_code=verification_code,
        name="name",
        phone="phone",
        email="email",
        password="password"
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
        email_hash="hashed",
        profile_type="OWNER",
        password="hashed",
    )

    mock_users_service.get_public_schema.return_value = fake_public_schema

    mock_users_repository.create.return_value = fake_user

    # Pass verification_code as first argument
    result = await use_case.execute(
        verification_code=verification_code,
        data=fake_request_data,
        profile_type="OWNER"
    )

    mock_users_service.prepare_new_user_data.assert_called_once_with(
        data=fake_request_data,
        profile_type="OWNER"
    )
    
    mock_users_repository.create.assert_called_once()
    
    mock_users_service.get_public_schema.assert_called_once_with(fake_user)

    assert result.name == "decrypted"
    assert result.phone == "decrypted"
    assert result.email == "decrypted"
    assert result.profile_type == "OWNER"


@pytest.mark.asyncio
async def test_verification_code_mismatch(
    mock_users_repository,
    mock_users_service: UsersService,
    use_case: CreateUser
):
    """Test that mismatched verification codes raise PermissionsException."""
    
    fake_request_data = CreateUserRequest(
        verification_code=999999,  # Different from what we pass
        name="name",
        phone="phone",
        email="email",
        password="password"
    )

    with pytest.raises(PermissionsException) as exc_info:
        await use_case.execute(
            verification_code=123456,  # Does not match request data
            data=fake_request_data,
            profile_type="OWNER"
        )
    
    assert exc_info.value.detail == "Verification failed"
    assert exc_info.value.status_code == 401
    
    # Ensure repository and service were never called
    mock_users_repository.create.assert_not_called()
    mock_users_service.prepare_new_user_data.assert_not_called()
    mock_users_service.get_public_schema.assert_not_called()