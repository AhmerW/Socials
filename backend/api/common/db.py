import asyncpg
from enum import Enum

class DBOP(Enum):
    Fetch = 0
    FetchFirst = 1
    Execute = 2


async def _processQuery(con, operation, query, *args):
    if operation == DBOP.Fetch:
        return await con.fetch(query, *args)
    elif operation == DBOP.FetchFirst:
        _res = await con.fetch(query, *args)
        if len(_res) >= 1:
            return _res[0]
        return _res
    elif operation == DBOP.Execute:
        return await con.execute(query, *args)

    return None


async def runQuery(
    *args, 
    query : str = None, 
    pool : asyncpg.pool = None, 
    con : asyncpg.Connection = None,
    op : DBOP = DBOP.Fetch, 
    ):
    if any(x is None for x in (op, query)) or (pool is None and con is None):
        return None
    
    if con is not None:
        return await _processQuery(con, op, query, *args)
    
    async with pool.acquire() as con:
        async with con.transaction():
            return await _processQuery(con, op, query, *args)
             
    return None