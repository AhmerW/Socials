import os
import aiohttp
import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def createApp(*args, **kwargs):
    app = FastAPI(*args, **kwargs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

async def createPool(args, **kwargs):
    return await asyncpg.create_pool(**{k: os.getenv(v) for k, v in kwargs.items()})