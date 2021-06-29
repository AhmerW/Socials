

import aioredis
from common.middleware.cache.cache_backend import RedisCachingBackend


class CacheClient():
    def __init__(self, con: aioredis.ConnectionsPool) -> None:
        self._con = con

    @property
    def con(self):
        return self._con

    @classmethod
    async def create(cls, *args, **kwargs) -> type:
        return CacheClient(
            await aioredis.create_redis_pool(
                *args,
                **kwargs
            )
        )
