from enum import Enum
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

class MQManagerType(Enum):
    Producer = 0,
    Consumer = 1

class MQManager():
    def __init__(self, mq_type : MQManagerType):
        self.type_ = mq_type