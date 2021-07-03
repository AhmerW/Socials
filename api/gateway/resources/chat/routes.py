
from fastapi import APIRouter, Depends, Request
from common.data.local.db import DBOP
from common.errors import Error, Errors
from common.middleware.cache.cache_reset import call_after

from common.response import Responses, Success
from common.queries import ChatQ, UserQ
from gateway import ctx

from gateway.core.auth.auth import getUser
from gateway.core.models import User

from gateway.core.repo.base import BaseRepo
from gateway.core.repo.repos import ChatRepo, MessageRepo
from gateway.resources.chat import chat_cache
from gateway.resources.chat.chat_const import MAX_CHATS_PREMIUM, MAX_CHATS_STANDARD, MAX_CHAT_NAME_LEN, MIN_CHAT_NAME_LEN
from gateway.resources.chat.models import Chat, ChatCreateModel, ChatFetchMessagesModel, ChatID
from gateway.resources.message.models import Message

router = APIRouter()


@router.get('/get')
async def chatGet(user: User = Depends(getUser)):

    async with ChatRepo(pool=ctx.chat_pool) as repo:
        chats = await repo.run(
            query=ChatQ.GET_ALL_CHATS(
                uid=user.uid
            ),
            op=DBOP.Fetch
        )
        members_dict = await repo.fetchChatsMembers(
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
        if repo.fetchAmount(user) > (MAX_CHATS_PREMIUM if user.premium else MAX_CHATS_STANDARD):
            raise Error(
                Errors.LIMIT_EXCEEDED,
                detail=Responses.LIMIT_EXCEEDED_PREMIUM_CHAT if user.premium else Responses.LIMIT_EXCEEDED_STANDARD_CHAT
            )

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
        messages = await repo.fetchChatMessages(
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
