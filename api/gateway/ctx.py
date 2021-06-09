from passlib.context import CryptContext
from common.create_app import createApp
from common.data.ext.email_service import EmailService

class ServerContext:
    pwd_ctx = CryptContext(
        schemes=['bcrypt'],
        deprecated='auto'
    )
    email_service = EmailService()
    pool = None
    otts = {}
    
app = createApp(
    title = 'Socials',
    redoc_url = None
)