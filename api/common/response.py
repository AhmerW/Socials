from typing import Any, Dict, Union

from fastapi.responses import JSONResponse
from pydantic.main import BaseModel


class ResponseModel(BaseModel):
    """
    The Response-model of all endpoints.
    Returned either as an excpetion (the commons.errors.Error function),
    or as a Successful operation return, (common.responses.Success function)
    """
    status: int
    ok: bool
    detail: str
    error: Dict[str, Union[str, int]]
    data: Dict[str, Any]


class Responses:
    """
    Contains responses which will either be sent directly to the user
    through email, etc, or directly available from the UI side.
    In the future add i18n 

    _F suffix -> Formattable response
    """
    SUCCESS = 'Success'
    ACCOUNT_VERIFIED = 'Your account is verified.'

    REGISTRATION_COMPLTE = 'Your account has succesfully been registered at Socials.'
    REGISTRATION_PENDING = 'Please check your email in order to continue the registration process.'

    OTT_VERIFIED = 'OTToken successfully verified.'
    OTT_GENERATED = 'OTToken Successfully generated.'

    LIMIT_EXCEEDED_STANDARD_F = "Your limit for {0} has exceeded. Please upgrade to premium if you wish to upgrade this amount."
    LIMIT_EXCEEDED_PREMIUM_F = "You have exceeded the limit for {0}."

    LIMIT_EXCEEDED_STANDARD_CHAT = LIMIT_EXCEEDED_STANDARD_F.format(
        'The amount of chats you can have')

    LIMIT_EXCEEDED_PREMIUM_CHAT = LIMIT_EXCEEDED_PREMIUM_F.format(
        'The amount of chats you can have'
    )


def Success(detail, data={}, status=200):
    return JSONResponse(
        status_code=status,
        content={
            'ok': True,
            'status': status,
            'error': {},
            'detail': detail,
            'data': data
        }
    )


class SuccessResponse(JSONResponse):
    def __init__(self, detail, data={}, status=200):
        super().__init__(
            status_code=200,
            content={
                'ok': True,
                'status': status,
                'error': {},
                'detail': detail,
                'data': data
            }
        )
