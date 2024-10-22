import os
import asyncpg


async def createPool(*_, **kwargs):
    return await asyncpg.create_pool(**{k: os.getenv(v) for k, v in kwargs.items()})
