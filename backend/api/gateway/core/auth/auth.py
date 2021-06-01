import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from passlib.context import CryptContext

from pydantic import BaseModel

from gateway.ctx import ServerContext as ctx
from gateway.core.models import User
from common.data.local import db
from common.queries import UserQ

router = APIRouter()
load_dotenv('.env')

SECRET_KEY = os.getenv('SERVER_AUTH_SKEY')
ALGORITHM = os.getenv('SERVER_AUTH_ALGO')
TOKEN_EXPIRE = int(os.getenv('SERVER_AUTH_EXPIRE')) # 




pwd_ctx = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = '/token'
)

class Token(BaseModel):
    access_token: str
    token_type: str
    
    @classmethod
    def create(cls, data: dict, expires_delta: Optional[timedelta] = None):
        copy = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=TOKEN_EXPIRE))
        copy.update({"exp": expire})
        encoded_jwt = jwt.encode(copy, SECRET_KEY, algorithm=ALGORITHM)

        return Token(
            access_token=encoded_jwt,
            token_type='bearer'
        )
        
class AuthData(BaseModel):
    username: str
    
class UserCreds(User):
    password: str


async def getByUsername(username: str, creds = False):
    """Gets username's details"""
    user = await db.runQuery(
        username,
        pool = ctx.pool, 
        op = db.DBOP.FetchFirst, 
        query = UserQ.BY_USERNAME
    )
    if not user:
        return None
    return UserCreds(**user) if creds else User(**user)



async def authUser(username: str, password: str):
    """Checks if password equals to username's password"""
    user = await getByUsername(username, True)
    if not user:
        return False

    return False if not pwd_ctx.verify(
        password,
        user.password
    ) else User(**user.dict())
    
            

async def getUser(token: str = Depends(oauth2_scheme)):
    """Takes a token and returns a User object from it (if valid)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        _auth_inf = AuthData(username=username)
    except JWTError:
        raise credentials_exception
    user = await getByUsername(_auth_inf.username)
    if user is None:
        raise credentials_exception
    return user


## Routes



@router.post('/token', response_model=Token)
async def authToken(form: OAuth2PasswordRequestForm = Depends()):
    """/auth/token endpoint. Creates a jwt token for the user if credentials are correct"""
    user = await authUser(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Token.create(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=TOKEN_EXPIRE)
    )
    return {"access_token": access_token.access_token, "token_type": access_token.token_type, "ok": True}