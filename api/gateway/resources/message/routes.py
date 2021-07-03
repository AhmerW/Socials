import time
import asyncio
from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks
from common.data.ext.event import Events, createEvent
from common.data.ext.mq_event import pushEvent

from gateway import ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repo.repos import MessageRepo
from gateway.resources.message.ext import getChatMembers
from gateway.resources.message.models import Message

from common.response import Success, Responses
from common.errors import Error, Errors
from gateway.resources.message.validation import validateChatMessage

router = APIRouter()


async def insertChatMessage(user: User, msg: Message):
    async with MessageRepo(user) as repo:
        await repo.insertChatMessage(msg)


@router.post('/send')
async def messageSend(
    background_tasks: BackgroundTasks,
    msg: Message,
    user: User = Depends(getUser),
):

    if not validateChatMessage(msg):
        raise Error(
            Errors.VALIDATION_ERROR,
            'Invalid msg'
        )

    message = msg.dict()
    members = await getChatMembers(message['chat_id'])
    if not members:
        raise Error(Errors.INVALID_DATA, 'Please retry later')

    if not any(member.get('uid') == user.uid for member in members):
        raise Error(Errors.UNAUTHORIZED)

    async with MessageRepo(user) as repo:
        msg_in_db = await repo.insertChatMessage(msg)
        message['message_id'] = msg_in_db.get('message_id')

    message['created_at'] = int(time.time())
    message['author_id'] = user.uid
    message['replies'] = []

    for member in members:
        await pushEvent(
            'user.message.new',
            createEvent(
                Events.Message,
                message,
                target=member
            ))

    return Success('', message)
