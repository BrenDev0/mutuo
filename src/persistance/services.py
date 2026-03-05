from uuid import UUID
from typing import Union
from .repositories import AsyncDataRepository
from .exceptions import ResourceNotFoundException

class ResourceExistsService:
    def __init__(
        self,
        repository: AsyncDataRepository
    ):
        self._repository = repository


    async def validate(
        self,
        key: str,
        value: Union[UUID, str, int],
        throw_error: bool = False
    ):
        resource = await self._repository.select_one(key, value)

        if not resource:
            if throw_error:
                raise ResourceNotFoundException(f"Resource with {key}: {value} not found")
            
            return None
        
        return resource