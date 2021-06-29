from fastapi import APIRouter, Depends
from starlette import status


from gateway.resources.ott.ot_token import OTToken
from gateway import ctx
from gateway.core.auth.auth import getUser
from gateway.core.models import User
from gateway.core.auth import auth
from gateway.ctx import app

from common.response import Success, Responses
from common.errors import Error, Errors

router = APIRouter()


@router.get('/verify')
async def verify(ott: str, user: User = Depends(auth.getUser)):
    uid = ctx.otts.get(ott)
    if uid is None:
        raise Error(Errors.OTT_NOT_FOUND)
    if uid != user.uid:
        raise Error(Errors.UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return Success(Responses.OTT_VERIFIED, data={'uid': user.uid})


@router.get('/get')
async def generate(user: User = Depends(auth.getUser)):
    ott = OTToken.generate(add=True, uid=user.uid)
    return Success(Responses.OTT_GENERATED, {'ott': ott})
