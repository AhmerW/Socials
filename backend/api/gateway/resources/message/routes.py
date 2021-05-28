from fastapi import APIRouter, Depends

from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.resources.message.models import Message

router = APIRouter()



@router.post('/send')
async def messageSend(msg : Message, user: User = Depends(getUser)):
    return msg