from common.data.local.queries.query import QueryCreator


class ChatQ(metaclass=QueryCreator):

    # Get all chats of an user, including the chat's members as List<int>
    # Chat's profile picture is the member's profile picture
    # if the amount of members = 1 (2 people conversation, not a group-chat)
    DEFAULT_GET_CHATS = """
        WITH chats AS
        (
            SELECT chat.chat_id,
                    chat.chat_name,
                    chat.chat_pfp
            FROM   chat.chat_members AS members
            join   chat.chats        AS chat
            ON     chat.chat_id = members.chat_id
            WHERE {optional_where} members.chat_member_uid = {uid} ), chat_members AS
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
    GET_ALL_CHATS = DEFAULT_GET_CHATS.format(optional_where='', uid='{uid}')
    GET_CHAT_WHERE_ID = DEFAULT_GET_CHATS.format(
        optional_where='chat.chat_id = {chat_id} AND',
        uid='{uid}')

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
        where members = {members};
            """

    GET_CHAT_MEMBERS = """
        SELECT PROFILE.PFP,
            PROFILE.DISPLAY_NAME,
            USERS.USERNAME,
            USERS.UID,
            CM.CHAT_ID
        FROM CHAT.CHAT_MEMBERS AS CM
        JOIN USERS ON CM.CHAT_MEMBER_UID = USERS.UID
        JOIN USER_PROFILES AS PROFILE ON USERS.UID = PROFILE.UID
        WHERE CM.CHAT_ID = ANY ({chats})
    """

    FROM_CHAT_MEMBERS_WHERE_UID = \
        """
        SELECT * from chat.chat_members as cm where cm.chat_member_uid = {uid} and cm.chat_id = {chat_id};
        """

    __OLD__GET_MESSAGES = \
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
                MSG.CHAT_MESSAGE_PARENT_ID = CM.MESSAGE_ID OFFSET {reply_offset}
                LIMIT
                {replies}
            ) AS REPLIES
        ) REPLIES
        WHERE CM.CHAT_MESSAGE_CHAT_ID = {chat_id}
        ORDER BY CM.MESSAGE_ID DESC
        OFFSET {offset}
        LIMIT {amount};

        """

    GET_CHAT_MESSAGES = \
        """
        SELECT 
        CM.MESSAGE_ID, 
        CM.CHAT_MESSAGE_AUTHOR AS AUTHOR_ID, 
        CM.CHAT_MESSAGE_CONTENT AS CONTENT,
        CM.CHAT_MESSAGE_PARENT_ID,
        CM.CHAT_MESSAGE_CREATED_AT AS CREATED_AT, 
        CASE WHEN CM.CHAT_MESSAGE_PARENT_ID IS NOT NULL THEN (
            SELECT 
            json_build_object(
                'parent_id', CM.CHAT_MESSAGE_PARENT_ID,
                'message_id', MSG.MESSAGE_ID, 
                'author_id', MSG.CHAT_MESSAGE_AUTHOR, 
                'author_pfp', up.pfp, 
                'content', MSG.CHAT_MESSAGE_CONTENT,
                'created_at', MSG.CHAT_MESSAGE_CREATED_AT
            )
            FROM 
            CHAT.CHAT_MESSAGES AS MSG 
            JOIN USER_profiles as up on up.uid = MSG.CHAT_MESSAGE_AUTHOR
            WHERE MSG.MESSAGE_ID = CM.CHAT_MESSAGE_PARENT_ID
            LIMIT 1


        ) ELSE row_to_json(ROW()) END REPLY_TO 
        FROM 
        CHAT.CHAT_MESSAGES AS CM 
        WHERE 
        CM.CHAT_MESSAGE_CHAT_ID = {chat_id}
        ORDER BY 
        CM.MESSAGE_ID {order} OFFSET {offset}
        LIMIT 
        {amount};

        """
