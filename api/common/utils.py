import os
from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv('.env')


"""
.env file format

# Server Data
SERVER_HOST=
SERVER_PORT=

SERVER_DB_DB=
SERVER_DB_USER=
SERVER_DB_HOST=
SERVER_DB_PORT=
SERVER_DB_PASSWD=

# SERVER_AUTH
SERVER_AUTH_SKEY=
SERVER_AUTH_ALGO=
SERVER_AUTH_EXPIRE=

# MAIL AUTH
MAIL_PASSWD=
MAIL_SKEY=

# Caching server

CACHE_SERVER_HOST=
CACHE_SERVER_PORT=
CACHE_SRVER_AUTH=
CACHE_SERVER_MAIN_DB= 

USER_CACHE_DB= 
"""


def falseThenNone(value):
    if str(value).lower().strip() in (
        '0',
        'false',
        'none'
    ):
        return None

    return value


SERVER_IP = os.getenv('SERVER_HOST')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_PROTOCOL = 'http'
SERVER_URL = f'{SERVER_PROTOCOL}://{SERVER_IP}:{SERVER_PORT}'
SYSTEM_UID = 0

IS_DEV = True  # Is development


ENCODING = 'utf-8'
SECRET_KEY = os.getenv('SERVER_AUTH_SKEY')
ALGORITHM = os.getenv('TOKEN_ALGO')
HMAC_ALGO = 'SHA256'


REFRESH_TOKEN_EXPIRE = int(os.getenv('REFRESH_TOKEN_EXPIRE'))
TOKEN_EXPIRE = int(os.getenv('TOKEN_EXPIRE'))
TOKEN_TYPE = 'Bearer'


SVC_DISPATCH_IS_EXT = falseThenNone(os.getenv('SVC_DISPATCH_IS_EXT'))
SVC_DISPATCH_IP = SERVER_IP
SVC_DISPATCH_PORT = 8021
SVC_DISPATCH_AK_BROKER_IP = 'localhost'
SVC_DISPATCH_AK_BROKER_PORT = 9092
SVC_DISPATCH_AK_BROKER = '{host}:{port}'.format(
    host=SVC_DISPATCH_AK_BROKER_IP,
    port=SVC_DISPATCH_AK_BROKER_PORT
)

# Cache


CACHE_SERVER_HOST = os.getenv('CACHE_SERVER_HOST')
CACHE_SERVER_PORT = os.getenv('CACHE_SERVER_PORT')
CACHE_SERVER_MAIN_DB = int(os.getenv('CACHE_SERVER_MAIN_DB'))
CACHE_SERVER_AUTH = falseThenNone(os.getenv('CACHE_SERVER_AUTH'))

USER_CACHE_HOST = CACHE_SERVER_HOST
USER_CACHE_PORT = CACHE_SERVER_PORT
USER_CACHE_DB = int(os.getenv('USER_CACHE_DB'))
USER_CACHE_AUTH = falseThenNone(os.getenv('CACHE_SERVER_AUTH'))
