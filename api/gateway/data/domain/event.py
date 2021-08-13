from typing import Any


class DomainEventRecord:
    pass


class DomainEvent:
    event: str  # past tense naming
    event_id: int
    timestamp: int
    record: Any
