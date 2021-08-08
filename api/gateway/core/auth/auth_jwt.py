import hmac
import uuid
from enum import Enum
from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional, Tuple, Union

from jose import jwt
from common.settings import SERVER_SETTINGS, SYSTEM_SETTINGS, TOKEN_SETTINGS
from common.settings.settings import AUTH_SETTINGS


ENCODED_SECRET_KEY = SERVER_SETTINGS.SKEY.encode(SYSTEM_SETTINGS.ENCODING)


class TokenType(Enum):
    RefreshToken = 0
    AccessToken = 1


def tokenTypeStr(token_type: TokenType) -> str:
    return "access" if token_type == TokenType.AccessToken else "refresh"


def decodeToken(
    token: str,
    key: Optional[str] = SERVER_SETTINGS.SKEY,
    algorithms: Optional[List[str]] = [TOKEN_SETTINGS.ALGO],
    default: Optional[Any] = None,
) -> Union[dict, Any]:
    try:
        return jwt.decode(token, key, algorithms=algorithms)
    except jwt.JWTError:
        pass

    return default


def _createToken(
    subject: str,
    expires_delta: timedelta,
    key: str,
    algo: str,
    access_token: str = None,
    claims: dict = {},
) -> str:
    expire = datetime.utcnow() + expires_delta
    data = {"sub": subject, "exp": expire, **claims}
    return jwt.encode(data, key, access_token=access_token, algorithm=algo)


def createNewToken(
    subject: str,
    token_type: TokenType,
    overrides: dict = {},
    access_token=None,
    key=SERVER_SETTINGS.SKEY,
    algo=TOKEN_SETTINGS.ALGO,
):

    _time: int = datetime.now(timezone.utc).timestamp()
    _token_is_access = token_type == TokenType.AccessToken

    claims = {
        "iat": _time,
        "nbf": _time,
        "jti": str(uuid.uuid4()),
        "type": tokenTypeStr(token_type),
    }
    if _token_is_access:
        claims["fresh"] = False

    claims.update(**overrides)
    return _createToken(
        subject=subject,
        key=key,
        algo=algo,
        claims=claims,
        access_token=access_token,
        expires_delta=timedelta(TOKEN_SETTINGS.EXPIRE)
        if _token_is_access
        else timedelta(minutes=TOKEN_SETTINGS.REFRESH_EXPIRE),
    )


def verifyRefreshToken(token: str, unique: str) -> Union[None, Tuple[bool, str]]:
    payload = decodeToken(token, default=dict())
    if payload is None or payload.get("unique") is None:
        return False, "Invalid data"

    if payload.get("type") != tokenTypeStr(TokenType.RefreshToken):
        return False, "Invalid token type"

    if not hmac.compare_digest(
        payload["unique"],
        hmac.new(
            ENCODED_SECRET_KEY,
            unique.encode(TOKEN_SETTINGS.ENCODING),
            AUTH_SETTINGS.HMAC_ALGO,
        ).hexdigest(),
    ):
        return False, "Invalid unique-id"

    return True, payload.get("sub")
