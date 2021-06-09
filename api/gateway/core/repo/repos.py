

from gateway.core.repo.base import BaseRepo
from gateway.core.models import User
from gateway.ctx import ServerContext as ctx

from common.data.local import db
from common.queries import UserQ

class UserRepo(BaseRepo):
    async def fetchProfile():
        pass
    
    async def verifyEmail(self, user : User) -> bool:
        pass