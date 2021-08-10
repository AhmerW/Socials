from fastapi import APIRouter, Depends
from starlette import status


from gateway.resources.ott import ott
from gateway import ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.auth import auth
from gateway.ctx import app

from common.response import Success, Responses
from common.errors import Error, Errors

router = APIRouter()


@router.get("/verify")
async def verify(
    verified: bool = Depends(ott.verify),
    user: User = Depends(auth.getUser),
):
    if not verified:
        raise Error(Errors.UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return Success(Responses.OTT_VERIFIED, data={"uid": user.uid})


@router.get("/get")
async def generate(
    user: User = Depends(auth.getUser),
):
    code = ott.generate(user.uid)
    return Success(Responses.OTT_GENERATED, {"ott": code})
