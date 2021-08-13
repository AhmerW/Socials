from enum import Enum, auto
from typing import Optional, Union
from functools import partial

from starlette.responses import Response
from common.errors import Error, Errors
from common.response import Responses, Success

from gateway.core.models import User
from gateway.data.repos.base import Base, BaseService, BaseValidator
from gateway.data.repos.user_repo import UserRepo
from gateway.resources.account.models import UserNewModel
from gateway.resources.users.const import MAX_USERNAME_LEN, MIN_USERNAME_LEN


# stateless validator class
class UserServiceValidator(BaseValidator):
    def validUsername(username: str) -> bool:
        return all(
            [
                username.strip(),
                len(username) < MAX_USERNAME_LEN,
                len(username) > MIN_USERNAME_LEN,
            ]
        )

    def validateUsername(username: str) -> Optional[str]:
        long = len(username) < MAX_USERNAME_LEN
        short = len(username) > MIN_USERNAME_LEN - 1
        if not all(
            [
                username.strip(),
                long,
                short,
            ]
        ):
            text = "shorter" if long else "longer"
            return "Username can't be {text} than {chars} characters.".format(
                text=text,
                chars=MIN_USERNAME_LEN if long else MAX_USERNAME_LEN,
            )


class UserRegistrationResults(Enum):
    EXISTING_EMAIL = 0
    COMPLETE = 1


# Aggregate Root's service
class UserService(BaseService):
    validator = UserServiceValidator
    chats_services = None

    async def __aenter__(self, pool=None) -> "UserService":
        self._repo: UserRepo = await UserRepo.new(
            pool=pool,
        )
        return self

    async def getUser(
        self,
        value: Union[str, int],
    ) -> Optional[User]:
        return await self._repo.get(value)

    async def createNewUser(
        self,
    ):
        await self._repo.create()

    async def validNewUser(
        self,
        user: UserNewModel,
    ) -> bool:
        """
        Validates a new registration attempt
        returns a boolean
        """
        if not all(
            f()
            for f in [
                partial(UserService.validator.validUsername, user.username),
                (
                    (lambda: True)
                    if user.email is None
                    else partial(UserService.validator.validEmail, user.email)
                ),
            ]
        ):
            return False
        if user.email is None:
            return (await self.getUser(user.username)) is None

        return (
            await self._repo.getFromUsernameOrEmail(
                username=user.username, email=user.email
            )
        ) is None

    async def validateNewUser(self, user: UserNewModel):
        """Validates a new registration attempt with errors on fail"""
        username_err = UserService.validator.validateUsername(user.username)
        if isinstance(username_err, str):
            raise Error(
                Errors.USER_INVALID_USERNAME,
                detail=username_err,
            )

        if user.email is not None:
            email_err = UserService.validator.validEmail(user.email)
            if email_err:
                raise Error(
                    Errors.INVALID_EMAIL,
                    detail=str(email_err),
                )

            existing = await self._repo.getFromUsernameOrEmail(
                username=user.username,
                email=user.email,
            )

        else:
            existing = await self._repo.get(user.username)

        if existing:
            if user.username == existing.username:
                raise Error(
                    Errors.USER_INVALID_USERNAME,
                    detail="Username already exists",
                )

            if user.email is not None and user.email == existing.email:
                return UserRegistrationResults.EXISTING_EMAIL

        return UserRegistrationResults.COMPLETE

    # Chat

    async def getUsersChats(self, user: User):
        pass
