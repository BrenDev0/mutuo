from uuid import UUID
from typing import Union, Any
from .repositories import AsyncDataRepository
from .exceptions import ResourceNotFoundException


async def resource_exists(
    repository: AsyncDataRepository,
    key: str,
    value: Union[UUID, str, int]
) -> bool:
    """
    Check if a resource exists in the repository.
    
    Args:
        repository: The repository to check
        key: The field name to search by
        value: The value to search for
    
    Returns:
        True if resource exists, False otherwise
    """
    resource = await repository.select_one(key=key, value=value)
    return resource is not None


async def require_resource_exists(
    repository: AsyncDataRepository,
    key: str,
    value: Union[UUID, str, int]
) -> Any:
    """
    Ensure a resource exists, or raise an exception.
    
    Args:
        repository: The repository to check
        key: The field name to search by
        value: The value to search for
    
    Returns:
        The resource if found
        
    Raises:
        ResourceNotFoundException: If resource not found
    """
    resource = await repository.select_one(key=key, value=value)

    if not resource:
        raise ResourceNotFoundException(
            detail=f"Resource with {key}: {value} not found"
        )
    
    return resource