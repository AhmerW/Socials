

import json
from typing import Any, Dict, List
import asyncpg
from asyncpg.connection import Connection
from common.data.ext.event import Notice
from gateway import ctx

from gateway.core.repo.base import BaseRepo
from gateway.core.models import User


from common.data.local import db
from common.queries import ChatQ, MessageQ, NoticeQ, UserQ
from gateway.resources.account.ext.tasks import initVerification
from gateway.resources.chat.models import Chat, ChatCreateModel
from gateway.resources.message.models import Message


class UserRepo(BaseRepo):
    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    async def new(self, con: Connection = None) -> User:
        """Registers a new user"""
        pass

    async def exists(self, uid: int) -> bool:
        return bool(
            await self.run(query=UserQ.EXISTS(uid=uid), op=db.DBOP.FetchFirst)
        )

    async def getProfile():
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
    def __init__(self, *args, **kwargs):
        if not kwargs.get('pool'):
            kwargs['pool'] = ctx.chat_pool

        super().__init__(*args, **kwargs)

    async def createNew(
        self,
        user: User,
        data: ChatCreateModel
    ):
        pass

    async def getChatAmount(self, uid: int):
        result = await self.run(
            query=UserQ.TOTAL_CHATS(uid=uid),
            op=db.DBOP.FetchFirst
        )
        if isinstance(result, asyncpg.Record):
            return result['count']
        return result

    async def getChats(self, uid):
        return await self.run(
            query=ChatQ.GET_ALL_CHATS(
                uid=uid
            ),
            op=db.DBOP.Fetch
        )

    async def getChatsMembers(self, chat_ids: List[int]) -> Dict[int, List[int]]:

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

    async def getChatMembers(self, chat_id: int) -> List[int]:
        members = await self.getChatsMembers([chat_id])
        return members.get(chat_id, list())

    async def getChatFromMembers(self, members: List[int]):
        return await self.run(
            query=ChatQ.GET_CHAT_FROM_MEMBERS(members=sorted(members)),
            op=db.DBOP.FetchFirst
        )

    async def getChatMessages(
        self,
        chat_id: int,
        offset: int,
        amount: int,
        reply_offset: int,
        replies: int
    ) -> List[Dict[str, Any]]:
        return await self.run(
            query=ChatQ.FETCH_MESSAGES(
                chat_id=chat_id,
                offset=offset,
                amount=amount,
                reply_offset=reply_offset,
                replies=replies
            ),
            op=db.DBOP.Fetch
        )


class MessageRepo(BaseRepo):
    def __init__(self, user: User, *a, **kw):
        super().__init__(*a, **kw)
        self._user = user

    async def insertChatMessage(self, msg: Message):
        return await self.run(
            query=MessageQ.INSERT(
                author=self._user.uid,
                parent_id=msg.parent_id,
                chat_id=msg.chat_id,
                content=msg.content
            ),
            op=db.DBOP.FetchFirst
        )


class NoticeRepo(BaseRepo):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    async def getWhere(self, author: int, target: int):
        return await self.run(
            query=NoticeQ.GET_WHERE_AUTHOR_AND_TARGET(
                author=author, target=target),
            op=db.DBOP.Fetch
        )

    async def existsWhere(self, author: int, target: int):
        return bool(await self.getWhere(author, target))

    async def deleteWhere(self, author: int, target: int):
        return await self.run(
            NoticeQ.DELETE_WHERE_AUTHOR_AND_TARGET(
                author=author, target=target),
            op=db.DBOP.FetchFirst
        )

    async def existsNotice(self, notice_id: int):
        pass

    async def insertNotice(self, notice: Notice):
        print("notice inserted")
        return await self.run(
            NoticeQ.INSERT(
                author=notice.author,
                target=notice.target,
                event=notice.event,
                title=notice.options.get('title'),
                body=notice.options.get('body'),
                data=json.dumps(notice.data) if notice.data else None
            ),
            op=db.DBOP.Execute
        )
