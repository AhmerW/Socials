class Query():
    """
    Allows use to write queries with $placeholder syntax instead of using $(some number),
    and then passing the keyword argument for that placeholder when calling the class. (__call__ // format())
    The query then gets converted into number-like syntax instead of placeholders, in order to be compatible
    with the postgres engines.
    """

    def __init__(self, query, format_chr='$'):
        self._q = query
        self._fc = format_chr

    @property
    def query(self):
        return self._q

    def __repr__(self):
        return self._q

    def __call__(self, **kwargs):
        return self.format(**kwargs)

    def _getKwargs(self):
        """Extracts each keyword argument from the query"""
        ci = None
        cw = None
        kwargs = list()
        for i, kw in enumerate(self._q):
            if ci is not None and cw is not None:
                if i+1 == len(self._q):
                    # end
                    kwargs.append(self._q[ci:i+1])
                elif not self._q[i].strip() or self._q[i] in (
                    # EOLs
                    ',',
                    ';',
                    ')',
                    '(',
                ):
                    kwargs.append(self._q[ci:i])
                    ci, cw = None, None
            if kw.startswith(self._fc):
                ci, cw = i, kw

        return kwargs

    def format(self, **kwargs):
        """
        **kwargs
                - List of keyword arguments to apply to the query

        returns:
                (str, tuple)
                which represents the query and the values applied to each kwarg.

        """

        kwargs_extracted = self._getKwargs()
        kwargs_no_fc = [kw[1::] for kw in kwargs_extracted]

        kwargs_sorted = sorted(kwargs, key=kwargs_no_fc.index)
        values = [
            kwargs.get(k)
            for k in
            kwargs_sorted
        ]

        query = self._q
        used = list()
        c = 0

        # Replace each keyword argument with an appropiate index number
        for kw in kwargs_extracted:
            kwe = kw[1::]
            if not kwe in used:
                used.append(kwe)
                c += 1
            query = query.replace(kw, f'{self._fc}{c}')

        return (query, *values)


class _QueryCreator(type):
    """Query(attr) when an attribute is referenced"""

    def __getattribute__(self, name) -> Query:
        return Query(
            object.__getattribute__(self, name),
            format_chr='$'
        )


class UserQ(metaclass=_QueryCreator):
    FROM_USERNAME = "SELECT * FROM public.users WHERE username=$username"
    FROM_EMAIL = "SELECT email FROM public.users WHERE email=$email"
    FROM_USERNAME_OR_EMAIL = "SELECT email, username FROM public.users WHERE email = $email OR username = $username"
    EXISTS = "SELECT uid from public.users where uid=$uid"

    VERIFY = "UPDATE users SET verified=TRUE where uid=$uid"

    PROFILE = """
    SELECT * from public.users
    JOIN public.user_profiles 
    ON public.users.uid = public.user_profiles.uid;
    """

    TOTAL_CHATS = """
    SELECT COUNT(*) from chat.chat_members where chat.chat_members.chat_member_uid = $uid
    """


class AccountQ(metaclass=_QueryCreator):

    NEW = """
        WITH ins1 AS
        (
                    insert INTO users
                                (
                                            username,
                                            email,
                                            password,
                                            verified
                                )
                                VALUES
                                (
                                            $username,
                                            $email,
                                            $password,
                                            $verified
                                )
                    returning   * ), ins2 AS
        (
                    INSERT INTO user_profiles
                                (
                                            UID,
                                            display_name
                                )
                                VALUES
                                (
                                (
                                    SELECT UID
                                    FROM   ins1
                                )
                                ,
                                $display_name
                                )
                    returning   * )
        SELECT ins1.username,
            ins1.UID
        FROM   ins1
        join   ins2
        ON     ins1.UID = ins2.UID; 
    """


