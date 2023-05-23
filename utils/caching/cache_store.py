from typing import Any, List
from redis import asyncio as aioredis

from utils.caching.cache_store_config import CacheStoreConfig


# See https://aioredis.readthedocs.io/en/latest/examples/#recipes
class CacheStore():
    def __init__(self, config: CacheStoreConfig) -> None:
        # Clients and connections have implemented __del__, so will attempt to automatically clean up any open connections when garbage-collected
        redis = aioredis.from_url(config.url, encoding=config.encoding)
        self._instance = redis

    async def get(self, key: str) -> Any | None:
        value = await self._instance.get(key)
        return value

    async def set(self, key: str, value: str, ttl: int = None, get: bool = True) -> Any | None:
        prevValue = await self._instance.set(key, value, ex=ttl, get=get)
        return prevValue

    async def mset(self, data: List[List]):
        async with self._instance.pipeline(transaction=True) as pipe:
            for key, val in data:
                pipe.set(key, val)
            results = await pipe.execute()
        for res in results:
            assert res

    async def delete(self, *key: str):
        await self._instance.delete(*key)
