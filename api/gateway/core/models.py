from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    uid: int
    username: str
    email: Optional[str] = None
    verified: Optional[bool] = False
    premium: Optional[bool] = False