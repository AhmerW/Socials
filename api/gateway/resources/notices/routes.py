from typing import Any, Dict, List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from common.response import Success

from gateway.core.auth.auth import getUser
from gateway.core.models import User

from gateway.data.repos.repos import NoticeRepo

PREFIX = "/notices"
router = APIRouter(prefix=PREFIX)


@router.get("/{notice_id}")
async def getNotice(notice_id, user: User = Depends(getUser)):
    return Success("")
