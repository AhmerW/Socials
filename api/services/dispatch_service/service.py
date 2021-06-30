import asyncio
from fastapi import FastAPI, WebSocket, status, WebSocketDisconnect
import aiohttp

from common import utils
from common.data.ext.mq_manager import MQManager, MQManagerType, deserializer

from services.dispatch_service.ctx import ServiceContext as ctx


class NotificationManager():
    MAX_WS_CON = 3

    def __init__(self):
        self.consumer = None
        self.running = False
        self.clients = {
            'uid': [  # List of Websocket connections [max: MAX_WS_CON]
                {
                    'id': 'device-id',
                    'ws': '{ws object}',
                    'queue': '{queue object}'
                }
            ]
        }

    async def sendNotice(self):
        pass

    async def start(self):
        self.consumer = MQManager(
            MQManagerType.Consumer,
            utils.SERVICE_NC_AK_BROKER,
            'user.message.new',
            'user.message.delete',
            value_deserializer=deserializer
        )
        await self.consumer.start()
        async for msg in self.consumer.client:
            transfer_data = msg.value.get('transfer_data')
            if transfer_data is None:
                continue
            data = self.clients.get(
                transfer_data.get('target')
            )
            del msg.value['transfer_data']
            if data:
                for con in data:
                    await con['queue'].put(msg.value)

            else:
                await self.sendNotice()

    async def addUser(self, uid, ws, device_id):
        """
        Adds user to the object
        Returns the data or false dependent on 
        if the operation was a success.
        """
        data = self.clients.get(uid)
        if data is not None:
            if len(data) > self.__class__.MAX_WS_CON:
                return False
            for i, obj in enumerate(data):
                if obj['id'] == device_id:
                    data.pop(i)

        ws_info = {
            'id': device_id,
            'ws': ws,
            'queue': asyncio.Queue()
        }
        if data is None:
            self.clients[uid] = [ws_info]
        else:
            self.clients[uid].append(ws_info)
        return ws_info

    async def removeUser(self, uid, device) -> bool:
        data = self.clients.get(uid)
        if data:
            for i, con in enumerate(data):
                if con['id'] == device:
                    self.clients[uid].pop(i)
                    return True

        return False


HOST = utils.SERVICE_NC_IP
PORT = utils.SERVICE_NC_PORT
verification_session = None

app = FastAPI()


@app.on_event('startup')
async def onStartup():
    ctx.ncm = NotificationManager()
    asyncio.create_task(ctx.ncm.start())


@app.on_event('shutdown')
async def onShutdown():
    await ctx.ncm.cosumer.stop()


@app.websocket('/ws')
async def connectWs(websocket: WebSocket, ott: str, device: str):
    global verification_session
    if verification_session is None:
        verification_session = aiohttp.ClientSession()
    status_ = status.WS_1008_POLICY_VIOLATION
    token = websocket.headers.get('Authorization')
    async with verification_session.get(
        f'{utils.SERVER_URL}/ott/verify?ott={ott}',
        headers={'Authorization': token}
    ) as response:
        resp = await response.json()
        if not resp.get('ok'):
            return await websocket.close(code=status_)

    await websocket.accept()
    data = await ctx.ncm.addUser(
        resp['data']['uid'],
        websocket,
        device
    )
    if not data:
        return await websocket.close(code=status_)
    try:
        while True:
            msg = await data['queue'].get()
            if msg.get('transfer_data') is not None:
                del msg['transfer_data']
            await websocket.send_json(msg)
    except WebSocketDisconnect:
        print("removing ", await ctx.ncm.removeUser(device))

"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
