from typing import Optional, List

from pydantic import BaseModel 

message_types = ['message', 'comment']

class MessageData(BaseModel):
    content: str
    user: int
    channel_id: int
    type_: 'message'
    assets: Optional[List[str]] = []