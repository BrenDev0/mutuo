import json
from uuid import uuid4
from src.security import HashingService, IncorrectPassword
from src.persistence import ResourceNotFoundException
from typing import cast
from src.persistence import AsyncSessionRepository
from ..repository import UserRepository
from ..models import User
from ..services import UsersService
from .schemas import LoginResult


class UserLogin:
    def __init__(
        self,
        users_repository: UserRepository,
        session_repository: AsyncSessionRepository,
        users_service: UsersService,
        hashing: HashingService
    ):
        self.__session_repository = session_repository
        self.__users_repository = users_repository
        self.__users_service = users_service
        self.__hashing = hashing

    async def execute(
        self,
        email: str,
        password: str,
        session_expiration: int
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
        
        session_id = uuid4()

        session_data = {
            "user_id": str(user.user_id),
            "is_authenticated": True 
        }

        await self.__session_repository.set_session(
            key=str(session_id),
            value=json.dumps(session_data),
            expire_seconds=session_expiration
        )

        
        public_schema = self.__users_service.get_public_schema(user)
        return LoginResult(
            user_public=public_schema,
            session_id=session_id
        )

