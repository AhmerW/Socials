

from typing import Any, Dict
from common.data.ext.app.status import Status
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
    status = await ctx.user_cache.con.exists(target)

    if not status:  # is offline
        return await sendNotice(target, status)

    return await producer.send(event, event_data)
