

from typing import Any, Dict

from common.data.ext.app.status import Status
from common.data.ext.cache_client import CacheClient
from common.data.ext.event import Event, Notice
from common.data.ext.mq_manager import MQManager
from common.utils import SYSTEM_UID
from gateway import ctx
from gateway.core.models import NoticeInsert
from gateway.core.repo.repos import NoticeRepo

retries = []


def retry(event: Event):
    # TODO: implement retry system
    print("[ERROR] retrying... ", event.event())


async def sendNotice(notice: Notice):
    print('sending notice to: ', notice.target)


async def pushEvent(
        event: Event,
        producer: MQManager = None,
        cache: CacheClient = None) -> None:

    if event.target == SYSTEM_UID:
        return

    if producer is None:
        producer = ctx.producer

    if cache is None:
        cache = ctx.user_cache

    status = await cache.con.exists(event.target)
    if not status:  # is offline
        if not event.hasNotice():
            # Events which require user interaction to proceed, or which has a target
            # will include a Notice. This is not the case for events which will later
            # be fetched upon client login. One example with this are: chat messages.
            return

        notice = event.getNotice()
        if notice.save and notice.author != notice.target:
            async with NoticeRepo() as repo:
                try:
                    await repo.insertNotice(notice)
                except Exception as e:
                    raise e

        return await sendNotice(notice)

    await producer.send('ws.event.new', event.getData())
