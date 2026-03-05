from abc import ABC, abstractmethod
from typing import Union, TypeVar, List, Generic, Optional, Dict,Any
from uuid import UUID

E = TypeVar("E")  # Entity/pydantic
M = TypeVar("M")  # SQLAlchemy model


class AsyncDataRepository(ABC, Generic[E, M]):
    @abstractmethod
    async def create(
        self, 
        data: E
    ) -> E:
        raise NotImplementedError

    @abstractmethod
    async def select_one(
        self,
        key: str,
        value: Union[str, int, UUID]
    ) -> E | None:
        raise NotImplementedError
    
    @abstractmethod
    async def select_many(
        self,
        key: str,
        value: Union[str, int, UUID],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[E] | None:
        raise NotImplementedError
    
    @abstractmethod
    async def select_all(
        self,
        key: str,
        value: Union[str, int, UUID],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def update_one(
        self,
        key: str,
        value: Union[str, int, UUID],
        changes: Dict[str, Any]
    ) -> E:
        raise NotImplementedError
    
    @abstractmethod
    async def update_many(
        self,
        key: str,
        value: Union[str, int, UUID],
        changes: Dict[str, Any]
    ) -> List[E] | None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(
        self,
        key: str,
        value: Union[str, int, UUID]
    ) -> E:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_many(
        self,
        key: str,
        value: Union[str, int, UUID]
    ) -> List[E] | None:
        raise NotImplementedError