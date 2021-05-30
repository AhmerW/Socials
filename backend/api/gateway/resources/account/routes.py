from fastapi import APIRouter, Depends

from gateway.ctx import ServerContext as ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repos import UserRepo
from gateway.resources.message.models import Message

from common.response import Success, Responses
from common.errors import Error, Errors


router = APIRouter()




@router.post('/new')
async def newAccount(user : User = Depends(getUser)):
    pass