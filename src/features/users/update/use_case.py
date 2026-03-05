from uuid import UUID
from src.persistence import require_resource_exists
from ..services import UsersService
from ..schemas import UserPublic
from ..repository import UserRepository
from .schemas import UpdateUserRequest


class UpdateUser:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService
    ):
        self._users_repository = users_repository
        self._users_service = users_service

    async def execute(
        self,
        user_id: UUID,
        changes: UpdateUserRequest
    ) -> UserPublic: 
        await require_resource_exists(
            repository=self._users_repository,
            key="user_id",
            value=user_id
        )

        encrypted_data = self._users_service.prepare_update_data(
            data=changes
        )
        
        updated_user = await self._users_repository.update_one(
            key="user_id",
            value=user_id,
            changes=encrypted_data
        )

        return self._users_service.get_public_schema(entity=updated_user)