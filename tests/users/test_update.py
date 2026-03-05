import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, Mock
from src.features.users.update.use_case import UpdateUser
from src.features.users.update.schemas import UpdateUserRequest
from src.features.users.models import User
from src.features.users.schemas import UserPublic


@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def mock_service():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    mock_service
):
    return UpdateUser(
        users_repository=mock_repository,
        users_service=mock_service
    )


@pytest.mark.asyncio

async def test_success(
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    user_id = uuid4()
    fake_user = User(
        user_id=user_id,
        name="update_name",
        phone="encrypted",
        email="hashed",
        email_hash="hashedfs",
        profile_type="user",
        password="hashed",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrytpted",
        phone="decrytpted",
        email="email",
        profile_type="user",
        created_at=datetime.now()
    )

    changes = UpdateUserRequest(
        name="updated_name"
    )

    mock_repository.update_one.return_value = fake_user
    mock_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(
        user_id=user_id,
        changes=changes
    )
    

    mock_repository.update_one.assert_called_once_with(
        key="user_id",
        value=user_id,
        changes=changes.model_dump(exclude_none=True, by_alias=False)
    )

    assert isinstance(result, UserPublic)

