import logging

from common.settings.settings import (
    DEV_SETTINGS,
    LOGGER_SETTINGS,
)


def getLogger() -> logging.Logger:
    return logging.Logger(
        LOGGER_SETTINGS.DEV_LOGGER_NAME
        if DEV_SETTINGS.IS_DEV
        else LOGGER_SETTINGS.LOGGER_NAME,
    )
