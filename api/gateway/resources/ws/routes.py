import asyncio
import dotenv
import os

from fastapi import WebSocket, status, WebSocketDisconnect, APIRouter
from websockets.exceptions import WebSocketException
import aioredis


from common import utils
from common.data.ext.mq_manager import MQManager, MQManagerType, deserializer

from gateway import ctx
from gateway.resources.ws.const import WS_DISCONNECT_CHECK, TD_KEY, MAX_WS_CON
from gateway.resources.ws.validate import *

HOST = utils.SVC_DISPATCH_IP
PORT = utils.SVC_DISPATCH_PORT


router = APIRouter()


consumer = None
running = False
clients = {
    'uid': [  # List of Websocket connections [max: MAX_WS_CON]
        {
            'id': 'device-id',
            'ws': '{ws object}',
            'queue': '{queue object}'
        }
    ]
}


async def sendNotice():
    pass


async def start():
    consumer = MQManager(
        MQManagerType.Consumer,
        utils.SVC_DISPATCH_AK_BROKER,
        value_deserializer=deserializer
    )
    await consumer.start()
    consumer.client.subscribe(pattern='ws.event.new')

    async for msg in consumer.client:
        transfer_data = msg.value.get(TD_KEY)
        if transfer_data is None:
            continue
        data = clients.get(
            transfer_data.get('target')

        )
        del msg.value[TD_KEY]
        if data:
            for con in data:
                await con['queue'].put(msg.value)

        else:
            await sendNotice()


async def addUser(uid, ws, device_id):
    """
    Adds user to the object
    Returns the data or false dependent on
    if the operation was a success.
    """
    data = clients.get(uid)
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
        clients[uid] = [ws_info]
    else:
        clients[uid].append(ws_info)

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


async def removeUser(uid, device) -> bool:
    data = clients.get(uid)
    if data is None:
        return False
    for i, con in enumerate(data):
        if not con['id'] == device:
            continue

        clients[uid].pop(i)
        info = await ctx.user_cache.con.hgetall(uid)
        info = decodeValue(info)

        if not isinstance(info, dict):
            return True

        connections = info.get('connections', 1)
        if connections == 1:
            await ctx.user_cache.con.delete(uid)
        else:
            await ctx.user_cache.con.hset(uid, 'connections', connections-1)
        print("User has disconnected.")
        # send http call for sending notice
        return True


@ router.on_event('startup')
async def onStartup():
    asyncio.create_task(start())


@ router.on_event('shutdown')
async def onShutdown():
    await consumer.stop()


@ router.websocket('/connect')
async def connectWs(websocket: WebSocket, ott: str, device: str):
    status_ = status.WS_1008_POLICY_VIOLATION
    uid = await validateConnection(websocket, ott)

    if not uid:
        return await websocket.close(code=status_)

    await websocket.accept()
    data = await addUser(
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
        await removeUser(uid, device)
    except Exception as e:
        print('another exception: ', e)

"""
When client fetches user details also return device id's
so, if current device id equals to the one returned then dont send update
otherwise send.
"""
