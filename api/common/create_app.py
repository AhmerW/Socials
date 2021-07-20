import os
import asyncpg


async def createPool(*args, **kwargs):
    return await asyncpg.create_pool(
        **{
            k: os.getenv(v)
            for k, v in
            kwargs.items()
        }
    )
