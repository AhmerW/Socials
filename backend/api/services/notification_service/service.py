from fastapi import FastAPI, WebSocket, status
import aiohttp

from common.mq_manager import MQManager
from common import utils

from services.notification_service.ctx import ServiceContext as ctx

class NotificationManager():
    def __init__(self):
        self.manager = MQManager()
        self.clients = {
            'uid': [..., ...] # ws connections
        }
        
    async def addUser(self, uid, ws):
        self.clients[uid] = []
        
HOST = utils.SERVICE_NC_IP
PORT = utils.SERVICE_NC_PORT
verification_session = aiohttp.ClientSession()
      
app = FastAPI()  

@app.on_event('startup')
async def onStartup():
    ctx.ncm = NotificationManager()



@app.websocket('/ws')
async def connectWs(websocket : WebSocket, code: str):
    status_ = status.WS_1008_POLICY_VIOLATION
    async with verification_session.get(f'{utils.SERVER_URL}/verify?code={code}') as response:
        resp = await response.json()
        if not resp['ok']:
            return await websocket.close(code=status_)
    await websocket.accept()
    await ctx.ncm.addUser(resp['uid'])
    while True:
        pass
    
"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
