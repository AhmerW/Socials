

from typing import Dict, List
from asyncpg.connection import Connection

from gateway.core.repo.base import BaseRepo
from gateway.core.models import User


from common.data.local import db
from common.queries import ChatQ, MessageQ, UserQ
from gateway.resources.account.ext.tasks import initVerification
from gateway.resources.chat.models import Chat, ChatCreateModel
from gateway.resources.message.models import Message


class UserRepo(BaseRepo):
    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    async def new(self, con: Connection = None) -> User:
        """Registers a new user"""
        pass

    async def fetchProfile():
        """Fetches an user profile"""
        pass

    async def verify(self):
        """Makes the user verified"""
        return await self.run(
            query=UserQ.VERIFY(uid=self.user.uid),
            op=db.DBOP.Execute
        )

    async def resendVerification(self):
        """Resend verification email"""
        return await initVerification(self.user.email)


class ChatRepo(BaseRepo):

    async def createNew(
        self,
        user: User,
        data: ChatCreateModel
    ):
        pass

    async def fetchAmount(self, user: User):
        return await self.run(
            query=UserQ.TOTAL_CHATS(uid=user.uid),
            op=db.DBOP.FetchFirst
        )

    async def fetchChatsMembers(self, chat_ids: List[int]) -> Dict[int, List[int]]:

        members = await self.run(
            query=ChatQ.GET_MEMBERS(
                chats=chat_ids
            ),
            op=db.DBOP.Fetch
        )

        members_dict = dict.fromkeys(
            chat_ids,
            list()
        )
        for member in members:
            # Don't need the chat_id in the final json applied with each member
            _id = member['chat_id']
            del member['chat_id']
            members_dict[_id].append(member)

        return members_dict

    async def fetchChatMembers(self, chat_id: int) -> List[int]:
        members = await self.fetchChatsMembers([chat_id])
        print("from db: ", members)
        return members.get('chat_id', list())


class MessageRepo(BaseRepo):
    def __init__(self, user: User, *a, **kw):
        super().__init__(*a, **kw)
        self._user = user

    async def insertChatMessage(self, msg: Message):
        await self.run(
            query=MessageQ.INSERT(
                author=self._user.uid,
                parent_id=msg.parent_id,
                channel_id=msg.channel_id,
                content=msg.content
            ),
            op=db.DBOP.Execute
        )
