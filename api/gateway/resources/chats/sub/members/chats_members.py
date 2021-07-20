
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
from gateway.core.repo.repos import ChatRepo


from gateway.resources.chats import chat_cache
from gateway.resources.chats.chat_const import MAX_CHAT_NAME_LEN, MIN_CHAT_NAME_LEN
from gateway.resources.chats.ext import getChatLimitExceededError, isMaxChatAmount
from gateway.resources.chats.models import Chat, ChatCreateModel, ChatID

from gateway.resources.chats.sub.invites import chat_invites


router = APIRouter()


async def updateChatMembers_fromRequest(request: Request):
    chat_id = (await request.json()).get('chat_id')
    if chat_id is not None:
        await chat_cache.updateChatMembers(chat_id)


@ router.post('/member')
@ call_after(
    only_on_success=True,
    callback=updateChatMembers_fromRequest
)
async def chatAddUser(
    request: Request,
    id_: ChatID,
    user: User = Depends(getUser)
):
    chat_id = id_.chat_id

    return Success('test')


router.include_router(chat_invites.router)
