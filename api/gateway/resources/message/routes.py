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
    # In chat context name it chat/_id instead of a channel
    message = msg.dict()
    message['chat_id'] = message.pop('channel_id')

    background_tasks.add_task(
        insertChatMessage,
        user,
        msg
    )

    members = await getChatMembers(message['chat_id'])
    for member in members:
        await pushEvent(
            'user.message.new',
            createEvent(
                Events.Message,
                message,
                target=member
            ))

    await ctx.producer.send(
        'user.message.new',
        createEvent(
            Events.Message,
            message,
            target=user.uid
        )
    )

    return Success('', message)
