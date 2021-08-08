import json
from typing import Any, Dict, List
import asyncpg
from asyncpg.connection import Connection
from common.data.ext.event import Notice
from common.data.local.queries.query import Query
from gateway import ctx

from gateway.data.repos.base import BaseRepo
from gateway.core.models import User


from common.data.local import db
from common.data.local.queries.chat_q import ChatQ
from common.data.local.queries.notice_q import NoticeQ
from common.data.local.queries.message_q import MessageQ
from common.data.local.queries.user_q import UserQ

from gateway.resources.account.ext.tasks import initVerification
from gateway.resources.chats.models import Chat, ChatCreateModel
from gateway.resources.messages.models import Message


class UserRepo(BaseRepo):
    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    async def new(self, con: Connection = None) -> User:
        """Registers a new user"""
        pass

    async def exists(self, uid: int) -> bool:
        return bool(await self.run(query=UserQ.EXISTS(uid=uid), op=db.DBOP.FetchFirst))

    async def getProfile(self, user_id: int):
        """Fetches an user profile"""
        return await self.run(
            query=UserQ.PROFILE_FROM_UID(uid=user_id), op=db.DBOP.FetchFirst
        )

    async def verify(self):
        """Makes the user verified"""
        return await self.run(query=UserQ.VERIFY(uid=self.user.uid), op=db.DBOP.Execute)

    async def resendVerification(self):
        """Resend verification email"""
        return await initVerification(self.user.email)


class ChatRepo(BaseRepo):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("pool"):
            kwargs["pool"] = ctx.chat_pool

        super().__init__(*args, **kwargs)

    async def createNew(self, user: User, data: ChatCreateModel):
        """
        Create a new chat for user.
        """

    async def getChatAmount(self, uid: int):
        """
        Get the amount of chats a User have.
        """
        result = await self.run(query=UserQ.TOTAL_CHATS(uid=uid), op=db.DBOP.FetchFirst)
        if isinstance(result, asyncpg.Record):
            return result["count"]
        return result

    async def getChats(self, uid: int):
        """
        Get a List of all chat's belonging to a User.
        """
        return await self.run(query=ChatQ.GET_ALL_CHATS(uid=uid), op=db.DBOP.Fetch)

    async def getChatWhereID(self, chat_id: int, uid: int):
        """
        Get a Chat when you know it's ID
        """
        return self.run(
            query=ChatQ.GET_CHAT_WHERE_ID(chat_id=chat_id, uid=uid),
            op=db.DBOP.FetchFirst,
        )

    async def getChatsMembers(self, chat_ids: List[int]) -> Dict[int, List[int]]:
        """
        Get a dictionary mapping a chat id to a list of it's members
        """
        members = await self.run(
            query=ChatQ.GET_CHAT_MEMBERS(chats=chat_ids), op=db.DBOP.Fetch
        )

        members_dict = dict.fromkeys(chat_ids, list())
        for member in members:
            # Don't need the chat_id in the final json applied with each member
            _id = member["chat_id"]
            del member["chat_id"]
            members_dict[_id].append(member)

        return members_dict

    async def getChatMembers(self, chat_id: int) -> List[int]:
        """
        Get a Chat's members
        """
        members = await self.getChatsMembers([chat_id])
        return members.get(chat_id, list())

    async def getChatMemberFromUID(self, uid: int, chat_id: int):
        """
        Returns the user from chat.chat_members.
        Useful for checking if the user is a participant of the chat
        """
        return await self.run(
            query=ChatQ.FROM_CHAT_MEMBERS_WHERE_UID(uid=uid, chat_id=chat_id),
            op=db.DBOP.FetchFirst,
        )

    async def getChatFromMembers(self, members: List[int]):
        """
        Get a chat where you know who the members are
        """
        return await self.run(
            query=ChatQ.GET_CHAT_FROM_MEMBERS(members=sorted(members)),
            op=db.DBOP.FetchFirst,
        )

    async def getChatMessages(
        self, chat_id: int, offset: int, amount: int, order: str = "DESC"  # asc
    ) -> List[Dict[str, Any]]:
        """
        Get a List of chat's messages
        """
        query = ChatQ.GET_CHAT_MESSAGES.query.format(
            order=order, chat_id="{chat_id}", offset="{offset}", amount="{amount}"
        )
        return await self.run(
            query=Query(query).format(
                chat_id=chat_id,
                offset=offset,
                amount=amount,
            ),
            op=db.DBOP.Fetch,
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
                content=msg.content,
            ),
            op=db.DBOP.FetchFirst,
        )


class NoticeRepo(BaseRepo):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    async def getWhere(self, author: int, target: int):
        return await self.run(
            query=NoticeQ.GET_WHERE_AUTHOR_AND_TARGET(author=author, target=target),
            op=db.DBOP.Fetch,
        )

    async def getWhereTarget(self, target: int, offset: int, limit: int):
        return await self.run(
            query=NoticeQ.GET_WHERE_TARGET(target=target, offset=offset, limit=limit),
            op=db.DBOP.Fetch,
        )

    async def existsWhere(self, author: int, target: int):
        return bool(await self.getWhere(author, target))

    async def deleteWhere(self, author: int, target: int):
        return await self.run(
            NoticeQ.DELETE_WHERE_AUTHOR_AND_TARGET(author=author, target=target),
            op=db.DBOP.FetchFirst,
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
                title=notice.options.get("title"),
                body=notice.options.get("body"),
                data=json.dumps(notice.data) if notice.data else None,
            ),
            op=db.DBOP.Execute,
        )
