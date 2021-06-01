from typing import Optional
from pydantic import BaseModel

class UserNewModel(BaseModel):
    username: str
    password: str
    email: Optional[str] = None