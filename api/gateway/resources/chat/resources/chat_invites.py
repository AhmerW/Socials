from fastapi import APIRouter
from fastapi.param_functions import Depends
from common.data.ext.event import Event, NewNotice, Notice
from common.data.ext.mq_event import pushEvent
from common.errors import Error, Errors
from common.queries import ChatQ
from common.response import Success
from gateway.core.auth.auth import getUser

from gateway.core.models import SingleUidModel, User
from gateway.core.repo.repos import ChatRepo, NoticeRepo, UserRepo
from gateway.resources.chat.ext import getChatLimitExceededError, isMaxChatAmount


router = APIRouter(prefix='/invite')


@ router.post('/new')
async def chatInvite(
    target: SingleUidModel,
    user: User = Depends(getUser)
):
    invalid_data: Error = Error(Errors.INVALID_DATA, 'Invalid data')

    if user.uid == target.uid:
        raise invalid_data

    async with ChatRepo() as repo:
        async with UserRepo(
                con=repo.con,
                # Important!
                auto_close_con=False) as urepo:
            if not await urepo.exists(target.uid):
                raise invalid_data

        amount = await repo.getChatAmount(user.uid)
        if isMaxChatAmount(amount, user.premium):
            raise getChatLimitExceededError(user.premium)

        async with NoticeRepo(
            con=repo.con,
                auto_close_con=False) as nrepo:
            if await nrepo.existsWhere(user.uid, target.uid):
                raise Error(Errors.EXISTING, 'Invite already sent')

        # Should be last thing to check,
        # since it should already be checked on client-side
        if await repo.getChatFromMembers([user.uid, target.uid]):
            raise Error(Errors.EXISTING, 'Chat already exists')

    await pushEvent(
        Event(
            'chat.invite.new',
            dict(target=target.uid, author=user.uid),
            notice=NewNotice(
                'Chat invite', f'Invite from {user.username}!', True)
        )
    )

    return Success('Invite successfully sent')
