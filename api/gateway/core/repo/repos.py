

from gateway.core.repo.base import BaseRepo
from gateway.core.models import User
from gateway.ctx import ServerContext as ctx

from common.data.local import db
from common.queries import UserQ


class UserRepo(BaseRepo):
    def __init__(self, user: User):
        self.user = user

    async def fetchProfile():
        pass

    async def verifyEmail(self) -> bool:
        pass

    async def verify(self):
        return await self.run(
            query=UserQ.VERIFY(uid=self.user.uid),
            op=db.DBOP.Execute
        )
