from fastapi import APIRouter, Depends

from gateway.core.auth.auth import getUser
from gateway.core.models import User
from common.response import Success

router = APIRouter()


@router.get("/profile")
async def userProfile(user: User = Depends(getUser)):
    return Success('', user.dict())