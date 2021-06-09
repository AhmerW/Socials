import logging
import asyncio
import os
from yaml import load
from hbmqtt.broker import Broker



@asyncio.coroutine
def broker_coro(config):
    broker = Broker(config)
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    
    with open('config.yaml', 'r') as f:
        
        asyncio.get_event_loop().run_until_complete(broker_coro(load(f)))
        asyncio.get_event_loop().run_forever()