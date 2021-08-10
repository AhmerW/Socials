import asyncpg

from passlib.context import CryptContext
from fastapi.applications import FastAPI
from starlette.middleware.cors import CORSMiddleware


from gateway.data.clients.cache_client import CacheClient

from gateway.data.clients.mq.mq_client import MQManager
from common.response import SuccessResponse
from common.settings.settings import DEV_SETTINGS


PROJECT_NAME = "Socials"


# must be created in an async function
producer: MQManager = None
pool: asyncpg.pool.Pool = None
chat_pool: asyncpg.pool.Pool = None

cache_client: CacheClient = None
user_cache: CacheClient = None

otts = {}

pwd_ctx = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


_defaults = dict(openapi_url=None, redoc_url=None, docs_url=None)

if DEV_SETTINGS.IS_DEV:
    _defaults = dict(
        docs_url="/documentation",
        openapi_url="/openapi.json",
    )

app = FastAPI(
    title=PROJECT_NAME,
    default_response_class=SuccessResponse,
    **_defaults,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
