from fastapi import APIRouter
from fastapi.param_functions import Depends
from common.data.ext.event import Event, NewNotice, Notice
from common.data.ext.mq_event import pushEvent
from common.errors import Error, Errors
from common.queries import ChatQ
from common.response import Responses, Success
from gateway.core.auth.auth import getUser

from gateway.core.models import SingleUidModel, User
from gateway.core.repo.repos import ChatRepo, NoticeRepo, UserRepo
from gateway.resources.chats.ext import getChatLimitExceededError, isMaxChatAmount


router = APIRouter(prefix='/invites')


@ router.post('/')
async def chatInviteNew(
    uid: int,
    user: User = Depends(getUser)
):
    target = uid
    invalid_data: Error = Error(Errors.INVALID_DATA, 'Invalid data')

    if user.uid == target:
        raise invalid_data

    async with ChatRepo() as repo:
        async with UserRepo(
                con=repo.con,
                # Important!
                auto_close_con=False) as urepo:
            if not await urepo.exists(target):
                raise invalid_data

        amount = await repo.getChatAmount(user.uid)
        if isMaxChatAmount(amount, user.premium):
            raise getChatLimitExceededError(user.premium)

        async with NoticeRepo(
            con=repo.con,
                auto_close_con=False) as nrepo:
            if await nrepo.existsWhere(user.uid, target):
                raise Error(Errors.EXISTING, 'Invite already sent')

        # Should be last thing to check,
        # since it should already be checked on client-side
        if await repo.getChatFromMembers([user.uid, target]):
            raise Error(Errors.EXISTING, 'Chat already exists')

    await pushEvent(
        Event(
            'chat.invite.new',
            target=target,
            author=user.uid,
            notice=NewNotice(
                'Chat invite', f'Invite from {user.username}!', True)
        )
    )

    return Success('Invite successfully sent')


@ router.delete('/')
async def chatInviteDelete(
    uid: int,
    user: User = Depends(getUser)
):
    target = uid
    async with NoticeRepo() as repo:
        if not await repo.deleteWhere(user.uid, target):
            return Success('If there was an invite, it has been deleted')

    raise Error(Errors.INTERNAL)
