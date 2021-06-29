from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    # channel ids : any of the potential different channels
    # the most common channel is chat (chat_id)

    parent_id: Optional[int] = None
    assets: Optional[List[str]] = []
    channel_id: int
    content: str

    class Config:
        anystr_strip_whitespace = True
