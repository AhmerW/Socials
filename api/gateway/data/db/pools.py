import asyncio
from asyncio.queues import Queue
from sys import exc_info
from typing import List

from common.settings.settings import PG_SETTINGS
from gateway.ctx import app

from gateway.data.db.db_connection import PGPool
from gateway.data.events.events import SystemEvent
from gateway.data.log import getLogger

from gateway.data.events.bus import eventBus

loop = asyncio.get_event_loop()
logger = getLogger()


class Pools:
    DB_POOL: PGPool = None
    CHAT_POOL: PGPool = None


@app.on_event("startup")
async def setPools() -> None:
    try:
        eventBus.emit(SystemEvent("db.init.start"))
        Pools.DB_POOL = await PGPool.fromDsn(
            PG_SETTINGS.DSN,
            PG_SETTINGS.DSN_SCHEMA,
        )

        Pools.CHAT_POOL = await PGPool.fromDsn(
            PG_SETTINGS.CHAT_DSN,
            PG_SETTINGS.CHAT_DSN_SCHEMA,
        )

        eventBus.emit(SystemEvent("db.init.done"))

    except Exception as e:
        _, exc_value, __ = exc_info()

        if not hasattr(exc_value, "message"):
            raise e

        logger.error(
            "Database connection failed with error:  '%s'" % exc_value.message,
        )
