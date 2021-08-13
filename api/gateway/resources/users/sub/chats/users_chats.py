from gateway.data.repos.repos import ChatRepo
from gateway.core.models import User
from gateway.core.auth.auth import getUser
from gateway import ctx
from common.response import Success
from fastapi import APIRouter, Depends
from common.errors import Error, Errors
from gateway.data.services import user_service


router = APIRouter()


@router.get("/{user_id}/chats")
async def usersChats(user_id: int, user: User = Depends(getUser)):
    if user_id != user.uid:
        raise Error(Errors.UNAUTHORIZED)

    async with ChatRepo(pool=ctx.chat_pool) as repo:
        chats = await repo.getChats(user.uid)
        members_dict = await repo.getChatsMembers([chat["chat_id"] for chat in chats])

        for chat in chats:
            chat["members"] = members_dict.get(chat["chat_id"])

        return Success("", {"chats": chats})
