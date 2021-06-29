CREATE TABLE chat.chat_messages (
    chat_message_id BIGSERIAL PRIMARY KEY,
    chat_message_parent_id integer REFERENCES chat.chat_messages,
    chat_message_channel_id integer REFERENCES chat.chats,
    chat_message_author integer REFERENCES users,
    chat_message_content text
);