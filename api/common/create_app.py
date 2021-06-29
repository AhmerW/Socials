import os
import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


async def createPool(args, **kwargs):
    return await asyncpg.create_pool(
        **{
            k: os.getenv(v)
            for k, v in
            kwargs.items()
        }
    )
