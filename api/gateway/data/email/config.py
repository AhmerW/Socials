from fastapi_mail import ConnectionConfig

import os
from dotenv import load_dotenv

load_dotenv()


EMAIL_CONF = ConnectionConfig(
    MAIL_USERNAME="socials.site",
    MAIL_FROM="socials.site@gmail.com",
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PASSWORD=os.getenv("MAIL_PASSWD"),
    MAIL_PORT=587,
    USE_CREDENTIALS=True,
    MAIL_TLS=True,
    MAIL_SSL=False,
)
