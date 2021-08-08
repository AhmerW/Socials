import json
from typing import List


from gateway import ctx
from gateway.data.repos.repos import ChatRepo


async def updateChatMembers(chat_id: int) -> List[int]:
    async with ChatRepo(pool=ctx.chat_pool) as repo:
        members = await repo.getChatMembers(chat_id)

    await ctx.cache_client.con.set(chat_id, json.dumps(members))
    print("updated chat members cache")
    return members
