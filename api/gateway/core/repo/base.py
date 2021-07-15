from abc import ABC, abstractmethod


from asyncpg import Connection, pool
import asyncpg
from fastapi.param_functions import Query
from common.data.ext.config import DEFAULT_CONF

from gateway import ctx
from common.data.local import db


class BaseInterface(ABC):

    @abstractmethod
    async def delete(self):
        pass


class BaseRepo():
    def __init__(
        self,
        # Whether or not we should acquire a database connection
        acquire: bool = True,
        # Defaults to the 'public' schema
        pool: pool.Pool = ctx.pool,
        # Existing connection object
        con: Connection = None,
        auto_close_con: bool = True
    ):
        self._acquire = acquire
        self._pool = pool
        self.con: Connection = con
        self._close_con = auto_close_con

    async def __aenter__(self):
        if not hasattr(self, 'con'):
            raise RuntimeError(
                'super().__init__() not called for parent-class.')
        if self.con is None and self._acquire:
            if self._pool is None:
                self._pool = ctx.pool
            self.con = await self._pool.acquire()

        return self

    async def __aexit__(self, *_, **__):
        await self.close()

    async def close(self):
        if self._close_con and isinstance(self.con, Connection):
            try:
                if not self.con.is_closed():
                    await self.con.close()
            except asyncpg.exceptions.InterfaceError:
                """Assuming connection already released back to the pool"""

    async def run(
        self,
        query: Query = None,
        pool: pool.Pool = None,
        con: Connection = None,
        op: db.DBOP = db.DBOP.Fetch,
    ):
        if not self._acquire:
            return None
        if con is None:
            con = self.con
        return await db.runQuery(
            query=query,
            pool=pool,
            con=con,
            op=op
        )


def constructOrExec(query: Query):
    pass
