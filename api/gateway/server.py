

from common.data.ext.cache_client import CacheClient
from gateway.resources.ott import routes as ott_routes
from gateway.resources.user import routes as user_routes
from gateway.resources.chat import routes as chat_routes
from gateway.resources.message import routes as msg_routes
from gateway.resources.account import routes as account_routes

from common.data.ext.mq_manager import MQManager, MQManagerType, serializer
from common.create_app import createPool
from common import utils
from common.response import ResponseModel, Success

from gateway import ctx
from gateway.ctx import app
from gateway.core.auth import auth


@app.on_event('startup')
async def startup_event():

    async def _helper_create_pool(schema: str):
        return await createPool(
            {'server_settings': {'search_path': schema}},
            # (Environment variables, from .env)
            host='SERVER_DB_HOST',
            port='SERVER_DB_PORT',
            user='SERVER_DB_USER',
            password='SERVER_DB_PASSWD',
            database='SERVER_DB_DB'
        )

    ctx.pool = await _helper_create_pool('public')
    ctx.chat_pool = await _helper_create_pool('chat')
    ctx.producer = MQManager(
        MQManagerType.Producer,
        broker=utils.SERVICE_NC_AK_BROKER,
        value_serializer=serializer
    )
    ctx.user_cache = await CacheClient.create(
        (utils.USER_CACHE_HOST, utils.USER_CACHE_PORT),
        password=utils.USER_CACHE_AUTH
    )

    assert not any([x is None for x in (
        ctx.pool,
        ctx.chat_pool,
        ctx.producer,
        ctx.user_cache
    )])

    try:
        await ctx.producer.start()

    except Exception as e:
        raise e(
            'Make sure the apache kafka broker is active!'
        )


@ app.on_event('shutdown')
async def shutdown_event():
    await ctx.producer.stop()


# Test endpoint
@ app.get('/', response_model=ResponseModel)
async def test_endpoint():
    return Success(
        detail='200!'
    )


# dependencies = [] arg

routers = {
    'ott': ott_routes,
    'user': user_routes,
    'chat': chat_routes,
    'message': msg_routes,
    'account': account_routes,
    'auth': auth
}

for prefix, routes in routers.items():
    assert hasattr(
        routes, 'router'), f'Missing concrete implementation of routes in {prefix}'

    app.include_router(
        getattr(
            routes,
            'router'
        ),
        prefix=f'/{prefix}'
    )
