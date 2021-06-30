

from typing import Any, Dict
from common.data.ext.mq_manager import MQManager
from gateway import ctx

retries = []


def retry(event, event_data):
    # TODO: implement retry system
    pass


async def sendNotice(target, info):
    print('sending notice to: ', target)


async def pushEvent(event: str, event_data: Dict[str, Any], producer=None, cache=None):
    if producer is None:
        producer = ctx.producer

    if cache is None:
        cache = ctx.user_cache

    try:
        transfer_data = event_data.get('transfer_data')
        target = transfer_data.get('target', dict()).get('uid')
        if target is None:
            return retry(event, event_data)
    except KeyError:
        return None

    info = await ctx.user_cache.con.get(target)
    if isinstance(info, bytes):
        info = info.decode('utf-8')

    if not info:
        return await sendNotice(target, info)

    return await producer.send(event, event_data)
