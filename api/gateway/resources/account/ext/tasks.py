from enum import Enum

from fastapi import BackgroundTasks, FastAPI

from common.queries import UserQ
from common.data.local.html import HTML
from gateway.ctx import ServerContext as ctx



class RegistrationProcType(Enum):
    PENDING = 0,
    EXISTING = 1

async def registrationProc(email: str, rpt : RegistrationProcType):
    if rpt == RegistrationProcType.PENDING:
        html = HTML.REGISTRATION_PENDING
    
    elif rpt == RegistrationProcType.EXISTING:
        html = HTML.REGISTRATION_EXISTING
        

    await ctx.email_service.sendMail(
        body = html,
        target = email,
        subject = 'Account notification'
    )