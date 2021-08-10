from collections.abc import Iterable

import asyncpg
from enum import Enum

from gateway.data.db.queries import Query


class DBOP(Enum):
    Fetch = 0
    FetchFirst = 1
    Execute = 2


async def _processQuery(
    con: asyncpg.Connection, operation: DBOP, query: Query, serialize: bool = True
):

    result = list()
    if operation == DBOP.Fetch:
        result = list(await con.fetch(*query))

    elif operation == DBOP.FetchFirst:
        result = await con.fetchrow(*query)
        if result is not None:
            return dict(result)

    elif operation == DBOP.Execute:
        return await con.execute(*query)

    # make result serailizable
    # cast from iterable<asyncpg.Record> to list<dict>
    if serialize and isinstance(result, Iterable):
        return [dict(row) for row in result]

    return result


async def runQuery(
    query: Query = None,
    pool: asyncpg.pool.Pool = None,
    con: asyncpg.Connection = None,
    op: DBOP = DBOP.Fetch,
    serialize: bool = True,
):
    if any(x is None for x in (op, query)) or (pool is None and con is None):
        return None

    if con is not None:
        return await _processQuery(con, op, query)

    async with pool.acquire() as con:
        async with con.transaction():
            return await _processQuery(con, op, query, serialize=serialize)
