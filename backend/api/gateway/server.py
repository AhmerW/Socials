import os
import secrets
import asyncio
from aiokafka import AIOKafkaProducer

from fastapi import Depends, HTTPException, status
import asyncpg


from gateway.resources.user import routes as user_routes
from gateway.resources.message import routes as msg_routes
from gateway.resources.account import routes as account_routes

from common.mq_manager import MQManager, MQManagerType, serializer
from common.create_app import createPool
from common import utils
from common.response import Success, Responses
from common.errors import Error, Errors


from gateway.ctx import ServerContext as ctx
from gateway.ctx import app
from gateway.core.auth import auth
from gateway.core.models import User




@app.on_event('startup')
async def startup_event():
    ctx.pool = await createPool(
        {'server_settings': {'search_path': 'public'}},
        host='SERVER_DB_HOST',
        port='SERVER_DB_PORT',
        user='SERVER_DB_USER',
        password='SERVER_DB_PASSWD',
        database='SERVER_DB_DB'
    )
    
    assert ctx.pool != None

    ctx.producer = MQManager(
        MQManagerType.Producer,
        broker = utils.SERVICE_NC_AK_BROKER,
        value_serializer = serializer
    )

    await ctx.producer.start()
    
@app.on_event('shutdown')
async def shutdown_event():
    await ctx.producer.stop()

@app.get('/verify')
async def verify(code: str, user: User = Depends(auth.getUser)):
    uid = ctx.codes.get(code)
    if uid is None:
        raise Error(Errors.CODE_NOT_FOUND)
    if uid != user.uid:
        raise Error(Errors.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED) 
    
    return Success(Responses.CODE_VERIFIED, data = {'uid': user.uid})

@app.get('/code')
async def generateCode(user: User = Depends(auth.getUser)):
    code:str = secrets.token_urlsafe(10)
    ctx.codes[code] = user.uid
    return Success(Responses.CODE_GENERATED, {'code': code})

#dependencies = [] arg

app.include_router(user_routes.router, prefix='/user')
app.include_router(msg_routes.router, prefix='/message')
app.include_router(account_routes.router, prefix='/account')


app.include_router(auth.router, prefix='/auth')