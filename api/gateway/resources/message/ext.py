import json

from common.data.ext.cache_client import CacheClient
from gateway import ctx
from gateway.core.repo.repos import ChatRepo
from gateway.resources.chat.models import Chat


async def getChatMembers(chat_id: int):
    members = await ctx.user_cache.con.get(chat_id)
    if isinstance(members, bytes):
        members = members.decode('utf-8')
    print("got: ", members)
    if not members:
        return members

    if isinstance(members, str):
        try:
            members = json.loads(members)
        except json.JSONDecodeError:
            pass

    async with ChatRepo(pool=ctx.chat_pool) as repo:
        members = await repo.fetchChatMembers(chat_id)

    await ctx.user_cache.con.set(
        chat_id,
        json.dumps(members)
    )
    print("final members: ", members)
    return members
