from abc import ABC, abstractmethod

import aioredis

from common.middleware.cache.cache_common import CacheBlock


class CachingBackend(ABC):

    @abstractmethod
    async def add(self, block: CacheBlock) -> None:
        """Adds a new block to cache"""
        pass

    @abstractmethod
    async def check(self) -> bool:
        pass


class RedisCachingBackend(CachingBackend):
    """aioredis implementation"""

    def __init__(self, redis: aioredis.Redis):
        self._redis = redis

    def add(self):
        pass


DefaultCacheBackend = RedisCachingBackend
