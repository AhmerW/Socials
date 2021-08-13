from typing import Final
from common.settings.settings import SVC_DISPATCH_SETTINGS
from common.settings.utils import constructUrl
from gateway.data.clients.mq.mq_client import MQManager, MQManagerType, serializer

from gateway.ctx import app


AK_BROKER_URL = constructUrl(
    SVC_DISPATCH_SETTINGS.AK_BROKER_IP,
    SVC_DISPATCH_SETTINGS.AK_BROKER_PORT,
    "",
)


class Producers:
    PRODUCER: MQManager = None


@app.on_event("startup")
async def setProducer():
    Producers.PRODUCER = MQManager(
        MQManagerType.Producer,
        broker=AK_BROKER_URL,
        value_serializer=serializer,
    )
