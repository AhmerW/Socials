from typing import Any, Dict
from fastapi import APIRouter, Depends, Request
from common.data.ext.mq_event import pushEvent
from common.data.local.db import DBOP
from common.errors import Error, Errors
from common.middleware.cache.cache_reset import call_after

from common.response import Success
from gateway import ctx

from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.data.repos.repos import ChatRepo


from gateway.resources.chats import chat_cache
from gateway.resources.chats.chat_const import MAX_CHAT_NAME_LEN, MIN_CHAT_NAME_LEN
from gateway.resources.chats.ext import getChatLimitExceededError, isMaxChatAmount
from gateway.resources.chats.models import Chat, ChatCreateModel, ChatID

from gateway.resources.chats.sub.invites import chat_invites
from gateway.resources.chats.sub.messages import chats_messages

router = APIRouter()


@router.get("/{chat_id}")
async def chatGet(chat_id: int, user: User = Depends(getUser)):
    chat: Dict[str, Any] = dict()
    async with ChatRepo() as repo:
        chat = await repo.getChatWhereID(chat_id, user.uid)

    return Success("", dict(chat=chat))


@router.post("/")
async def chatNew(chat: ChatCreateModel, user: User = Depends(getUser)):

    if len(chat.members) <= 0:
        raise Error(Errors.INVALID_DATA, "")

    chat.name = chat.name.strip()

    if len(chat.name) > MAX_CHAT_NAME_LEN or len(chat.name) < MIN_CHAT_NAME_LEN:
        raise Error(
            Errors.INVALID_DATA,
            "Chat name must be between {0} and {1} characters long".format(
                MIN_CHAT_NAME_LEN, MAX_CHAT_NAME_LEN
            ),
        )

    async with ChatRepo() as repo:
        amount = await repo.getChatAmount(user.uid)
        if isMaxChatAmount(amount, user.premium):
            raise getChatLimitExceededError(user.premium)

    if len(chat.members) >= 1:
        # dispatch notification event if chat is a group
        # otherwise wait until a message has been sent
        pass


router.include_router(chats_messages.router)
router.include_router(chat_invites.router)
