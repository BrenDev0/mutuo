from uuid import UUID
from ..services import UsersService
from ..repository import UserRepository
from .schemas import UpdateUserRequest


class UpdateUser:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService
    ):
        self.__users_repository = users_repository
        self.__users_service = users_service

    async def execute(
        self,
        user_id: UUID,
        changes: UpdateUserRequest
    ): 
        updated_user = await self.__users_repository.update_one(
            key="user_id",
            value=user_id,
            changes=changes.model_dump(exclude_none=True, by_alias=False)
        )

        return self.__users_service.get_public_schema(entity=updated_user)