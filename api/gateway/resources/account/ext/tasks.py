from enum import Enum

from fastapi import BackgroundTasks, FastAPI
from common.internal.limits import INTERNAL_USERNAME_PREFIX, MAX_USERNAME_LEN

from common.queries import UserQ
from common.data.local.html import HTML
from gateway.ctx import ServerContext as ctx
from gateway.resources.account.ext.registrator import Registrator


registrator = Registrator()


def registrationAllowUsername(username: str) -> bool:
    if len(username) > MAX_USERNAME_LEN:
        return False
    return not username.startswith(INTERNAL_USERNAME_PREFIX)


def registrationVerify(token: str, email: str) -> bool:
    return registrator.confirm(token) == email


class RegistrationProcType(Enum):
    PENDING = 0,  # Registration not done, must verify email
    EXISTING = 1  # Registration account already existing


async def registrationProc(email: str, rpt: RegistrationProcType):
    if rpt == RegistrationProcType.PENDING:
        token = registrator.generate(email)
        html = HTML.REGISTRATION_PENDING_EMAIL.format(token)

    elif rpt == RegistrationProcType.EXISTING:
        html = HTML.REGISTRATION_EXISTING

    await ctx.email_service.sendMail(
        body=html,
        target=email,
        subject='Account notification'
    )
