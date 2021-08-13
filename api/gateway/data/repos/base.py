from typing import Any, Optional
from abc import ABC, abstractmethod


import asyncpg
from asyncpg import Connection, pool
from email_validator import EmailNotValidError, validate_email as _validateEmail


from gateway import ctx
from gateway.data.db import db
from gateway.data.db.db_connection import PGConnection, PGPool
from gateway.data.db.pools import Pools


class Base(ABC):
    __slots__ = "pool", "_con"

    def __init__(
        self,
        con: PGConnection = None,
        pool: PGPool = None,
    ) -> None:
        self._con = con
        self.pool = pool or Pools.DB_POOL

    @classmethod
    async def new(
        cls,
        pool=None,
    ) -> "Base":
        pool = pool or Pools.DB_POOL
        con = await pool.get()
        return cls(
            con,
            pool,
        )

    async def __aenter__(self):
        if self._con is None:
            self._con = await self.pool.get()

        return self

    async def __aexit__(self, *_, **__) -> None:
        await self.close()

    async def close(self) -> None:
        if self._con is not None:
            await self.pool.release_connection(self._con)
        # if not self._con.closed():
        # await self._con.close()

    @abstractmethod
    async def create(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> Any:
        raise NotImplementedError


class BaseService(ABC):
    __slots__ = ("_repo",)

    async def __aenter__(
        self,
        repo: Base,
        pool=None,
    ) -> "BaseService":
        self._repo = await repo.new(
            pool=pool,
        )
        return self

    async def __aexit__(self, *_, **__) -> None:
        await self._repo.close()


class BaseValidator:
    def validEmail(email) -> Optional[str]:
        try:
            _validateEmail(
                email,
                check_deliverability=False,
            )
        except EmailNotValidError as msg:
            return str(msg)


class BaseRepo:
    def __init__(
        self,
        # Whether or not we should acquire a database connection
        acquire: bool = True,
        # Defaults to the 'public' schema
        pool: pool.Pool = ctx.pool,
        # Existing connection object
        con: Connection = None,
        auto_close_con: bool = True,
    ):
        self._acquire = acquire
        self._pool = pool
        self.con: Connection = con
        self._close_con = auto_close_con

    async def __aenter__(self):
        if not hasattr(self, "con"):
            raise RuntimeError("super().__init__() not called for parent-class.")
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
        query: str = None,
        pool: pool.Pool = None,
        con: Connection = None,
        op: db.DBOP = db.DBOP.Fetch,
    ):
        if not self._acquire:
            return None
        if con is None:
            con = self.con
        return await db.runQuery(query=query, pool=pool, con=con, op=op)
