import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class Message(BaseModel):

    message_id: Optional[int] = None
    parent_id: Optional[int] = None
    assets: Optional[List[str]] = []
    chat_id: int
    content: str

    class Config:
        anystr_strip_whitespace = True


def constructMessage(message: Dict[str, Any], **kwargs) -> dict:

    return {
        'created_at': int(time.time()),
        'reply_to': "{}",
        **message,
        **kwargs
    }
