

from gateway.core.repo.base import Base
from gateway.core.models import User
from gateway.ctx import ServerContext as ctx

from common.data.local import db
from common.queries import UserQ

class UserRepo(Base):
    async def fetchProfile():
        pass
    
    async def verifyEmail(self, user : User) -> bool:
        pass