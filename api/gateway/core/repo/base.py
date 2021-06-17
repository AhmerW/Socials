from abc import ABC, abstractmethod
from asyncpg import Connection
import asyncpg
from fastapi.param_functions import Query

from gateway.ctx import ServerContext as ctx
from common.data.local import db


class BaseInterface(ABC):

    @abstractmethod
    async def delete(self):
        pass


class BaseRepo():
    def __init__(self):
        self.con: Connection = None

    def __setattr__(self, name, value):
        if name == 'con' and value is not None:
            if not isinstance(value, Connection):
                raise RuntimeError(
                    'Connection of type <{0}> not permitted.'.format(Connection))

        return super.__setattr__(self, name, value)

    async def __aenter__(self):
        if self.con is None:
            self.con = await ctx.pool.acquire()
        return self

    async def __aexit__(self, *a, **kw):
        await self.close()

    async def close(self):
        if isinstance(self.con, Connection):
            await self.con.close()

    async def run(
        self,
        query: Query = None,
        pool: asyncpg.pool = None,
        con: asyncpg.Connection = None,
        op: db.DBOP = db.DBOP.Fetch,
    ):
        if con is None:
            con = self.con
        return await db.runQuery(
            query=query,
            pool=pool,
            con=con,
            op=op
        )
