import json
from uuid import uuid4
from src.security import PermissionsException, EncryptionService
from src.persistance import AsyncSessionRepository
from ..repository import UserRepository
from ..services import UsersService
from .schemas import CreateUserRequest, CreateUserResult
from ..models import User

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
        data: CreateUserRequest,
        session_expiration: int
    ):
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

        session_id = uuid4()
        session_data = {
            "user_id": str(entity.user_id),
            "is_authenticated": True
        }
        await self._session_repository.set_session(
            key=str(session_id),
            value=json.dumps(session_data),
            expire_seconds=session_expiration
        )

        public_schema = self._users_service.get_public_schema(entity)

        return CreateUserResult(
            user_public=public_schema,
            session_id=session_id
        )