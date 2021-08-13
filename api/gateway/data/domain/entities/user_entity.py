import asyncio
from typing import Optional

from pydantic import EmailStr

from gateway.data.db.queries.query import Query
from gateway.data.domain.objects import (
    Entity,
    EntityModel,
    ValueObject,
    ValueObjectModel,
)


from gateway.data.db.pools import Pools


from gateway.data.events import event
from gateway.data.events.bus import eventBus
from gateway.data.events.events import SystemEvent


class UserEntityModel(EntityModel):
    username: str
    display_name: str
    email: Optional[EmailStr]

    verified: Optional[bool] = False
    premium: Optional[bool] = False


@eventBus.listen("db.init.done")
async def init(event: SystemEvent):
    pass
