import asyncpg

from passlib.context import CryptContext
from fastapi.applications import FastAPI
from starlette.middleware.cors import CORSMiddleware


from common.data.ext.cache_client import CacheClient
from common.data.ext.config import DEFAULT_CONF
from common.data.ext.email_service import EmailService
from common.data.ext.mq_manager import MQManager
from common.response import SuccessResponse
from common.settings.settings import DEV_SETTINGS


PROJECT_NAME = "Socials"

HOST = "localhost"
PORT = 8000
PROTOCOL = "http"
URL = f"{PROTOCOL}://{HOST}:{PORT}"
ACCOUNT_VERIFY_URL = f"{URL}/account/verify"


# must be created in an async function
producer: MQManager = None
pool: asyncpg.pool.Pool = None
chat_pool: asyncpg.pool.Pool = None

cache_client: CacheClient = None
user_cache: CacheClient = None

otts = {}

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# default email service for account notifications
# verifications, security updates, etc...

email_service = EmailService(DEFAULT_CONF, incl_name="Socials")

_defaults = dict(openapi_url=None, redoc_url=None, docs_url=None)

if DEV_SETTINGS.IS_DEV:
    _defaults = dict(docs_url="/documentation", openapi_url="/openapi.json")

app = FastAPI(title=PROJECT_NAME, default_response_class=SuccessResponse, **_defaults)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL, f"{PROTOCOL}://{HOST}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
