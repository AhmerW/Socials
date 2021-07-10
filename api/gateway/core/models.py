from typing import Optional
from pydantic import BaseModel

from common.response import Success


class User(BaseModel):
    uid: int
    username: str
    email: Optional[str] = None
    verified: Optional[bool] = False
    premium: Optional[bool] = False


class TokenModel(BaseModel):
    token: str


class DeviceIDModel(BaseModel):
    device_id: str
