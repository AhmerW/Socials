import os

from dotenv import load_dotenv

load_dotenv('.env')


def falseThenNone(value):
    if str(value).lower().strip() in (
        '0',
        'false',
        'none'
    ):
        return None

    return value


SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000
SERVER_PROTOCOL = 'http'
SERVER_URL = f'{SERVER_PROTOCOL}://{SERVER_IP}:{SERVER_PORT}'

# Chat Service
SERVICE_CHAT_IP = SERVER_IP
SERVICE_CHAT_PORT = 8011
SERVICE_CHAT_REDIS_IP = SERVER_IP
SERVICE_CHAT_REDIS_PORT = 8012
SERVICE_CHAT_RMQ_IP = SERVER_IP
SERVICE_CHAT_RMQ_PORT = 5672

# Notification Service
# AK : Apache Kafka
SERVICE_NC_IP = SERVER_IP
SERVICE_NC_PORT = 8021
SERVICE_NC_AK_BROKER_IP = 'localhost'
SERVICE_NC_AK_BROKER_PORT = 9092
SERVICE_NC_AK_BROKER = '{host}:{port}'.format(
    host=SERVICE_NC_AK_BROKER_IP,
    port=SERVICE_NC_AK_BROKER_PORT
)

# Cache

USER_CACHE_HOST = os.getenv('USER_CACHE_HOST')
USER_CACHE_PORT = os.getenv('USER_CACHE_PORT')
USER_CACHE_AUTH = falseThenNone(os.getenv('USER_CACHE_AUTH'))
