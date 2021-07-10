import asyncio
import dotenv
import os

from fastapi import FastAPI, WebSocket, status, WebSocketDisconnect
from websockets.exceptions import WebSocketException
import aioredis


from common import utils
from common.data.ext.mq_manager import MQManager, MQManagerType, deserializer

from services.dispatch_service import ctx
from services.dispatch_service.const import MAX_WS_CON, TD_KEY, WS_DISCONNECT_CHECK
from services.dispatch_service.validate import decodeValue, validateConnection

HOST = utils.SVC_DISPATCH_IP
PORT = utils.SVC_DISPATCH_PORT


app = FastAPI()


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
            utils.SVC_DISPATCH_AK_BROKER,
            value_deserializer=deserializer
        )
        await self.consumer.start()
        self.consumer.client.subscribe(pattern='^user.*')

        async for msg in self.consumer.client:
            transfer_data = msg.value.get(TD_KEY)
            if transfer_data is None:
                continue
            data = self.clients.get(
                transfer_data.get(
                    'target',
                    dict()
                ).get('uid')
            )
            del msg.value[TD_KEY]
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

        connections = await ctx.user_cache.con.hget(uid, 'connections')
        connections = decodeValue(connections)

        if not connections:
            # TODO: instead of default status 1, implement preffered status
            await ctx.user_cache.con.hmset_dict(uid, connections=1, status=1)
        else:
            if connections > MAX_WS_CON:

                return False
            await ctx.user_cache.con.hincrby(uid, 'connections', 1)

        return ws_info

    async def removeUser(self, uid, device) -> bool:
        data = self.clients.get(uid)
        if data:
            for i, con in enumerate(data):
                if con['id'] == device:
                    self.clients[uid].pop(i)
                    info = await ctx.user_cache.con.hgetall(uid)
                    info = decodeValue(info)

                    if not isinstance(info, dict):
                        print("not is dict?")
                        # already removed ??
                        return True

                    connections = info.get('connections', 1)
                    if connections == 1:
                        await ctx.user_cache.con.delete(uid)
                    else:
                        await ctx.user_cache.con.hset(uid, 'connections', connections-1)
                    print("User has disconnected.")
                    # send http call for sending notice
                    return True

        return False


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
    status_ = status.WS_1008_POLICY_VIOLATION
    response = await validateConnection(websocket, ott)

    if not response:
        return await websocket.close(code=status_)

    try:
        uid = response['data']['uid']
        if not isinstance(uid, int):
            raise ValueError()

    except (KeyError, ValueError):
        return await websocket.close(code=status_)

    await websocket.accept()
    data = await ctx.ncm.addUser(
        uid,
        websocket,
        device
    )
    if not data:
        return await websocket.close(code=status_)

    try:
        while True:
            try:
                event = await asyncio.wait_for(
                    data['queue'].get(),
                    WS_DISCONNECT_CHECK
                )
            except asyncio.TimeoutError:
                event = None

            if event is None:
                await websocket.send_json({'tick': 0})
                continue

            if event.get(TD_KEY) is not None:
                del event[TD_KEY]

            await websocket.send_json(event)

    except (
            WebSocketDisconnect,
            ConnectionError,
            WebSocketException
    ):
        print("removing ", await ctx.ncm.removeUser(uid, device))
    except Exception as e:
        print('another exception: ', e)

"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
