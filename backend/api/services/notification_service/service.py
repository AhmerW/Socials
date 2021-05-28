import asyncio
from aiokafka import AIOKafkaConsumer

from fastapi import FastAPI, WebSocket, status, BackgroundTasks
import aiohttp

from common import utils

from services.notification_service.ctx import ServiceContext as ctx



class NotificationManager():
    MAX_WS_CON = 3
    def __init__(self):

        self.running = False
        self.clients = {
            'uid': [ # List of Websocket connections [max: MAX_WS_CON]
                {
                    'id': 'device-id',
                    'ws': '{ws object}',
                    'queue': '{queue object}'
                }
            ] 
        }

    async def start(self):
        consumer = AIOKafkaConsumer(
            'events',
            bootstrap_servers='localhost:9092')
        # Get cluster layout and join group `my-group`
        print("listening for consumer events")
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                    msg.key, msg.value, msg.timestamp)
        finally:
            # Will leave consumer group; perform autocommit if enabled.
            await consumer.stop()
                
 
        
    async def addUser(self, uid, ws, device_id) -> bool:
        """
        Adds user to the object
        Returns the data or false dependent on 
        if the operation was a success.
        """
        data = self.clients.get(uid)
        if data is not None:
            if len(data) > self.__class__.MAX_WS_CON:
                return False
            for obj in data:
                if obj['id'] == device_id:
                    return False
        data = {
            'id': device_id,
            'ws': ws,
            'queue': asyncio.Queue()
        }
        self.clients[uid] = data
        return data
        
        
HOST = utils.SERVICE_NC_IP
PORT = utils.SERVICE_NC_PORT
verification_session = aiohttp.ClientSession()
      
app = FastAPI()  

@app.on_event('startup')
async def onStartup():
    ctx.ncm = NotificationManager()
    print("starting consumer") 
    asyncio.create_task(ctx.ncm.start())
    print("consumer running")




@app.websocket('/ws')
async def connectWs(websocket : WebSocket, code: str):
    status_ = status.WS_1008_POLICY_VIOLATION
    token = websocket.headers.get('Authorization')
    code = websocket.headers.get('Authorization-Code')
    async with verification_session.get(
            f'{utils.SERVER_URL}/verify?code={code}',
            headers={'Authorization': f'bearer {token}'}
        ) as response:
        resp = await response.json()
        if not resp['ok']:
            return await websocket.close(code=status_)
    
    await websocket.accept()
    data = await ctx.ncm.addUser(resp['uid'])
    if not data:
        return await websocket.close(code=status_)
    
    while True:
        msg = await data['queue'].get()
        print(msg)
    
"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
