from uuid import UUID
from src.persistance import ResourceExistsService
from ..repository import UserRepository
from ..services import UsersService


class DeleteUser:
    def __init__(
        self,
        users_repository: UserRepository,
        users_service: UsersService
    ):
        self.__users_repository = users_repository
        self.__users_service = users_service

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
        user_exists_rule = ResourceExistsService(
            repository=self.__users_repository
        )

        await user_exists_rule.validate(
            key="user_id",
            value=user_id,
            throw_error=True
        )
        
        deleted_user = await self.__users_repository.delete_one(
            key="user_id",
            value=user_id
        )

        return self.__users_service.get_public_schema(entity=deleted_user)