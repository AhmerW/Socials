from abc import ABC, abstractmethod
from asyncpg import Connection

class BaseInterface(ABC):
    
    @abstractmethod
    async def delete(self):
        pass
    
    
class Base():
    def __init__(self):
        self.con : Connection = None
        
    def __setattr__(self, name, value):
        if name == 'con':
            if not isinstance(value, Connection):
                raise RuntimeError('Connection attribute not of type <{0}>'.format(Connection))
        
        return super.__setattr__(self, name, value)
    
    async def __aenter__(self):
        if self.con is None:
            self.con = await ctx.pool.acquire()
        return self
     
    async def __aexit__(self, *a, **kw):
        self.close()
        
    async def close(self):
        await self.con.close()

        
    async def run(self, *args, **kwargs):
        if not kwargs.get('con'):
            kwargs['con'] = self.con
        return await db.runQuery(*args, **kwargs)

