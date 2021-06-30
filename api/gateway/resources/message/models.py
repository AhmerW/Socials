from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):

    message_id: Optional[int] = None
    parent_id: Optional[int] = None
    assets: Optional[List[str]] = []
    chat_id: int
    content: str

    class Config:
        anystr_strip_whitespace = True
