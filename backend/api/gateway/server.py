import os
import secrets
import asyncio

from fastapi import Depends, HTTPException, status
from aiokafka import AIOKafkaProducer
import asyncpg


from gateway.resources.ott import routes as ott_routes
from gateway.resources.user import routes as user_routes
from gateway.resources.message import routes as msg_routes
from gateway.resources.account import routes as account_routes

from common.data.ext.mq_manager import MQManager, MQManagerType, serializer
from common.create_app import createPool
from common import utils
from common.response import Success, Responses
from common.errors import Error, Errors


from gateway.ctx import ServerContext as ctx
from gateway.ctx import app
from gateway.core.auth import auth
from gateway.core.models import User

APP_RUN_TESTS = False

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

#dependencies = [] arg

app.include_router(ott_routes.router, prefix='/ott')
app.include_router(user_routes.router, prefix='/user')
app.include_router(msg_routes.router, prefix='/message')
app.include_router(account_routes.router, prefix='/account')


app.include_router(auth.router, prefix='/auth')