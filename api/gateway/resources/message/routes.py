from fastapi import APIRouter, Depends

from gateway.ctx import ServerContext as ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.resources.message.models import Message

from common.response import Success, Responses
from common.errors import Error, Errors

router = APIRouter()



@router.post('/send')
async def messageSend(msg : Message, user: User = Depends(getUser)):
    msg_data = {'uid': user.uid}
    msg_data.update(msg.dict())
    await ctx.producer.send('messages', msg_data)
    return msg