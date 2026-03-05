import json
from src.security import PermissionsException, EncryptionService
from src.persistance import AsyncSessionRepository
from ..repository import UserRepository
from ..services import UsersService
from .schemas import CreateUserRequest
from ..models import User
from ..schemas import UserPublic

class CreateUser:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService,
        session_repository: AsyncSessionRepository,
        encryption: EncryptionService
        
    ):
        self._users_repository = users_repository
        self._users_service = users_service
        self._session_repository = session_repository
        self._encryption = encryption
        

    async def execute(
        self,
        data: CreateUserRequest
    ) -> UserPublic:
        partial_entity = self._users_service.prepare_new_user_data(
            data=data
        )

        key = f"verification:{partial_entity.email_hash}"
        verification = await self._session_repository.get_session(key)
        
        if not verification:
            raise PermissionsException(detail="Verification code expired or not found", status_code=401)
        
        encrypted_code = verification.get("verification_code")
        attempts = verification.get("attempts", 0)

        if not encrypted_code: 
            raise PermissionsException(detail="Verification failed", status_code=401)
        
        if attempts >= 3:
            await self._session_repository.delete_session(key=key)
            raise PermissionsException(detail="Limit reached please request new code", status_code=429)

        if int(self._encryption.decrypt(encrypted_code)) != int(data.verification_code):
            verification["attempts"] = attempts + 1
            
            await self._session_repository.set_session(
                key=key,
                value=json.dumps(verification)
            )

            raise PermissionsException(detail="Verification failed", status_code=401)
         

        await self._session_repository.delete_session(
            key=key
        )

        entity: User = await self._users_repository.create(
            data=partial_entity
        )

        return self._users_service.get_public_schema(entity)

       