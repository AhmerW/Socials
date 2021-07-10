from common.data.ext.mq_manager import MQManager, MQManagerType, serializer
from common.data.ext.cache_client import CacheClient
from common.create_app import createPool
from gateway import ctx
from common import utils


loc = ctx  # Namespace


async def initializeConnections():
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

    loc.pool = await _helper_create_pool('public')
    loc.chat_pool = await _helper_create_pool('chat')
    loc.producer = MQManager(
        MQManagerType.Producer,
        broker=utils.SVC_DISPATCH_AK_BROKER,
        value_serializer=serializer
    )
    loc.cache_client = await CacheClient.create(
        (utils.CACHE_SERVER_HOST, utils.CACHE_SERVER_PORT),
        password=utils.CACHE_SERVER_AUTH,
        db=utils.CACHE_SERVER_MAIN_DB
    )

    loc.user_cache = await CacheClient.create(
        (utils.USER_CACHE_HOST, utils.USER_CACHE_PORT),
        password=utils.USER_CACHE_AUTH,
        db=utils.USER_CACHE_DB
    )

    assert not any([x is None for x in (
        loc.pool,
        loc.chat_pool,
        loc.producer,
        loc.user_cache
    )])

    try:
        await loc.producer.start()

    except Exception as e:
        raise e(
            'Make sure the apache kafka broker is active!'
        )


async def closeConnections():
    if isinstance(loc.producer, MQManager):
        await loc.producer.stop()
