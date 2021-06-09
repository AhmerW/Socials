from fastapi import APIRouter, Depends

from gateway.core.auth.auth import getUser
from gateway.core.models import User

router = APIRouter()

