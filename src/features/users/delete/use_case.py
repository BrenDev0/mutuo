from uuid import UUID
from src.persistence import require_resource_exists
from ..repository import UserRepository
from ..services import UsersService


class DeleteUser:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService
    ):
        self._users_repository = users_repository
        self._users_service = users_service

    async def execute(
        self,
        user_id: UUID
    ):
        """
        Delete user

        Args:
            user_id: from token 

        Returs: 
            Deleted user schema

        Raises:
            ResourceNotFound exception if no user found in db 
        """
        await require_resource_exists(
            repository=self._users_repository,
            key="user_id",
            value=user_id
        )

        deleted_user = await self._users_repository.delete_one(
            key="user_id",
            value=user_id
        )

        return self._users_service.get_public_schema(entity=deleted_user)