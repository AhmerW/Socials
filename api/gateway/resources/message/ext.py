import json

from common.data.ext.cache_client import CacheClient
from gateway import ctx
from gateway.core.repo.repos import ChatRepo
from gateway.resources.chat import chat_cache

from gateway.resources.chat.models import Chat


async def getChatMembers(chat_id: int):
    members = await ctx.cache_client.con.get(chat_id, encoding='utf-8')
    if isinstance(members, str):
        if members:
            try:
                members = json.loads(members)
                return members
            except json.JSONDecodeError:
                pass

    print("setting chat members cache.")
    return await chat_cache.updateChatMembers(chat_id)
