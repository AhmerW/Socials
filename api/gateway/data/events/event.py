from typing import Dict, Any, Optional

from common.settings.settings import SYSTEM_SETTINGS


class NewNotice:
    __slots__ = "title", "body", "save", "include_data", "options"

    def __init__(
        self,
        title: str = None,
        body: str = None,
        save: bool = False,
        include_data: bool = False,
        **opts
    ) -> None:
        self.title, self.body, self.save = title, body, save
        self.include_data = include_data
        self.options = opts


class Notice:
    __slots__ = ("event", "data", "has_content", "save", "author", "target", "options")
    event: str
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
        author: int = SYSTEM_SETTINGS.UID,
        target: int = None,
        notice: NewNotice = None,
        **opts
    ) -> None:
        self.event, self.data = event, data
        self.author = author
        self.notice = notice
        self.target = target or author
        self.transfer_data = {"target": self.target, **opts}

    def hasNotice(self) -> bool:
        return self.notice is not None

    def _getNoticeOptions(self) -> Dict[str, Any]:
        return dict(
            title=self.notice.title, body=self.notice.body, **self.notice.options
        )

    def getData(self) -> Dict[str, Any]:
        """
        Creates a dictionary which consists of:
            event, str:
                The event-type, example 'chat.message.new', 'friend.request.new'.
            data, Optional[Dict[str, Any]]:
                Contains event data. For a 'chat.message.new' event, this would be the
                message body, but for a friend.request.new, this doesnt necessarily
                have to be anything, it can be None.
                This is also available to the end user.
            transfer_data. Dict[str, Any]:
                Required dictionary which contains information such as the target of this event.
                This target (integer) is necessary for the dispatch service, so it knows
                where to send the event to. Not available to the end user, this key
                will be deleted before dispatching.

        """
        event = dict(event=self.event, data=self.data, transfer_data=self.transfer_data)
        if self.hasNotice():
            event["notice"] = self._getNoticeOptions()

        return event

    def getNotice(self) -> Optional[Notice]:
        """
        Creates a Notice instance with all the attributes found in Notice.__slots__
        Not all attribtes of this instance is  meant for the client (the end user),
        if anything, only Notice.options, in order to render UI.
        The instance is used internally to store the notification object in the database,
        or to send user a push notification.
        """
        # self.notice : NewNotice
        if self.notice is None:
            return None

        notice = Notice(
            event=self.event,
            has_content=self.notice.title and self.notice.body,
            save=self.notice.save,
            author=self.author,
            target=self.target,
            data=self.data,
            options=self._getNoticeOptions(),
        )
        # Wether to include data in the notice,
        # if true this data will also be stored in the databse
        # if Notice.save is true
        if self.notice.include_data:
            notice.data = self.data

        return notice
