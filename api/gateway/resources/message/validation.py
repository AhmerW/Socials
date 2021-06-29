from gateway.resources.message.models import Message
from gateway.resources.chat.chat_const import MAX_CHAT_MESSAGE_LEN


def validateChatMessage(msg: Message) -> bool:

    if len(msg.content) > MAX_CHAT_MESSAGE_LEN:
        return False

    if len(msg.assets) > MAX_CHAT_MESSAGE_LEN:
        return False

    return True
