from typing import List, Optional, Union

from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

from common.data.ext.config import DEFAULT_CONF


class EmailService(object):
    INCL_NAME = 'Socials'
    INCL_NAME_PREFIX = True
    INCL_APPLY_AUTO = True
    
    def __init__(self, conf : ConnectionConfig = DEFAULT_CONF):
        self._user_store = dict()
    
    def __prepareMessage(
        self,
        subject: str,
        target: Union[List[str], str],
        body: str
        ) -> MessageSchema:
        
        cls = self.__class__
        if cls.INCL_NAME_PREFIX and not subject.startswith(cls.INCL_NAME):
            if not cls.INCL_APPLY_AUTO:
                return None
            subject = f'{cls.INCL_NAME} - {suject}'
            
        if not target:
            return None

        if isinstance(target, str):
            target = [target]
        
        return MessageSchema(
            subject = subject,
            recipients = target,
            body = html,
            subtype = 'html'
        )
    
    async def sendMail(self, *args, **kwargs) -> bool:
        message = self.__prepareMessage(*args, **kwargs)
        if message is None:
            return False
        fm = FastMail(REGISTER_CONF)
        await fm.send_message(message)
        return True