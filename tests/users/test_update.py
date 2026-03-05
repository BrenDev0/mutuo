import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from src.features.users.update.use_case import UpdateUser
from src.features.users.update.schemas import UpdateUserRequest
from src.features.users.models import User
from src.features.users.schemas import UserPublic
from src.persistence import ResourceNotFoundException
from src.app import AppException


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
@patch('src.features.users.update.use_case.require_resource_exists')
async def test_success(
    mock_require_exists,
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    user_id = uuid4()
    fake_user = User(
        user_id=user_id,
        name="encrypted_updated_name",
        phone="encrypted_phone",
        email="hashed_email",
        email_hash="hashed_email_hash",
        profile_type="OWNER",
        password="hashed_password",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrypted_updated_name",
        phone="decrypted_phone",
        email="decrypted_email",
        profile_type="OWNER",
        created_at=datetime.now()
    )

    changes = UpdateUserRequest(
        name="updated_name"
    )

    encrypted_changes = {
        "name": "encrypted_updated_name"
    }

    mock_require_exists.return_value = fake_user
    mock_service.prepare_update_data.return_value = encrypted_changes
    mock_repository.update_one.return_value = fake_user
    mock_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(
        user_id=user_id,
        changes=changes
    )

    mock_require_exists.assert_called_once_with(
        repository=mock_repository,
        key="user_id",
        value=user_id
    )

    mock_service.prepare_update_data.assert_called_once_with(
        data=changes
    )

    mock_repository.update_one.assert_called_once_with(
        key="user_id",
        value=user_id,
        changes=encrypted_changes
    )

    mock_service.get_public_schema.assert_called_once_with(entity=fake_user)

    assert isinstance(result, UserPublic)
    assert result == fake_public_schema


@pytest.mark.asyncio
@patch('src.features.users.update.use_case.require_resource_exists')
async def test_user_not_found(
    mock_require_exists,
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    user_id = uuid4()
    changes = UpdateUserRequest(
        name="updated_name"
    )

    mock_require_exists.side_effect = ResourceNotFoundException(
        detail=f"Resource with user_id: {user_id} not found"
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        await use_case.execute(
            user_id=user_id,
            changes=changes
        )

    assert f"Resource with user_id: {user_id} not found" in str(exc_info.value.detail)

    mock_require_exists.assert_called_once_with(
        repository=mock_repository,
        key="user_id",
        value=user_id
    )

    mock_service.prepare_update_data.assert_not_called()
    mock_repository.update_one.assert_not_called()
    mock_service.get_public_schema.assert_not_called()


@pytest.mark.asyncio
@patch('src.features.users.update.use_case.require_resource_exists')
async def test_no_fields_to_update(
    mock_require_exists,
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    """Test that sending null values or empty request raises AppException"""
    user_id = uuid4()
    
    fake_user = User(
        user_id=user_id,
        name="encrypted_name",
        phone="encrypted_phone",
        email="hashed_email",
        email_hash="hashed_email_hash",
        profile_type="OWNER",
        password="hashed_password",
        created_at=datetime.now()
    )

    changes = UpdateUserRequest(
        name=None,
        phone=None
    )

    mock_require_exists.return_value = fake_user
    mock_service.prepare_update_data.side_effect = AppException(
        detail="Request must include at least one non null field to update",
        status_code=400
    )

    with pytest.raises(AppException) as exc_info:
        await use_case.execute(
            user_id=user_id,
            changes=changes
        )

    assert "Request must include at least one non null field to update" in str(exc_info.value.detail)
    assert exc_info.value.status_code == 400

    mock_require_exists.assert_called_once_with(
        repository=mock_repository,
        key="user_id",
        value=user_id
    )

    mock_service.prepare_update_data.assert_called_once_with(
        data=changes
    )

    mock_repository.update_one.assert_not_called()
    mock_service.get_public_schema.assert_not_called()


@pytest.mark.asyncio
@patch('src.features.users.update.use_case.require_resource_exists')
async def test_update_multiple_fields(
    mock_require_exists,
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    user_id = uuid4()
    fake_user = User(
        user_id=user_id,
        name="encrypted_new_name",
        phone="encrypted_new_phone",
        email="hashed_email",
        email_hash="hashed_email_hash",
        profile_type="OWNER",
        password="hashed_password",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrypted_new_name",
        phone="decrypted_new_phone",
        email="decrypted_email",
        profile_type="OWNER",
        created_at=datetime.now()
    )

    changes = UpdateUserRequest(
        name="new_name",
        phone="new_phone"
    )

    encrypted_changes = {
        "name": "encrypted_new_name",
        "phone": "encrypted_new_phone"
    }

    mock_require_exists.return_value = fake_user
    mock_service.prepare_update_data.return_value = encrypted_changes
    mock_repository.update_one.return_value = fake_user
    mock_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(
        user_id=user_id,
        changes=changes
    )

    mock_service.prepare_update_data.assert_called_once_with(
        data=changes
    )

    mock_repository.update_one.assert_called_once_with(
        key="user_id",
        value=user_id,
        changes=encrypted_changes
    )

    assert isinstance(result, UserPublic)
    assert result == fake_public_schema


@pytest.mark.asyncio
@patch('src.features.users.update.use_case.require_resource_exists')
async def test_update_only_name(
    mock_require_exists,
    mock_repository,
    mock_service,
    use_case: UpdateUser
):
    """Test that only fields set in request are updated (exclude_none behavior)"""
    user_id = uuid4()
    fake_user = User(
        user_id=user_id,
        name="encrypted_new_name",
        phone="encrypted_original_phone",
        email="hashed_email",
        email_hash="hashed_email_hash",
        profile_type="OWNER",
        password="hashed_password",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=user_id,
        name="decrypted_new_name",
        phone="decrypted_original_phone",
        email="decrypted_email",
        profile_type="OWNER",
        created_at=datetime.now()
    )

    changes = UpdateUserRequest(
        name="new_name"
    )

    encrypted_changes = {
        "name": "encrypted_new_name"
    }

    mock_require_exists.return_value = fake_user
    mock_service.prepare_update_data.return_value = encrypted_changes
    mock_repository.update_one.return_value = fake_user
    mock_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(
        user_id=user_id,
        changes=changes
    )

    # Verify only name is in encrypted_changes
    call_args = mock_service.prepare_update_data.call_args
    assert call_args[1]["data"].name == "new_name"
    assert call_args[1]["data"].phone is None

    # Verify encrypted_changes only has name
    update_call_args = mock_repository.update_one.call_args
    assert "name" in update_call_args.kwargs["changes"]
    assert "phone" not in update_call_args.kwargs["changes"]

    assert isinstance(result, UserPublic)
    assert result == fake_public_schema