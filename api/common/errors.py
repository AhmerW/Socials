from enum import Enum, auto
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from gateway.ctx import app




class Errors(Enum):
    UNAUTHORIZED = auto()
    
    INVALID_ARGUMENTS = auto()
    INVALID_EMAIL = auto()
    INVALID_DATA = auto()
    
    OTT_NOT_FOUND = auto()

    
    CHANNEL_NOT_FOUND = auto()
    CHANNEL_EXISTS = auto()
    
    USER_EMAIL_EXISTS = auto()
    USER_USERNAME_EXISTS = auto()
    
    
class ErrorStatus(Enum):
    CHANNEL = 402
    INVALID = 202
    
class Error(Exception):
    def __init__(self, error: Errors, detail = '', status = 400, headers = {}):
        self.error : Errors = error
        self.headers = headers
        self.status = status
        self.detail = detail
            
    
    def json(self):
        return {
            'msg': str(self.error), 
            'code': self.error.value, 
            'type': 'exception'
        }
    



     
@app.exception_handler(Error)
async def Error_handler(request: Request, exc: Error):
    return JSONResponse(
        status_code = exc.status,
        headers = exc.headers,
        content = {
            'ok': False,
            'status': exc.status,
            'error': exc.json(),
            'detail': exc.detail,
            'data': {}
        }
    )

@app.exception_handler(RequestValidationError)
async def RequestValidationError_handler(request: Request, exc):
    return JSONResponse(
        status_code = 400,
        content = {
            'ok': False,
            'status': 400,
            'error': {'type': 'validation', 'msg': str(exc), 'code': None},
            'detail': '',
            'data': {}
        }
    )