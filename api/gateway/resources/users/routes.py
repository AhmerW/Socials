from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends

from gateway.core.auth.auth import getUser
from gateway.core.models import User
from common.response import Success

from gateway.data.repos.repos import UserRepo
from gateway.data.services.user_service import UserRegistrationResults, UserService
from gateway.resources.users.models import UserNewModel

from gateway.resources.users.sub.chats import users_chats
from gateway.resources.users.sub.notices import users_notices


router = APIRouter()


@router.get("/")
async def usersSelf(user: User = Depends(getUser)):
    return Success("", dict(profile=user.dict()))


@router.get("/{user_id}/")
async def usersProfile(user_id: int, user: User = Depends(getUser)):
    profile: Dict[str, Any] = dict()

    if user_id == user.uid:
        return Success("", dict(profile=user.dict()))

    async with UserRepo() as repo:
        profile = await repo.getProfile(user_id)

    return Success("", dict(profile=profile))


@router.post("/")
async def usersPosts(
    user: UserNewModel,
):
    result: UserRegistrationResults = None
    async with UserService() as service:
        result = await service.validateNewUser(user)

    return Success("Registered")


router.include_router(users_chats.router)
router.include_router(users_notices.router)
