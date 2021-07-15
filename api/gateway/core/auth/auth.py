from enum import unique
import hmac
from typing import Optional
from dotenv import load_dotenv


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from pydantic import BaseModel
from starlette.requests import Request
from common.internal.access import InternalUser
from common.internal.limits import INTERNAL_USERNAME_PREFIX


from gateway import ctx
from gateway.core.auth.auth_jwt import ENCODED_SECRET_KEY, TokenType, createNewToken, decodeToken, verifyRefreshToken
from gateway.core.models import TokenModel, User
from common.response import Success, Responses
from common.errors import Error, Errors
from common.data.local import db
from common.queries import Query, UserQ
from common.utils import *

router = APIRouter()
load_dotenv('.env')


pwd_ctx = ctx.pwd_ctx

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/token'
)

credentials_exception = Error(
    Errors.UNAUTHORIZED,
    detail='Could not validate credentials',
    status=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW-Authenticate": TOKEN_TYPE}
)
user_auth_exception = Error(Errors.UNAUTHORIZED,
                            'You are not authorized to login with this username')


class AuthData(BaseModel):
    username: str


class UserCreds(User):
    password: str


async def getByUsername(username: str, creds=False):
    """Gets username's details"""
    user = await db.runQuery(
        pool=ctx.pool,
        op=db.DBOP.FetchFirst,
        query=UserQ.FROM_USERNAME.format(username=username)
    )
    if not user:
        return None
    return UserCreds(**user) if creds else User(**user)


async def getUser(token: str = Depends(oauth2_scheme)) -> User:
    """Takes a token and returns a User object from it (if valid)."""

    payload = decodeToken(token, default=dict())
    if payload is None or payload.get('sub') is None:
        raise credentials_exception

    user = await getByUsername(payload['sub'])
    if user is None:
        raise credentials_exception

    return user


async def authUser(username: str, password: str):
    """Checks if password equals to username's password"""

    user = await getByUsername(username, True)
    if not user:
        return False

    return False if not pwd_ctx.verify(
        password,
        user.password
    ) else User(**user.dict())

# Internal user ( // Optional base user for login and register purposes)


async def OptionalUser(request: Request):
    token = request.headers.get('Base')
    if token is None:
        return None
    return await getUser(token)


async def _checkIsInternal(username: str, base: User = None):
    if username.lower().startswith(INTERNAL_USERNAME_PREFIX):
        if base is None:
            raise user_auth_exception
        # specifically for login we need to check if the base is
        # an authorized internal user account

        # allow login with an internal user if the base is admin
        if not base.username == InternalUser.username:
            raise user_auth_exception

    return base


# Routes

@ router.post('/login')
async def authenticateUser(
    device_id: str = Form(...),
    form: OAuth2PasswordRequestForm = Depends(),
    base: Optional[User] = Depends(OptionalUser)
):
    """/auth/login endpoint. Creates a jwt token for the user if refresh toen is correct"""

    await _checkIsInternal(form.username, base=base)

    user = await authUser(
        form.username,
        form.password
    )
    if not user:
        raise credentials_exception

    return Success(
        'Success',
        {
            "access_token": createNewToken(user.username, token_type=TokenType.AccessToken),
            "refresh_token": createNewToken(
                user.username,
                token_type=TokenType.RefreshToken,
                overrides={
                    'unique': hmac.new(
                        ENCODED_SECRET_KEY,
                        device_id.encode(ENCODING),
                        HMAC_ALGO
                    ).hexdigest()
                }
            ),
            "token_type": TOKEN_TYPE
        }
    )


class RefreshTokenModel(TokenModel):
    device_id: str


@ router.post('/refresh')
async def refreshToken(
    token: RefreshTokenModel
):
    """
    Creates a jwt token for the user if it passes the valdiation test,
    - if the device_id matches the one the token was created with.
      (compared via hmac.compare_digest)
    - it's a refresh token.
    """
    response, value = verifyRefreshToken(
        token.token, token.device_id)
    if not response:
        raise Error(
            Errors.UNAUTHORIZED,
            detail=value,
            status=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": TOKEN_TYPE}
        )

    return Success(
        'Success',
        {
            "access_token": createNewToken(value, token_type=TokenType.AccessToken),
            "token_type": TOKEN_TYPE
        }
    )
