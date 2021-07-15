from fastapi import APIRouter, Depends
from common.data.ext.event import Event, NewNotice, Notice
from common.data.ext.mq_event import pushEvent

from gateway import ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repo.repos import MessageRepo
from gateway.resources.message.ext import getChatMembers
from gateway.resources.message.models import Message, constructMessage, constructMessage

from common.response import Success, Responses
from common.errors import Error, Errors
from gateway.resources.message.validation import validateChatMessage

router = APIRouter()


async def insertChatMessage(user: User, msg: Message):
    async with MessageRepo(user) as repo:
        await repo.insertChatMessage(msg)


@router.post('/send')
async def messageSend(
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

    message = constructMessage(
        message,
        author_id=user.uid
    )

    for member in members:
        await pushEvent(
            Event(
                'chat.message.new',
                message,
                author=user.uid,
                target=member['uid'],
                notice=NewNotice('New message', message.get('content'))
            )
        )

    return Success('', message)
