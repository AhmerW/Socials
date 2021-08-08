from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from common.errors import Error, Errors


from common.response import Success


from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.data.repos.repos import ChatRepo


router = APIRouter()


@router.get("/{chat_id}/messages")
async def chatFetchMessages(
    chat_id: int,
    offset: Optional[int] = 0,
    amount: Optional[int] = 10,
    order: Optional[str] = "desc",
    user: User = Depends(getUser),
):
    messages: List[Dict[str, Any]] = list()
    print(offset)

    if len(order) > 4 or order.lower() not in ("desc", "asc"):
        raise Error(Errors.INVALID_ARGUMENTS, "Order must be 'desc' or 'asc'")

    async with ChatRepo() as repo:

        if not await repo.getChatMemberFromUID(user.uid, chat_id):
            raise Error(Errors.UNAUTHORIZED)

        messages = await repo.getChatMessages(chat_id, offset, amount, order=order)
    return Success("", {"messages": messages})
