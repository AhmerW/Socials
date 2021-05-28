import asyncpg
from enum import Enum

class DBOP(Enum):
    Fetch = 0
    FetchFirst = 1
    Execute = 2



async def runQuery(pool, operation, query, *args):
    if pool is None:
        return None
    async with pool.acquire() as con:
        async with con.transaction():
            try:
                if operation == DBOP.Fetch:
                    return await con.fetch(query, *args)
                elif operation == DBOP.FetchFirst:
                    _res = await con.fetch(query, *args)
                    if len(_res) >= 1:
                        return _res[0]
                    return _res
                elif operation == DBOP.Execute:
                    return await con.execute(query, *args)
            except Exception as e:
                raise e
             
    return None