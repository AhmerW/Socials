from typing import Any, Dict, List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from common.errors import Error, Errors
from common.response import Success

from gateway.core.auth.auth import getUser
from gateway.core.models import User

from gateway.core.repo.repos import NoticeRepo
router = APIRouter()


@router.get('/{user_id}/notices')
async def getNotices(
    user_id: int,
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(getUser)
):
    if user_id != user.uid:
        raise Error(Errors.UNAUTHORIZED)
    notices: List[Dict[str, Any]] = list()

    async with NoticeRepo() as repo:
        notices = await repo.getWhereTarget(user.uid, offset, limit)

    return Success('', dict(notices=notices))
