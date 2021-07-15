from typing import Dict, Any, Optional

from common.utils import SYSTEM_UID


class NewNotice:
    __slots__ = 'title', 'body', 'save', 'include_data', 'options'

    def __init__(
            self,
            title: str = None,
            body: str = None,
            save: bool = False,
            include_data: bool = False, **opts) -> None:
        self.title, self.body, self.save = title, body, save
        self.include_data = include_data
        self.options = opts


class Notice:
    __slots__ = (
        'event',
        'data',
        'title',
        'body',
        'has_content',
        'save',
        'author',
        'target',
        'options'
    )
    event: str
    title: str
    body: str
    author: int
    target: int
    has_content: bool
    save: bool
    data: Optional[Dict[str, Any]]
    options: Optional[Dict[str, Any]]

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class Event:
    def __init__(
        self,
        event: str,
        data: Dict[str, Any] = dict(),
        author: int = SYSTEM_UID,
        target: int = None,
        notice: NewNotice = None,
        **opts
    ) -> None:
        self.event, self.data = event, data
        self.author = author
        self.notice = notice
        self.target = target or author
        self.transfer_data = {'target': self.target, **opts}

    def hasNotice(self) -> bool: return self.notice is not None

    def getData(self) -> Dict[str, Any]:
        return dict(
            event=self.event,
            data=self.data,
            transfer_data=self.transfer_data
        )

    def getNotice(self) -> Optional[Notice]:
        if self.notice is None:
            return None
        notice = Notice(
            event=self.event,
            title=self.notice.title,
            body=self.notice.body,
            has_content=self.notice.title and self.notice.body,
            save=self.notice.save,
            author=self.author,
            target=self.target,
            options=self.notice.options
        )
        if self.notice.include_data:
            notice.data = self.data
        return notice
