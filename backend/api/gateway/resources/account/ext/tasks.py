from enum import Enum

from fastapi import BackgroundTasks, FastAPI

from common.queries import UserQ
from common.data.local.html import HTML



class RegistrationProcType(Enum):
    PENDING = 0,
    EXISTING = 1

async def registrationProc(email: str, rpt : RegistrationProcType):
    if rpt == RegistrationProcType.PENDING:
        email = 0
    elif rpt == RegistrationProcType.COMPLETE:
        email = 0
