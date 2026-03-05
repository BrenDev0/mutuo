from src.di.injector import Injector
from .repositories import AsyncSessionRepository
from .redis.async_session_repository import AsyncRedisSessionRepository

def register_dependencies(injector: Injector):
    injector.register(AsyncSessionRepository, AsyncRedisSessionRepository)
    
    