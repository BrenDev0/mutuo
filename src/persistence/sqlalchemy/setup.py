import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

_async_engine = None
_async_session_factory = None

class SqlAlchemyBase(DeclarativeBase):
    pass


def get_async_engine():
    global _async_engine

    if _async_engine is None:
        db_url = os.getenv("DATABASE_URL")

        if not db_url:
            raise ValueError("DB variables not set")
        
        _async_engine = create_async_engine(
            url=db_url,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True 
        )

    return _async_engine

def get_async_session_factory():
    global _async_session_factory

    if _async_session_factory is None:
        async_engine = get_async_engine()
        _async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
    
    return _async_session_factory