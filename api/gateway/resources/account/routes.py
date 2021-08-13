import os
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi_mail import MessageSchema, FastMail
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from email_validator import validate_email as validateEmail
from email_validator import EmailNotValidError
from gateway.data.email.html import HTML, TEMPLATE_DIR
from common.internal.access import InternalUser
from common.internal.limits import INTERNAL_USERNAME_PREFIX


from gateway import ctx
from gateway.core.auth.auth import getUser, OptionalUser
from gateway.core.models import TokenModel, User
from gateway.data.repos.repos import UserRepo
from gateway.data.repos.base import BaseRepo
from gateway.resources.account.models import UserNewModel
from gateway.resources.account.ext import registrator
from gateway.resources.account.ext.tasks import (
    initVerification,
    registrationVerify,
    registrationAllowUsername,
)

from common.response import ResponseModel, Success, Responses
from common.errors import Error, Errors
from gateway.data.db.db import DBOP
from gateway.data.db.queries.account_q import AccountQ
from gateway.data.db.queries.user_q import UserQ

from gateway.data.services.user_service import UserService


router = APIRouter()


# Simple static file serving
router.mount(
    "/web/static", StaticFiles(directory=os.path.join("web", "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join("web", "templates"))


@router.post("/")
async def newAccount(
    user: UserNewModel,
    background_tasks: BackgroundTasks,
    base: Optional[User] = Depends(OptionalUser),
):

    _success = Success(Responses.REGISTRATION_PENDING, status=202)

    async with UserService() as service:
        pass

    # <Validation>

    if not registrationAllowUsername(user.username.lower()):
        raise Error(Errors.USER_INVALID_USERNAME, detail="Username not allowed")

    if user.username.startswith(INTERNAL_USERNAME_PREFIX):
        if base is None or (not base.username == InternalUser.username):
            raise Error(Errors.USER_INVALID_USERNAME, detail="Username not allowed")

    if user.email is not None:
        try:
            validateEmail(user.email)
        except EmailNotValidError as validation_msg:
            raise Error(Errors.INVALID_EMAIL, detail=str(validation_msg))

    # <Registration>

    async with BaseRepo() as repo:
        if user.email is None:
            existing = await repo.run(
                query=UserQ.FROM_USERNAME(username=user.username), op=DBOP.FetchFirst
            )
        else:
            existing = await repo.run(
                query=UserQ.FROM_USERNAME_OR_EMAIL(
                    email=user.email, username=user.username
                ),
                op=DBOP.FetchFirst,
            )
        if existing:
            if user.username == existing.get("username"):
                raise Error(
                    Errors.USER_INVALID_USERNAME, detail="Username already exists"
                )

            if user.email is not None:
                if user.email == existing.get("email"):
                    background_tasks.add_task(
                        ctx.email_service.sendMail,
                        body=HTML.REGISTRATION_EXISTING,
                        target=user.email,
                        subject="Account notification",
                    )
                    return _success

        await repo.run(
            query=AccountQ.NEW(
                username=user.username,
                display_name=user.username,
                email=user.email,
                password=ctx.pwd_ctx.hash(user.password),
                verified=(user.email is None),
            ),
            op=DBOP.Execute,
        )

        if user.email is None:
            return Success(Responses.REGISTRATION_COMPLTE, status=202)

        background_tasks.add_task(initVerification, email=user.email)
        return _success


@router.post("/verify-attempt")
async def verifyAccount(data: TokenModel, user: User = Depends(getUser)):
    if user.verified:
        return Success("Your account is already verified.")
    error = Error(Errors.INVALID_DATA, detail="Could not verify this account")
    if user.email is None:
        raise error

    if user.verified:
        return Success(Responses.ACCOUNT_VERIFIED)

    if registrationVerify(data.token, user.email):
        async with UserRepo(user) as repo:
            await repo.verify()
            return Success(Responses.ACCOUNT_VERIFIED)

    raise error


@router.get("/verify")
async def verificationVerify(token: str):
    return HTMLResponse(HTML.REGISTRATION_PENDING)


@router.get("/resend")
async def verificationResend(user: User = Depends(getUser)):
    if user.verified:
        return Success("Your account is already verified.")

    async with UserRepo(user, acquire=False) as repo:
        await repo.resendVerification()

    return Success(Responses.REGISTRATION_PENDING)
