from pydantic import BaseModel

class Message(BaseModel):
    channel_id: int
    content: str

    