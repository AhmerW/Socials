from fastapi import APIRouter, Depends

from gateway.core.auth.auth import getUser
from gateway.core.models import User
from common.response import Success

from gateway.resources.users.sub.chats import users_chats
from gateway.resources.users.sub.notices import users_notices


router = APIRouter()


@router.get("/{user_id}")
async def userProfile(
    user_id: int,
    user: User = Depends(getUser)
):
    if user_id == user.uid:
        return Success('', user.dict())


router.include_router(users_chats.router)
router.include_router(users_notices.router)
