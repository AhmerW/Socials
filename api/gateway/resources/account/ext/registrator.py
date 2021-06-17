import os

from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

from fastapi_mail import MessageSchema, FastMail, ConnectionConfig


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

class Registrator():
    def __init__(self):
        # email : details
        self._tokens = {}
        self._skey = os.getenv('MAIL_SKEY'),
        self._spass = os.getenv('SERVER_AUTH_SKEY')
        

        
    def generate(self, email):
        return URLSafeTimedSerializer(self._skey).dumps(
            email,
            salt = self._spass
        )
        
    async def confirm(self, token, expire=900):
        try:
            email = URLSafeTimedSerializer(self._skey).loads(
                token,
                salt=self._spass,
                max_age=expire
            )
        except:
            return False 
        return email
        
