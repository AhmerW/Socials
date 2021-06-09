from abc import ABC, abstractmethod
from asyncpg import Connection

from gateway.ctx import ServerContext as ctx
from common.data.local import db

class BaseInterface(ABC):

    @abstractmethod
    async def delete(self):
        pass
    
    
class BaseRepo():
    def __init__(self):
        self.con : Connection = None
        
    def __setattr__(self, name, value):
        if name == 'con' and value is not None:
            if not isinstance(value, Connection):
                raise RuntimeError('Connection of type <{0}> not permitted.'.format(Connection))
        
        return super.__setattr__(self, name, value)
    
    async def __aenter__(self):
        if self.con is None:
            self.con = await ctx.pool.acquire()
        return self
     
    async def __aexit__(self, *a, **kw):
        await self.close()
        
    async def close(self):
        await self.con.close()

        
    async def run(self, *args, **kwargs):
        if not kwargs.get('con'):
            kwargs['con'] = self.con
        return await db.runQuery(*args, **kwargs)

