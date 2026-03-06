from src.security import EncryptionService, HashingService
from src.app import AppException
from typing import cast, Any, Dict
from uuid import UUID
from datetime import datetime
from .models import User
from .schemas import UserPublic
from .repository import UserRepository
from .rules import EmailAvailability
from .create.schemas import CreateUserRequest
from .update.schemas import UpdateUserRequest

class UsersService:
    def __init__(
        self,
        hashing: HashingService,
        encryption: EncryptionService
    ):
        self.__hashing = hashing
        self.__encryption = encryption
        
    def get_public_schema(
        self,
        entity: User
    ) -> UserPublic:
        return UserPublic(
            user_id=cast(UUID, entity.user_id),
            email=self.__encryption.decrypt(entity.email),
            name=self.__encryption.decrypt(entity.name),
            phone=self.__encryption.decrypt(entity.phone),
            profile_type=entity.profile_type,
            created_at=cast(datetime, entity.created_at)
        )
    
    def prepare_new_user_data(
        self,
        data: CreateUserRequest
    ) -> User:
        encrypted_email = self.__encryption.encrypt(data.email)
        encrypted_name = self.__encryption.encrypt(data.name)
        encrypted_phone = self.__encryption.encrypt(data.phone)

        hashed_password = self.__hashing.hash(data.password)
        hashed_email = self.__hashing.hash_for_search(data.email)

        partial_entity = User(
            name=encrypted_name,
            phone=encrypted_phone,
            email=encrypted_email,
            email_hash=hashed_email,
            profile_type=data.profile_type.upper(),
            password=hashed_password
        )

        return partial_entity
    
    def prepare_update_data(
        self,
        data: UpdateUserRequest
    ) -> Dict[str, Any]:
        model_dict = data.model_dump(exclude_none=True)

        if not model_dict:
            raise AppException(
                detail="Request must include at least one non null field to update",
                status_code=400
            )
        
        encrypted_dict = {}

        for key, value in model_dict.items():
            encrypted_dict[key] = self.__encryption.encrypt(value)
        
        return encrypted_dict



class EmailAvailabilityService(EmailAvailability):
    def __init__(
        self,
        users_repository: UserRepository
    ):
        self._users_repository = users_repository

    
    async def validate(self, email_hash: str) -> bool:
        """
        Check if email is available for registration.
        
        Args:
            email: Email address to validate.
        
        Returns:
            True if email is available (not in use), False if already exists.
        """

        email_in_use = await self._users_repository.select_one(
            key="email_hash",
            value=email_hash
        )

        return email_in_use is None