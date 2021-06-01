from fastapi import APIRouter, Depends

from gateway.ctx import ServerContext as ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repos import UserRepo
from gateway.resources.message.models import Message
from gateway.resources.account.models import UserNewModel

from common.response import Success, Responses
from common.errors import Error, Errors
from common.data.local import db
from common.queries import UserQ

router = APIRouter()




@router.post('/new')
async def newAccount(user : UserNewModel):
    async with UserRepo() as repo:
        if user.email is None:
            existing = await repo.run(
                user.username,
                query = UserQ.BY_USERNAME,
                op = db.DBOP.FetchFirst
            )
        else:
            existing  = await repo.run(
                user.email, 
                user.username,
                query = UserQ.BY_EMAIL_OR_USERNAME, 
                op = db.DBOP.FetchFirst)
        if existing:
            # Prioritize reporting back equal email first, over equal username
            # in case end user realize he already has an account
            if user.email is not None:
                if user.email == existing.get('email'):
                    raise Error(Errors.USER_EMAIL_EXISTS)
                
            raise Error(Errors.USER_USERNAME_EXISTS)
            
    return Success('Creating account')