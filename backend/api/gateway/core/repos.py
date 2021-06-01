

from gateway.core.models import User
from gateway.ctx import ServerContext as ctx

from common.data.local import db
from common.queries import UserQ

class Base():
    def __init__(self):
        self.con = None
    
    async def __aenter__(self):
        if self.con is None:
            self.con = await ctx.pool.acquire()
        return self
     
    async def __aexit__(self, *a, **kw):
        await self.con.close()
        
    async def close(self):
        await self.con.close()
        
    async def run(self, *args, **kwargs):
        assert self.con is not None
        if not kwargs.get('con'):
            kwargs['con'] = self.con
        return await db.runQuery(*args, **kwargs)


class UserRepo(Base):
    async def verifyEmail(self, user : User) -> bool:
        pass