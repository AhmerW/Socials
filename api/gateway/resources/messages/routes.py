from typing import Optional
from fastapi import APIRouter, Depends
from gateway.data.events import Event, NewNotice
from gateway.data.clients.mq.mq_event import pushEvent

from gateway import ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.data.repos.repos import ChatRepo, MessageRepo
from gateway.resources.messages.ext import getChatMembers
from gateway.resources.messages.models import (
    Message,
    constructMessage,
    constructMessage,
)

from common.response import Success
from common.errors import Error, Errors
from gateway.resources.messages.validation import validateChatMessage

router = APIRouter()


async def insertChatMessage(user: User, msg: Message):
    async with MessageRepo(user) as repo:
        await repo.insertChatMessage(msg)


@router.get("/{message_id}")
async def getMessages(message_id: int, _: User = Depends(getUser)):
    message = ""
    async with MessageRepo() as repo:
        pass
    return Success("", {"message": message})


@router.delete("/{message_id}")
async def deleteMessage(message_id: int, _: User = Depends(getUser)):
    async with MessageRepo() as repo:
        pass
    return Success("")


@router.post("/")
async def postMessage(
    msg: Message,
    user: User = Depends(getUser),
):

    if not validateChatMessage(msg):
        raise Error(Errors.VALIDATION_ERROR, "Invalid msg")

    message = msg.dict()
    members = await getChatMembers(message["chat_id"])
    if not members:
        raise Error(Errors.INVALID_DATA, "Please retry later")

    if not any(member.get("uid") == user.uid for member in members):
        raise Error(Errors.UNAUTHORIZED)

    async with MessageRepo(user) as repo:
        msg_in_db = await repo.insertChatMessage(msg)
        message["message_id"] = msg_in_db.get("message_id")

    message = constructMessage(message, author_id=user.uid)

    for member in members:
        await pushEvent(
            Event(
                "chat.message.new",
                message,
                author=user.uid,
                target=member["uid"],
                notice=NewNotice("New message", message.get("content")),
            )
        )

    return Success("", message)
