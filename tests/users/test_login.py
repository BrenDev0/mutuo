import pytest 
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, Mock
from src.features.users.login.use_case import UserLogin
from src.features.users.models import User
from src.features.users.schemas import UserPublic
from src.persistance import ResourceNotFoundException
from src.security import IncorrectPassword

@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_service():
    return Mock()

@pytest.fixture
def mock_hashing():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    mock_service,
    mock_hashing
):
    return UserLogin(
        users_repository=mock_repository,
        users_service=mock_service,
        hashing=mock_hashing
    )



@pytest.mark.asyncio
async def test_success(
    mock_hashing,
    mock_repository,
    mock_service,
    use_case: UserLogin
):
    fake_user = User(
        user_id=uuid4(),
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashedfs",
        profile_type="user",
        password="hashed",
        created_at=datetime.now()
    )

    fake_public_schema = UserPublic(
        user_id=uuid4(),
        name="decrytpted",
        phone="decrytpted",
        email="email",
        profile_type="user",
        created_at=datetime.now()
    )
    mock_hashing.hash_for_search.return_value = "hashed_for_search"
    mock_repository.select_one.return_value = fake_user
    mock_hashing.compare.return_value = True
    mock_service.get_public_schema.return_value = fake_public_schema

    result = await use_case.execute(
        email="email",
        password="password"
    )

    mock_hashing.hash_for_search.assert_called_once_with(
        "email"
    )
    mock_repository.select_one.assert_called_once_with(
        key="email_hash",
        value="hashed_for_search"
    )
    mock_hashing.compare.assert_called_once_with(
        unhashed="password",
        hashed="hashed"
    )

    assert isinstance(result, UserPublic)




@pytest.mark.asyncio
async def test_not_found(
    mock_hashing,
    mock_repository,
    use_case: UserLogin
):
   
    mock_hashing.hash_for_search.return_value = "hashed_for_search"
    mock_repository.select_one.return_value = None

    with pytest.raises(ResourceNotFoundException) as exc_info:

        await use_case.execute(
            email="email",
            password="password"
        )

    mock_hashing.hash_for_search.assert_called_once_with(
        "email"
    )
    mock_repository.select_one.assert_called_once_with(
        key="email_hash",
        value="hashed_for_search"
    )

    assert "Incorrect email" in str(exc_info.value.detail)





@pytest.mark.asyncio
async def test_incorrect_password(
    mock_hashing,
    mock_repository,
    use_case: UserLogin
):
    fake_user = User(
        user_id=uuid4(),
        name="encrypted",
        phone="encrypted",
        email="hashed",
        email_hash="hashedfs",
        profile_type="user",
        password="hashed",
        created_at=datetime.now()
    )

    mock_hashing.hash_for_search.return_value = "hashed_for_search"
    mock_repository.select_one.return_value = fake_user
    mock_hashing.compare.return_value = False

    with pytest.raises(IncorrectPassword) as exc_info:
        await use_case.execute(
            email="email",
            password="wrong_password"
        )

    mock_hashing.hash_for_search.assert_called_once_with(
        "email"
    )
    mock_repository.select_one.assert_called_once_with(
        key="email_hash",
        value="hashed_for_search"
    )
    mock_hashing.compare.assert_called_once_with(
        unhashed="wrong_password",
        hashed="hashed"
    )

    assert "Incorrect email or password" in str(exc_info.value.detail)

