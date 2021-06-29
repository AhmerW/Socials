

from common.data.ext.mq_manager import MQManager
from gateway import ctx

retries = []


def _setRetry(*a, **kw):
    retries.append(
        (a, kw)
    )


async def _pushEvent(producer, *args, **kwargs) -> bool:
    if not isinstance(producer, MQManager):
        return False

    return await producer.send(*args, **kwargs)


async def pushEvent(retry=True, producer=None, *args, **kwargs):
    if producer is None:
        producer = ctx.producer
    s = pushEvent(producer, *args, **kwargs)
    if s is False and retry:
        _setRetry(*args, **kwargs)
    return s
