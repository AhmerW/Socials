import os

from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

from fastapi_mail import ConnectionConfig


load_dotenv()

REGISTER_CONF = ConnectionConfig(
    MAIL_USERNAME='socials.site',
    MAIL_FROM='socials.site@gmail.com',
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PASSWORD=os.getenv('MAIL_PASSWD'),
    MAIL_PORT=587,
    USE_CREDENTIALS=True,
    MAIL_TLS=True,
    MAIL_SSL=False
)


_tokens = {}
_skey = os.getenv('MAIL_SKEY'),
_spass = os.getenv('SERVER_AUTH_SKEY')
if isinstance(_skey, tuple) and len(_skey) >= 1:
    _skey = _skey[0]


def existsEmailToken(token) -> bool:
    return not (_tokens.get(token) is None)


def generateEmailToken(email):
    return URLSafeTimedSerializer(_skey).dumps(
        email,
        salt=_spass
    )


def confirmEmailToken(token, expire=900):
    try:
        email = URLSafeTimedSerializer(_skey).loads(
            token,
            salt=_spass,
            max_age=expire
        )
    except:
        return False
    return email
