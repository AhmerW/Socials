import asyncio
import os
from asyncpg.connection import connect
import dotenv
import aioredis
from fastapi import FastAPI, WebSocket, status, WebSocketDisconnect
import aiohttp
import websockets

from common import utils
from common.data.ext.mq_manager import MQManager, MQManagerType, deserializer

from services.dispatch_service import ctx


MAX_WS_CON = 3


def decodeValue(value, default=None):
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    if not isinstance(value, str):
        return value

    if value.isdigit():
        try:
            value = int(value)
        except ValueError:
            value = default

    return value


class NotificationManager():

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
            value_deserializer=deserializer
        )
        await self.consumer.start()
        self.consumer.client.subscribe(pattern='^user.*')

        async for msg in self.consumer.client:
            transfer_data = msg.value.get('transfer_data')
            if transfer_data is None:
                continue
            data = self.clients.get(
                transfer_data.get(
                    'target',
                    dict()
                ).get('uid')
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
            if len(data) > MAX_WS_CON:
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

        # 1 : Status.ONLINE

        connections = await ctx.user_cache.hget(uid, 'connections')
        print(connections)
        connections = decodeValue(connections)
        print(connections)

        if not connections:
            # TODO: instead of default status 1, implement preffered status
            await ctx.user_cache.hmset_dict(uid, connections=1, status=1)
        else:
            if connections > MAX_WS_CON:

                return False
            await ctx.user_cache.hincrby(uid, 'connections', 1)

        return ws_info

    async def removeUser(self, uid, device) -> bool:
        data = self.clients.get(uid)
        if data:
            for i, con in enumerate(data):
                if con['id'] == device:
                    self.clients[uid].pop(i)
                    info = await ctx.user_cache.hgetall(uid)
                    info = decodeValue(info)

                    if not isinstance(info, dict):
                        print("not is dict?")
                        # already removed ??
                        return True
                    print('info')
                    connections = info.get('connections', 1)
                    if connections == 1:
                        await ctx.user_cache.delete(uid)
                    else:
                        await ctx.user_cache.hset(uid, 'connections', connections-1)
                    print("remvoed user.")
                    # send http call for sending notice
                    return True

        return False


HOST = utils.SERVICE_NC_IP
PORT = utils.SERVICE_NC_PORT
verification_session = None

app = FastAPI()


@ app.on_event('startup')
async def onStartup():
    dotenv.load_dotenv(os.path.join('services', 'dispatch_service', '.env'))
    auth = os.getenv('USER_CACHE_AUTH')

    if auth in (0, '0'):
        auth = None

    ctx.user_cache = await aioredis.create_redis_pool(
        (os.getenv('USER_CACHE_HOST'), os.getenv('USER_CACHE_PORT')),
        password=auth,
        db=int(os.getenv('USER_CACHE_DB'))
    )
    ctx.ncm = NotificationManager()
    asyncio.create_task(ctx.ncm.start())


@ app.on_event('shutdown')
async def onShutdown():
    await ctx.ncm.cosumer.stop()


@ app.websocket('/ws')
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
    try:
        uid = resp['data']['uid']
    except KeyError:
        return await websockets.close(code=status_)
    data = await ctx.ncm.addUser(
        uid,
        websocket,
        device
    )
    if not data:
        return await websocket.close(code=status_)
    try:
        while True:
            msg = await data['queue'].get()
           # print("delivering: ", msg)
            if msg.get('transfer_data') is not None:
                del msg['transfer_data']
            await websocket.send_json(msg)
    except (
            WebSocketDisconnect,
            ConnectionError,
            websockets.exceptions.WebSocketException
    ):
        print("removing ", await ctx.ncm.removeUser(uid, device))
    except Exception as e:
        print('another exception: ', e)

"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
