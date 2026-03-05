from src.security import HashingService, IncorrectPassword
from src.persistance import ResourceNotFoundException
from typing import cast
from ..repository import UserRepository
from ..models import User
from ..services import UsersService


class UserLogin:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService,
        hashing: HashingService
    ):
        self.__users_repository = users_repository
        self.__users_service = users_service
        self.__hashing = hashing

    async def execute(
        self,
        email: str,
        password: str
    ):
        hashed_email = self.__hashing.hash_for_search(email)

        user = await self.__users_repository.select_one(
            key="email_hash",
            value=hashed_email
        )

        if not user:
            raise ResourceNotFoundException(detail="Incorrect email or password", status_code=400)
        
        user = cast(User, user)
        
        if not self.__hashing.compare(
            unhashed=password,
            hashed=user.password
        ):
            raise IncorrectPassword(detail="Incorrect email or password", status_code=400)
        
        return self.__users_service.get_public_schema(user)

