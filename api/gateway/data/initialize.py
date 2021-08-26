import logging

from gateway.data.clients.mq.mq_client import MQManager, MQManagerType, serializer
from gateway.data.clients.cache_client import CacheClient
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





async def closeConnections():
    if isinstance(ctx.producer, MQManager):
        await ctx.producer.stop()
