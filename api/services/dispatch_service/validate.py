from typing import Dict, Union
from fastapi import WebSocket
from aiohttp import ClientSession

from common.utils import SERVER_URL


_session: ClientSession = None


async def getClientSession() -> ClientSession:
    global _session
    if _session is None:
        _session = ClientSession()
    return _session


async def validateConnection(ws: WebSocket, ott: str) -> Union[bool, Dict]:
    session = await getClientSession()
    token = ws.headers.get('Authorization')
    if token is None:
        return False

    async with session.get(
        f'{SERVER_URL}/ott/verify?ott={ott}',
        headers={'Authorization': token}
    ) as response:
        resp = await response.json()
        if not resp.get('ok'):
            return False

        return resp


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
