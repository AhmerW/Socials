import json

from enum import Enum
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from common.utils import SVC_DISPATCH_AK_BROKER


class MQManagerType(Enum):
    Producer = 0,
    Consumer = 1


def deserializer(serialized):
    return json.loads(serialized)


def serializer(value):
    return json.dumps(value).encode()


class MQManager():
    def __init__(self, mq_type: MQManagerType, broker=SVC_DISPATCH_AK_BROKER, *args, **kwargs):
        self.type_ = mq_type
        if self.type_ == MQManagerType.Producer:
            self.client = AIOKafkaProducer(
                bootstrap_servers=broker,
                *args,
                **kwargs
            )
        else:
            self.client = AIOKafkaConsumer(
                bootstrap_servers=broker,
                *args,
                **kwargs
            )

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()

    async def send(self, *args, **kwargs):
        assert self.type_ == MQManagerType.Producer
        return await self.client.send_and_wait(*args, **kwargs)

    def receive(self):
        assert self.type_ == MQManagerType.Consumer
        return self.client
