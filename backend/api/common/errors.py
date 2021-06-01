from enum import Enum, auto
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from gateway.ctx import app



class Errors(Enum):
    UNAUTHORIZED = auto()
    
    INVALID_ARGUMENTS = auto()
    INVALID_DATA = auto()
    
    CODE_NOT_FOUND = auto()
    
    CHANNEL_NOT_FOUND = auto()
    CHANNEL_EXISTS = auto()
    
    USER_EMAIL_EXISTS = auto()
    USER_USERNAME_EXISTS = auto()
    
    
class ErrorStatus(Enum):
    CHANNEL = 402
    INVALID = 202
    
class Error(Exception):
    def __init__(self, error: Errors, detail = '', status = 400):
        self.error : Errors = error
        self.status = status
        self.detail = detail
            
    
    def json(self):
        return {'msg': str(self.error), 'code': self.error.value}
    

    
@app.exception_handler(Error)
async def Error_handler(request: Request, exc: Error):
    return JSONResponse(
        status_code = exc.status,
        content = {
            'ok': False,
            'status': exc.status,
            'error': exc.json(),
            'detail': exc.detail,
            'data': {}
        }
    )
