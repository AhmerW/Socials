import json

from enum import Enum
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

AK_BROKER = 'localhost:9092'



def deserializer(serialized):
    return json.loads(serialized)

class MQClient():
    def __init__(self, broker = AK_BROKER, *args, **kwargs):
        self.client = AIOKafkaConsumer(
            bootstrap_servers = broker,
            value_deserializer = deserializer,
            *args,
            **kwargs
        )
        
    async def start(self):
        await self.client.start()
        
    async def stop(self):
        await self.client.stop()

        
    def receive(self):
        return self.client