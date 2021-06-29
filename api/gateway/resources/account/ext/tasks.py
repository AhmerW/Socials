from enum import Enum

from fastapi import BackgroundTasks, FastAPI
from common.internal.limits import INTERNAL_USERNAME_PREFIX, MAX_USERNAME_LEN

from common.queries import UserQ
from common.data.local.html import HTML
from gateway import ctx
from gateway.resources.account.ext import registrator


def registrationAllowUsername(username: str) -> bool:
    if len(username) > MAX_USERNAME_LEN:
        return False
    if not username.strip():
        return False

    return True


def registrationVerify(token: str, email: str) -> bool:
    return registrator.confirmEmailToken(token) == email


async def initVerification(email: str):
    """Generates and sends verification-email to target-mail"""
    token = registrator.generateEmailToken(email)
    html = HTML.REGISTRATION_PENDING_EMAIL.format(
        f'{ctx.ACCOUNT_VERIFY_URL}?token={token}')

    print('sending')
    return await ctx.email_service.sendMail(
        body=html,
        target=email,
        subject='Account notification'
    )
