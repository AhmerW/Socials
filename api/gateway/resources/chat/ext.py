from common.errors import Error, Errors
from common.response import Responses
from gateway.resources.chat.chat_const import MAX_CHATS_PREMIUM, MAX_CHATS_STANDARD


def getChatLimitExceededError(is_premium):
    return Error(
        Errors.LIMIT_EXCEEDED,
        detail=Responses.LIMIT_EXCEEDED_PREMIUM_CHAT if is_premium else Responses.LIMIT_EXCEEDED_STANDARD_CHAT
    )


def isMaxChatAmount(max_amount: int, is_premium: bool) -> bool:
    return max_amount > (MAX_CHATS_PREMIUM if is_premium else MAX_CHATS_STANDARD)
