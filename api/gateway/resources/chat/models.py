from typing import List, Optional
from pydantic import BaseModel

from gateway.core.models import User


class ChatID(BaseModel):
    chat_id: int


class Chat(BaseModel):
    name: str
    members: List[User]


class ChatCreateModel(BaseModel):
    members: List[int]
    name: Optional[str] = None


class ChatFetchMessagesModel(BaseModel):
    chat_id: int

    offset: Optional[int] = 0
    amount: Optional[int] = 10

    reply_offset: Optional[int] = 0
    replies: Optional[int] = 5
