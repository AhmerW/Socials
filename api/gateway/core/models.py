from typing import Any, Dict, Optional
from pydantic import BaseModel, create_model


# ValueModel.create(attr=(type, default: type / ...))
# (if ellipsis then attr is required)


class ValueModel(BaseModel):
    @classmethod
    def create(cls, **fields) -> "ValueModel":
        return create_model("ValueModel", __base__=cls, **fields)


class User(BaseModel):
    uid: int
    username: str
    email: Optional[str] = None
    verified: Optional[bool] = False
    premium: Optional[bool] = False


class NoticeInsert(BaseModel):
    author: int
    target: int
    event: str
    title: Optional[str] = (None,)
    body: Optional[str] = (None,)
    data: Optional[Dict[str, Any]] = None


# Single item models


class NoticeModel(BaseModel):
    notice_id: int


class TokenModel(BaseModel):
    token: str


class DeviceModel(BaseModel):
    device_id: str


class SingleUsernameModel(BaseModel):
    username: str


class SingleUidModel(BaseModel):
    uid: int