class ChatQ(metaclass=_QueryCreator):

    # Get all chats of an user, including the chat's members as List<int>
    # Chat's profile picture is the member's profile picture
    # if the amount of members = 1 (2 people conversation, not a group-chat)
    GET_ALL_CHATS = """
        WITH chats AS
        (
            SELECT chat.chat_id,
                    chat.chat_name,
                    chat.chat_pfp
            FROM   chat.chat_members AS members
            join   chat.chats        AS chat
            ON     chat.chat_id = members.chat_id
            WHERE  members.chat_member_uid = $uid ), chat_members AS
        (
                SELECT   chats.chat_id,
                        chats.chat_name,
                        chats.chat_pfp,
                        Array_agg(cm.chat_member_uid) AS members
                FROM     chats
                join     chat.chat_members AS cm
                ON       cm.chat_id = chats.chat_id
                GROUP BY chats.chat_id,
                        chats.chat_name,
                        chats.chat_pfp ), finalize AS
        (
                SELECT   chat.chat_name,
                        chat.members,
                        chat.chat_id,
                        CASE
                                WHEN (
                                                    Cardinality(chat.members) = 1) THEN
                                            (
                                                SELECT pfp
                                                FROM   user_profiles AS up
                                                WHERE  up.UID = chat.members[1] limit 1 )
                                ELSE chat.chat_pfp
                        END          AS chat_pfp
                FROM     chat_members AS chat
                GROUP BY chat.chat_name,
                        chat.chat_pfp,
                        chat.chat_id,
                        chat.members )
        SELECT *
        FROM   finalize; 
    """

    GET_CHAT_FROM_MEMBERS = """
        WITH chats AS
        (
            SELECT chat.chat_id,
                    chat.chat_name,
                    chat.chat_pfp
            FROM   chat.chat_members AS members
            join   chat.chats        AS chat
            ON     chat.chat_id = members.chat_id
            WHERE  members.chat_member_uid = 3 ), chat_members AS
        (
                SELECT   chats.chat_id,
                        chats.chat_name,
                        chats.chat_pfp,
                        Array_agg(cm.chat_member_uid) AS members
                FROM     chats
                join     chat.chat_members AS cm
                ON       cm.chat_id = chats.chat_id
                GROUP BY chats.chat_id,
                        chats.chat_name,
                        chats.chat_pfp ), finalize AS
        (
                SELECT   chat.chat_name,
                        chat.members,
                        chat.chat_id,
                        chat.chat_pfp
                FROM     chat_members AS chat
                GROUP BY chat.chat_name,
                        chat.chat_pfp,
                        chat.chat_id,
                        chat.members )
        SELECT *
        FROM   finalize
        where members = $members;
            """

    GET_MEMBERS = """
        SELECT PROFILE.PFP,
            PROFILE.DISPLAY_NAME,
            USERS.USERNAME,
            USERS.UID,
            CM.CHAT_ID
        FROM CHAT.CHAT_MEMBERS AS CM
        JOIN USERS ON CM.CHAT_MEMBER_UID = USERS.UID
        JOIN USER_PROFILES AS PROFILE ON USERS.UID = PROFILE.UID
        WHERE CM.CHAT_ID = ANY ($chats)
    """

    FETCH_MESSAGES = \
        """
        SELECT
        CM.MESSAGE_ID,
        CM.CHAT_MESSAGE_AUTHOR as author_id,
        CM.CHAT_MESSAGE_CONTENT as content,
        CM.CHAT_MESSAGE_CREATED_AT as created_at,
        REPLIES
        FROM
        CHAT.CHAT_MESSAGES AS CM,
        LATERAL (
            SELECT
            ARRAY (
                SELECT
                ROW(
                    MSG.MESSAGE_ID,
                    MSG.CHAT_MESSAGE_AUTHOR,
                    MSG.CHAT_MESSAGE_CONTENT,
                    MSG.CHAT_MESSAGE_CREATED_AT
                )
                FROM
                CHAT.CHAT_MESSAGES AS MSG
                WHERE
                MSG.CHAT_MESSAGE_PARENT_ID = CM.MESSAGE_ID OFFSET $reply_offset
                LIMIT
                $replies
            ) AS REPLIES
        ) REPLIES
        WHERE CM.CHAT_MESSAGE_CHAT_ID = $chat_id 
        ORDER BY CM.MESSAGE_ID DESC
        OFFSET $offset
        LIMIT $amount;

        """


class MessageQ(metaclass=_QueryCreator):
    INSERT = """
    INSERT into chat.chat_messages(
        chat_message_parent_id,
        chat_message_chat_id,
        chat_message_author,
        chat_message_content
    ) VALUES (
        $parent_id,
        $chat_id,
        $author,
        $content
    )
    RETURNING chat.chat_messages.message_id;
    """

    GET_MESSAGE_REPLIES = """
    """


class NoticeQ(metaclass=_QueryCreator):
    GET_WHERE_AUTHOR_AND_TARGET = \
        """
        SELECT * from notices WHERE notice_author = $author AND notice_target = $target;
        """
    DELETE_WHERE_AUTHOR_AND_TARGET =\
        """
        DELETE FROM notices WHERE notice_author = $author and notice_target = $target;
        """

    INSERT = \
        """
        INSERT INTO 
            notices(
                notice_author,
                notice_target,
                notice_event,
                notice_title,
                notice_body,
                notice_data
            )
            
            VALUES (
                $author,
                $target,
                $event,
                $title,
                $body,
                $data
            )
        """
