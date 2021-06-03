from fastapi import APIRouter, Depends

from gateway.ctx import ServerContext as ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repo.repos import UserRepo
from gateway.resources.message.models import Message
from gateway.resources.account.models import UserNewModel

from common.response import Success, Responses
from common.errors import Error, Errors
from common.data.local import db
from common.queries import UserQ, AccountQ

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
            if user.username == existing.get('username'):
                raise Error(Errors.USER_EMAIL_EXISTS)
                

            if user.email == existing.get('email'):
                # Return Success even though email is invalid
                # so user cant bruteforce his way into finding a lot of valid emails
                return Success()
        
        account = await repo.run(
            user.username,
            user.email,
            user.password,
            query = AccountQ.NEW,
            op = db.DBOP.FetchFirst
        )
         
    return Success('Creating account')