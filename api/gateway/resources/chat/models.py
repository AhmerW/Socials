from typing import List
from pydantic import BaseModel

from gateway.core.models import User


class Chat(BaseModel):
    name: str
    members: List[User]


class ChatCreateModel(BaseModel):
    members: List[int]
    name: str = None
