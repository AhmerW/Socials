from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    uid: int
    username: str
    email: str
    verified: Optional[bool] = False