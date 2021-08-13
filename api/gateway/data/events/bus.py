from typing import Callable, Dict, List

import asyncio


from gateway.data.events.events import SystemEvent


class EventBus:
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable]] = dict()

    def _create(self, event: str) -> None:
        """Adds event if not already added"""
        if not self._listeners.get(event):
            self._listeners[event] = list()

    def emit(self, event: SystemEvent):
        for ev in self._listeners.get(event.record.event, list()):
            asyncio.create_task(ev(event))

    def add(self, event: str, listener: Callable) -> None:
        self._create(event)
        self._listeners[event].append(listener)

    def listen(self, event: str):
        def decorator(func: Callable):
            self.add(event, func)

        return decorator


eventBus = EventBus()
