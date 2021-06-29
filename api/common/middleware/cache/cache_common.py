# Time-to-live is measured in seconds

MAX_TTL_PERIOD = 3600


class CacheBlock():
    """A new block to be added to cache"""

    def __init__(
        self,
        ttl: int = 300,

    ):
        self._ttl = ttl
