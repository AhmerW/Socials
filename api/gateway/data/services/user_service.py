from typing import Optional, Union
from gateway.core.models import User
from gateway.data.repos.base import Base, BaseService


from gateway.data.repos.user_repo import UserRepo


class UserService(BaseService):
    async def __aenter__(self, pool=None) -> "UserService":
        return await super().__aenter__(UserRepo, pool=pool)

    # Get the user object

    async def _getUser(self, value: Union[int, str]) -> Optional[User]:
        user = await self._repo.get(value)
        if not user:
            return None

        return User(**user)

    async def getUserFromUid(self, uid: int) -> Optional[User]:
        return await self._getUser(uid)

    async def getUserFromUsername(self, username: str) -> Optional[User]:
        return await self._getUser(username)

    async def exists(self, uid: int) -> bool:

        user = await self._getUser(uid)
        return user is not None

    # Chat

    async def getUsersChats(self, user: User):
        pass
