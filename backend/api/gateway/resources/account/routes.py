import os

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_mail import MessageSchema, FastMail
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from email_validator import validate_email as validateEmail
from email_validator import EmailNotValidError

from gateway.ctx import ServerContext as ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repo.repos import UserRepo
from gateway.core.repo.base import BaseRepo
from gateway.resources.message.models import Message
from gateway.resources.account.models import UserNewModel
from gateway.resources.account.ext.registrator import Registrator
from gateway.resources.account.ext.tasks import (
    registrationProc,
    RegistrationProcType
)

from common.response import Success, Responses
from common.errors import Error, Errors
from common.data.local import db
from common.queries import Query, UserQ, AccountQ

router = APIRouter()
manager = Registrator()

## Simple static file serving
router.mount(
    '/web/static',
    StaticFiles(directory=os.path.join('web', 'static')), name="static"
)
templates = Jinja2Templates(directory=os.path.join('web', 'templates'))


@router.post('/new')
async def newAccount(user : UserNewModel, background_tasks: BackgroundTasks):
    _success = Success(
        Responses.REGISTRATION_PENDING,
        # background task is created at all places we return this
        status = 202
    )
    
    if user.email is not None:
        try:
            validateEmail(user.email)
        except EmailNotValidError as e:
            raise Error(Errors.INVALID_EMAIL, detail = str(e))
    
    # using this repo in order to keep
    # the connection object and not create a new one
    # each time we run a query.
    async with BaseRepo() as repo:
        if user.email is None:
            existing = await repo.run(
                query = UserQ.FROM_USERNAME(username=user.username),
                op = db.DBOP.FetchFirst
            )
        else:
            existing  = await repo.run(
                query = UserQ.FROM_USERNAME_OR_EMAIL(
                    email = user.email, 
                    username = user.username
                ), 
                op = db.DBOP.FetchFirst)
        if existing:
            if user.username == existing.get('username'):
                raise Error(Errors.USER_USERNAME_EXISTS, detail = 'Username already exists')
                
            if user.email is not None:
                if user.email == existing.get('email'):
                    # Return Success even though email is invalid
                    # so user cant bruteforce his way into finding a lot of valid emails
                    
                    # ...Send email to user stating that:
                    # -> Someone tried to register using this mail
                    # -> this is your username in case you forgot
                    # -> if you forgot your password reset it here
                    # -> If you did not try to register, please ignore this email.
                    background_tasks.add_task(
                        registrationProc,
                        email = existing.get('email'),
                        rpt = RegistrationProcType.EXISTING
                    )
                    return _success
        if user.email is None:
            await repo.run(
                query = AccountQ.NEW(
                    username = user.username, 
                    display_name = user.username,
                    email = user.email, 
                    password = ctx.pwd_ctx.hash(user.password),
                    verified = True
                ),
                op = db.DBOP.Execute
            )
         
            return Success(Responses.REGISTRATION_COMPLTE, status = 202)
        
        background_tasks.add_task(
            registrationProc,
            email = user.email,
            rpt = RegistrationProcType.PENDING
        )
        return _success
    