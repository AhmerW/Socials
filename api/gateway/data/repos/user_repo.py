from typing import Any, Union

from gateway.data.repos.base import Base


from gateway.data.db.queries.account_q import AccountQ
from gateway.data.db.queries.user_q import UserQ


class UserRepo(Base):
    async def __aenter__(self) -> "UserRepo":
        return await super().__aenter__()

    async def create(
        self,
        username: str,
        password: str,
        email: str,
        verified: bool = False,
    ) -> str:
        return await self._con.execute(
            AccountQ.NEW.format(
                username=username,
                password=password,
                email=email,
                verified=verified,
            ),
        )

    async def get(
        self,
        value: Union[int, str],
    ) -> Any:

        if isinstance(value, int):
            return await self._con.fetchFirst(
                UserQ.PROFILE_FROM_UID,
                uid=value,
            )

        return await self._con.fetchFirst(
            UserQ.PROFILE_FROM_USERNAME,
            username=value,
        )

    async def delete(self) -> Any:
        return await super().delete()

    async def update(self) -> Any:
        return await super().update()
