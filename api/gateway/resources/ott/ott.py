from typing import Any, Optional
from secrets import token_urlsafe


TOKEN_BYTES = 10

_tokens = dict()


def generate(value: Any) -> str:
    token = token_urlsafe(TOKEN_BYTES)  # should always be url safe
    _tokens[token] = value
    return token


async def verify(token: Any, value: Optional[Any] = None) -> bool:
    if value is None:
        return _tokens.pop(token, None) is not None

    return _tokens.pop(token) == value
