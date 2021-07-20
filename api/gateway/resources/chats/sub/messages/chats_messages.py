
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from common.errors import Error, Errors


from common.response import Success


from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.repo.repos import ChatRepo


router = APIRouter()


@router.get('/{chat_id}/messages')
async def chatFetchMessages(
    chat_id: int,
    offset: Optional[int] = 0,
    amount: Optional[int] = 10,
    user: User = Depends(getUser)
):
    messages: List[Dict[str, Any]] = list()

    async with ChatRepo() as repo:

        if not await repo.getChatMemberFromUID(user.uid, chat_id):
            raise Error(Errors.UNAUTHORIZED)

        messages = await repo.getChatMessages(
            chat_id,
            offset,
            amount
        )
    return Success('', {'messages': messages})
