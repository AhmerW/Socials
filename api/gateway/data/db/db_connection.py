from typing import Iterable, List, Optional, AsyncIterator, Union
from contextlib import asynccontextmanager

from more_itertools import first
import asyncpg


from gateway.data.log import getLogger


from gateway.data.db.queries.query import Query
from gateway.data.db.base_connection import BasePool, BaseConnection

logger = getLogger()


class PGConnection(BaseConnection):
    """
    Represents a connection to Postgres, using asyncpg
    """

    def __init__(
        self,
        con: Optional[asyncpg.Connection] = None,
    ) -> None:
        self._con = con

    @property
    def connection(self) -> asyncpg.Connection:
        return self._con

    def _serialize(self, records: Iterable) -> List[dict]:
        return [dict(record) for record in records]

    def _getQuery(self, query: Union[Query, str]) -> Query:
        if isinstance(query, str):
            return Query(query)
        return query

    def closed(self) -> bool:
        return self._con.is_closed()

    async def close(self) -> None:
        await self._con.close()

    async def execute(self, query: Union[Query, str], **values) -> str:
        query = self._getQuery(query)
        return await self._con.execute(
            *query.format(**values),
        )

    async def fetch(self, query: Union[Query, str], **values) -> List[dict]:
        query = self._getQuery(query)
        res: List[asyncpg.Record] = await self._con.fetch(
            *query.format(**values),
        )

        return self._serialize(
            res,
        )

    async def fetchFirst(self, query: Query, **values) -> dict:
        records = await self.fetch(query, **values)

        return first(
            records,
            list(),
        )


class PGPool(BasePool):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self._pool = pool

    @classmethod
    async def fromDsn(
        self,
        dsn: str,
        schema: str = "schema",
    ) -> "PGPool":
        pool = await asyncpg.create_pool(
            dsn,
            server_settings={
                "search_path": schema,
            },
        )
        cls = PGPool(
            pool=pool,
        )

        await cls._test()
        return cls

    async def _test(self) -> None:
        async with self.acquire() as con:
            await con.execute("SELECT 1")

    async def release_connection(self, con: PGConnection) -> None:
        await self._pool.release(con.connection)

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[PGConnection]:
        async with self._pool.acquire() as con:
            pgc = PGConnection(con)
            yield pgc

            await self.release_connection(pgc)

    async def get(self):
        return PGConnection(await self._pool.acquire())
