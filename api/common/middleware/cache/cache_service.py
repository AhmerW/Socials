from functools import wraps

from common.middleware.cache.cache_backend import (
    CachingBackend,
    DefaultCacheBackend
)


class CacheSettings:
    def __init__(
        self,
        backend: CachingBackend = DefaultCacheBackend
    ):

        self.backend = backend


class Cache(object):
    def __init__(self, cache_settings=CacheSettings):
        self._settings = cache_settings

    def cache(
        ttl: int = 360
    ):
        """Cache using the default settings"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = kwargs.get('request')
                if request is not None:
                    pass

            return wrapper

        return decorator

    def __call__(self):
        pass
