import logging
from sqlalchemy import select, update, delete
from uuid import UUID
from typing import TypeVar, List, Type, Union, Optional, Dict, Any
from ..repositories import AsyncDataRepository
from .setup import get_async_session_factory

logger = logging.getLogger(__name__)

E = TypeVar("E") # Entity/pydantic
M = TypeVar("M") # sqlalchemy model

class AsyncSqlAlchemyDataRepository(AsyncDataRepository[E, M]):
    def __init__(self, model: Type[M]):
        self.__model = model
        self.__session_factory = get_async_session_factory()

    async def create(
        self, 
        entity: E
    ) -> E:
        try:
            async with self.__session_factory() as session:

                model = self._to_model(entity)
                session.add(model)
                await session.commit()
                await session.refresh(model)
            
                return self._to_entity(model)
        
        except Exception as e:
            logger.error(f"Error Inserting {self.__model.__name__}: {e}", exc_info=True)
            await session.rollback()
            raise



    async def select_one(
        self, 
        key: str, 
        value: Union[str, int, UUID]
    ) -> E | None:
        async with self.__session_factory() as session:
            stmt = select(self.__model).where(getattr(self.__model, key) == value)

            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            return self._to_entity(model) if model else None


    async def select_many(
        self, 
        key: str, 
        value: Union[str, int, UUID], 
        limit: Optional[int] = None, 
        offset: Optional[int] = None
    ) -> List[E] | None:
        async with self.__session_factory() as session:
            stmt = select(self.__model).where(getattr(self.__model, key) == value)

            if limit:
                stmt.limit(limit)

            if offset:
                stmt.offset(offset)

            result = await session.execute(stmt)
            models = result.scalars().all()

            return [
                self._to_entity(model) for model in models 
            ] if result else None

    async def select_all(
        self, 
        key: str, 
        value: Union[str, int, UUID], 
        limit: Optional[int] = None, 
        offset: Optional[int] = None
    ) -> List[E] | None:
        async with self.__session_factory() as session:
            stmt = select(self.__model).where(getattr(self.__model, key) == value)

            if limit:
                stmt.limit(limit)
            
            if offset:
                stmt.offset(offset)
            
            result = await session.execute(stmt)

            return [
                self._to_entity(row) for row in result
            ] if result else None

    async def update_one(
        self, 
        key: str, 
        value: Union[str, int, UUID], 
        changes: Dict[str, Any]
    ) -> E:
        async with self.__session_factory() as session:
            try:
                stmt = update(self.__model).where(getattr(self.__model, key) == value).values(**changes).returning(self.__model)

                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                await session.commit()

                return self._to_entity(model)
            
            except Exception as e:
                logger.error(f"Error updating {self.__model.__name__}: {e}", exc_info=True)
                await session.rollback()
                raise

    async def update_many(
        self, 
        key: str, 
        value: Union[str, int, UUID],
        changes: Dict[str, Any]
    ) -> List[E]:
        try:
            async with self.__session_factory() as session:
                stmt = update(self.__model).where(getattr(self.__model, key) == value).values(**changes).returning(self.__model)

                result = await session.execute(stmt)
                models = result.scalars().all()

                await session.commit()

                return [
                    self._to_entity(model) for model in models
                ]
        
        except Exception as e:
            logger.error(f"Error Updating {self.__model.__name__}: {e}", exc_info=True)
            await session.rollback()
            raise

    async def delete_one(
        self, 
        key: str, 
        value: Union[str, int, UUID]
    ) -> E:
        try:
            async with self.__session_factory() as session:
                stmt = delete(self.__model).where(getattr(self.__model, key) == value).returning(self.__model)

                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                await session.commit()

                return self._to_entity(model)
        
        except Exception as e:
            logger.error(f"Error deleting {self.__model.__name__}: {e}", exc_info=True)
            await session.rollback()
            raise

    async def delete_many(
        self, 
        key: str, 
        value: Union[str, int, UUID]
    ) -> List[E]:
        try:
            async with self.__session_factory() as session:
                stmt = delete(self.__model).where(getattr(self.__model, key) == value).returning(self.__model)

                result = await session.execute(stmt)
                models = result.scalars().all()

                await session.commit()

                return [
                    self._to_entity(model) for model in models
                ]
        
        except Exception as e:
            logger.error(f"Error deleting {self.__model.__name__}: {e}", exc_info=True)
            await session.rollback()
            raise



    def _to_model(self, entity: E) -> M:
        raise NotImplementedError
    
    def _to_entity(self, model: M) -> E:
        raise NotImplementedError