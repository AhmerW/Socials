from gateway.data.db.queries import Query, QueryCreator


class MessageQ(metaclass=QueryCreator):
    INSERT = """
    INSERT into chat.chat_messages(
        chat_message_parent_id,
        chat_message_chat_id,
        chat_message_author,
        chat_message_content
    ) VALUES (
        {parent_id},
        {chat_id},
        {author},
        {content}
    )
    RETURNING chat.chat_messages.message_id;
    """
