from typing import List, Any
import secrets
from pydantic import BaseModel

from gateway.ctx import ServerContext as ctx



class OTToken(object):
    TOKEN_BYTES = 10
    dict_otts = ctx.otts
    """
    Used for generating and verifying one-time tokens.
    Primarly used as an IPC-system between the different services,
    in order to verify an user session.
    (you will often see this refferred to as 'ott' internally, this 
    is due to naming conflictions between the usage of JWT-tokens and OTTokens)
    """

    @classmethod
    def generate(cls, add = False, uid = None) -> str:
        """Generates a one-time use Token"""
        token =  secrets.token_urlsafe(cls.TOKEN_BYTES)
        if add and uid is not None:
            cls.dict_otts[token] = uid
        return token
    
    @classmethod
    async def verify(cls, uid: int, token: str, remove = True):

        raise NotImplementedError()
        