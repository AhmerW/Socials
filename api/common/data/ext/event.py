from enum import Enum


class Events(Enum):
    Message = 0,
    Chat = 1,
    Friend = 2,
    Notice = 3


def createEvent(event: Events, data: dict,  **kwargs):
    if isinstance(event, Events):
        event = event.name.lower()
    return {
        'data': data,
        'event': event,
        'transfer_data': {
            **kwargs
        }
    }
