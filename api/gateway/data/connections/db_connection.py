import sys
from typing import Any, Final, Optional
from contextlib import asynccontextmanager

import asyncpg


from ctx import app
from common.data.log import getLogger


from common.data.local.queries.query import Query
from common.settings import SERVER_SETTINGS
from data.connections.base_connection import BasePool, BaseConnection

logger = getLogger()


class PGConnection(BaseConnection):
    """
    Represents a connection to Postgres, using asyncpg
    """

    def __init__(self, con: Optional[asyncpg.Connection] = None) -> None:
        self._con = con

    @property
    def connection(self) -> asyncpg.Connection:
        return self._con

    async def execute(self, query: Query, **values) -> None:
        return await self._con.execute(
            query.format(**values),
        )

    async def fetch(self, query: Query, **values) -> Any:
        return await self._con.fetch(
            query.format(**values),
        )


class PGPool(BasePool):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self._pool = pool

    @classmethod
    async def from_dsn(self, dsn: str) -> "PGPool":
        pool = await asyncpg.create_pool(dsn)
        cls = PGPool(
            pool=pool,
        )

        await cls._pre_init()
        return cls

    async def _pre_init(self) -> None:
        async with self.connection() as con:
            await con.execute("SELECT 1")

    async def release_connection(self, con: PGConnection) -> None:
        return await con.connection.close()

    @asynccontextmanager
    async def connection(self) -> PGConnection:
        async with self._pool.acquire() as con:
            pgc = PGConnection(con)
            yield pgc

            await self.release_connection(pgc)


CONNECTION_POOL: BasePool = ...


@app.on_event("startup")
async def setCp() -> None:
    global CONNECTION_POOL

    try:
        CONNECTION_POOL = await PGPool.from_dsn(
            "APP_SETTINGS.PG_DSN",
        )
    except Exception as e:
        _, exc_value, __ = sys.exc_info()

        logger.error("Database connection failed with error:  '%s'" % exc_value.message)
