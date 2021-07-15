
from fastapi import APIRouter, Depends, Request
from common.data.ext.mq_event import pushEvent
from common.data.local.db import DBOP
from common.errors import Error, Errors
from common.middleware.cache.cache_reset import call_after

from common.response import Success
from common.queries import ChatQ
from gateway import ctx

from gateway.core.auth.auth import getUser
from gateway.core.models import SingleUidModel, User
from gateway.core.repo.repos import ChatRepo


from gateway.resources.chat import chat_cache
from gateway.resources.chat.chat_const import MAX_CHAT_NAME_LEN, MIN_CHAT_NAME_LEN
from gateway.resources.chat.ext import getChatLimitExceededError, isMaxChatAmount
from gateway.resources.chat.models import ChatCreateModel, ChatFetchMessagesModel, ChatID

from gateway.resources.chat.resources import chat_invites


router = APIRouter()


@router.get('/get')
async def chatGet(user: User = Depends(getUser)):

    async with ChatRepo(pool=ctx.chat_pool) as repo:
        chats = await repo.getChats(user.uid)
        members_dict = await repo.getChatsMembers(
            [chat['chat_id'] for chat in chats]
        )

        for chat in chats:
            chat['members'] = members_dict.get(chat['chat_id'])

        return Success(
            '',
            {
                'chats': chats
            }
        )


@router.post('/new')
async def chatNew(
    chat: ChatCreateModel,
    user: User = Depends(getUser)
):

    if len(chat.members) <= 0:
        raise Error(Errors.INVALID_DATA, '')

    chat.name = chat.name.strip()

    if len(chat.name) > MAX_CHAT_NAME_LEN or len(chat.name) < MIN_CHAT_NAME_LEN:
        raise Error(
            Errors.INVALID_DATA,
            'Chat name must be between {0} and {1} characters long'.format(
                MIN_CHAT_NAME_LEN,
                MAX_CHAT_NAME_LEN
            )
        )

    async with ChatRepo() as repo:
        amount = await repo.getChatAmount(user.uid)
        if isMaxChatAmount(amount, user.premium):
            raise getChatLimitExceededError(user.premium)

    if len(chat.members) >= 1:
        # dispatch notification event if chat is a group
        # otherwise wait until a message has been sent
        pass


async def updateChatMembers_fromRequest(request: Request):
    chat_id = (await request.json()).get('chat_id')
    if chat_id is not None:
        await chat_cache.updateChatMembers(chat_id)


@router.post('/messages')
async def chatFetchMessages(
    info: ChatFetchMessagesModel,
    _: User = Depends(getUser)
):
    async with ChatRepo() as repo:
        messages = await repo.getChatMessages(
            info.chat_id,
            info.offset,
            info.amount,
            info.reply_offset,
            info.replies,
        )
    return Success('', {'messages': messages})


@ router.post('/add-member')
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
