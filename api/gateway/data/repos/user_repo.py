from typing import Any, Optional, Union
from gateway.core.models import User

from gateway.data.repos.base import Base


from gateway.data.db.queries.account_q import AccountQ
from gateway.data.db.queries.user_q import UserQ


class UserRepo(Base):
    async def __aenter__(self) -> "UserRepo":
        return await super().__aenter__()

    async def create(
        self,
        username: str,
        display_name: str,
        password: str,
        email: str,
        verified: bool,
    ) -> str:
        return await self._con.execute(
            AccountQ.NEW.format(
                username=username,
                display_name=display_name,
                password=password,
                email=email,
                verified=verified,
            ),
        )

    async def get(
        self,
        value: Union[int, str],
    ) -> Optional[User]:

        if isinstance(value, int):
            return await self._con.fetchFirst(
                UserQ.PROFILE_FROM_UID,
                uid=value,
            )

        user = await self._con.fetchFirst(
            UserQ.PROFILE_FROM_USERNAME,
            username=value,
        )
        if user:
            return User(**user)

    async def getFromUsernameOrEmail(
        self,
        username: str,
        email: str,
    ) -> Optional[User]:
        user = await self._con.fetchFirst(
            UserQ.FROM_USERNAME_OR_EMAIL,
            username=username,
            email=email,
        )
        if user:
            return User(**user)

    async def delete(self) -> Any:
        return await super().delete()

    async def update(self) -> Any:
        return await super().update()
