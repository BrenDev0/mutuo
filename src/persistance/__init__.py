__version__ = "1.0.0"
__author__ = "BrenDev0"
__description__ = "persistance package for app"

from .exceptions import ResourceNotFoundException, CollisionException
from .repositories import AsyncDataRepository, AsyncSessionRepository

from .utils import (
    require_resource_exists,
    resource_exists
)

from .sqlalchemy.setup import (
    SqlAlchemyBase,
    get_async_session_factory,
    get_async_engine
)
from .sqlalchemy.async_data_repository import AsyncSqlAlchemyDataRepository
from .redis.async_session_repository import AsyncRedisSessionRepository

__all__ = [
    "ResourceNotFoundException",
    "AsyncDataRepository",
    "AsyncSessionRepository",
    "CollisionException",


    "resource_exists",
    "require_resource_exists",
    
    "AsyncRedisSessionRepository",
    "AsyncSqlAlchemyDataRepository",
    "SqlAlchemyBase",
    "get_async_engine",
    "get_async_session_factory",
]