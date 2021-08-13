from typing import Any, Dict, Type, Union
from datetime import datetime
from gateway.data.clients.mq.mq_client import MQManager, MQManagerType

from gateway.data.events.types import system_events
from gateway.data.clients.mq import Producers


class EventRecord:
    __slots__ = ("_event", "_timestamp", "_data")

    def __init__(
        self,
        event: str,
        data: Dict[Any, Any] = dict(),
    ) -> None:
        if not event in system_events:
            raise TypeError("Invalid event '%s'" % event)

        self._event = event
        self._timestamp = int(datetime.now().timestamp())
        self._data = data

    def __sub__(self, other: "EventRecord") -> int:
        return self._timestamp - other.timestamp

    @property
    def event(self) -> str:
        return self._event

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def toJson(self) -> Dict[Any, Any]:
        return dict(
            event=self._event,
            timstamp=self._timestamp,
            data=self._data,
        )


class SystemEvent:
    def __init__(
        self,
        record: Union[EventRecord, str],
        **data,
    ) -> None:
        if isinstance(record, EventRecord):
            self._record = record
        else:
            self._record = EventRecord(record, data=data)

    @property
    def record(self) -> EventRecord:
        return self._record

    async def dispatch(
        self,
        broker=None,
        broker_topic="ws.event.new",
    ) -> None:
        broker = broker or Producers.PRODUCER

        if isinstance(broker, MQManager) and broker.type_ == MQManagerType.Producer:
            await broker.send(
                broker_topic,
                self._record.toJson(),
            )


# the event bus should not deal with the notice
# its up for the creator of the event to process the Notice (processNotice)


class SystemNotice:
    def __init__(self, event: SystemEvent) -> None:
        self.event = event
