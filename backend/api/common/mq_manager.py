import asyncio
from typing import Dict, List
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

"""

    0 when we prefer that the message will not arrive at all rather than arrive twice
    1 when we want the message to arrive at least once but don't care if it arrives twice (or more)
    2 when we want the message to arrive exactly once. A higher QOS value means a slower transfer

"""

class MQManager(MQTTClient):
    def __init__(self):
        # topic : clients
        # self.clients : Dict[str, ...] = {}
        pass
    
    async def mqPublish(self, topic, msg):
        await asyncio.gather(
            self.publish()
        )
        
    async def mqSubscribe(self, topic, qos = QOS_1):
        await self.subscribe([
            (topic, qos)
        ])
    
    async def mqStart(self):
        await self.connect('localhost:1883')
        
    async def mqClose(self):
        await self.disconnect()