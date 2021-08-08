import logging

from common.data.ext.mq_manager import MQManager, MQManagerType, serializer
from common.data.ext.cache_client import CacheClient
from common.create_app import createPool
from common.settings.settings import (
    CACHE_SERVER_SETTINGS,
    DEV_SETTINGS,
    LOGGER_SETTINGS,
    SVC_DISPATCH_SETTINGS,
    ServiceDispatchSettings,
    USER_CACHE_SETTINGS,
)
from common.settings.utils import constructUrl
from gateway import ctx


def loggerInit(logger: logging.Logger) -> logging.Logger:
    """Init logger, global settings, independent on DEV_SETTINGS.IS_DEV"""

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
    )
    logger.addHandler(handler)

    return logger


def configureLogging() -> logging.Logger:
    def _loggingForDev(logger: logging.Logger) -> logging.Logger:
        logger.setLevel(level=logging.DEBUG)
        return logger

    if DEV_SETTINGS.IS_DEV:

        return loggerInit(
            _loggingForDev(
                logging.Logger(LOGGER_SETTINGS.DEV_LOGGER_NAME),
            )
        )

    logger = logging.getLogger(LOGGER_SETTINGS.LOGGER_NAME)

    logger.setLevel(level=logging.WARNING)

    return loggerInit(logger)


async def initializeConnections():
    """
    Decleration of global immutable instances and connection (pools).
    Stored in the global context (ctx) module.
    """

    async def _create_pool(schema: str):
        return await createPool(
            {"server_settings": {"search_path": schema}},
            # (Environment variables)
            host="SERVER_DB_HOST",
            port="SERVER_DB_PORT",
            user="SERVER_DB_USER",
            password="SERVER_DB_PASSWD",
            database="SERVER_DB_DB",
        )

    AK_BROKER_URL = constructUrl(
        SVC_DISPATCH_SETTINGS.AK_BROKER_IP,
        SVC_DISPATCH_SETTINGS.AK_BROKER_PORT,
        "",
    )

    ctx.pool = await _create_pool("public")
    ctx.chat_pool = await _create_pool("chat")

    ctx.producer = MQManager(
        MQManagerType.Producer,
        broker=AK_BROKER_URL,
        value_serializer=serializer,
    )
    ctx.cache_client = await CacheClient.create(
        (str(CACHE_SERVER_SETTINGS.IP), CACHE_SERVER_SETTINGS.PORT),
        password=CACHE_SERVER_SETTINGS.AUTH,
        db=CACHE_SERVER_SETTINGS.DB,
    )

    ctx.user_cache = await CacheClient.create(
        (str(USER_CACHE_SETTINGS.IP), USER_CACHE_SETTINGS.PORT),
        password=USER_CACHE_SETTINGS.AUTH,
        db=USER_CACHE_SETTINGS.DB,
    )

    assert not any(
        [x is None for x in (ctx.pool, ctx.chat_pool, ctx.producer, ctx.user_cache)]
    )

    try:
        await ctx.producer.start()

    except Exception as e:
        raise e("Make sure the apache kafka broker is active!")


async def closeConnections():
    if isinstance(ctx.producer, MQManager):
        await ctx.producer.stop()
