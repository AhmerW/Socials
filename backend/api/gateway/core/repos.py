from gateway.core.models import User
from gateway.ctx import ServerContext as ctx


class Base():
    def __init__(self):
        self.pool = ctx.pool.acquire()
        
    def __enter__(self):
        return self
     
    def __exit__(self, *a, **kw):
        self.pool.close()


class UserRepo():
    def verifyEmail(self, user : User):
        pass