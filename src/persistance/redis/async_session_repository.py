from redis import asyncio as aioredis
import json
from typing import Optional, Dict, Any
import os
from ..repositories import AsyncSessionRepository


class AsyncRedisSessionRepository(AsyncSessionRepository):
    def __init__(self):
        self.__connection_url = os.getenv("REDIS_URL")

        if not self.__connection_url:
            raise ValueError("Redis variable not configured")
        
        self.redis = aioredis.from_url(url=self.__connection_url)

    async def set_session(self, key: str, value: str, expire_seconds: Optional[int] = 3600) -> None:       
        await self.redis.set(key, value, ex=expire_seconds)

    async def get_session(self, key: str) -> Dict[str, Any] | None:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def delete_session(self, key: str) -> bool:
        return await self.redis.delete(key) > 0