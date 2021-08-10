import aioredis
from common.middleware.cache.cache_backend import RedisCachingBackend


class CacheClient:
    def __init__(self, con: aioredis.ConnectionsPool) -> None:
        self._con: aioredis.Redis = con

    @property
    def con(self) -> aioredis.Redis:
        return self._con

    @classmethod
    async def create(cls, *args, **kwargs) -> "CacheClient":
        return CacheClient(
            await aioredis.create_redis_pool(*args, **kwargs),
        )
