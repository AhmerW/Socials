from typing import List, Union
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig


class EmailService(object):

    def __init__(self, config: ConnectionConfig, incl_name: str = None):
        self._user_store = dict()
        self._config = config
        self._incl_name = incl_name

    def _prepareMessage(
        self,
        subject: str,
        target: Union[List[str], str],
        body: str
    ) -> MessageSchema:

        incl_name = self._incl_name
        if incl_name is not None and not subject.startswith(incl_name):
            subject = f'{incl_name} - {subject}'

        if not target:
            return None

        if isinstance(target, str):
            target = [target]

        return MessageSchema(
            subject=subject,
            recipients=target,
            body=body,
            subtype='html'
        )

    async def sendMail(
        self,
        subject: str,
        target: Union[List[str], str],
        body: str
    ) -> bool:
        message: MessageSchema = self._prepareMessage(subject, target, body)
        if message is None:
            return False
        fm = FastMail(self._config)
        await fm.send_message(message)
        return True
