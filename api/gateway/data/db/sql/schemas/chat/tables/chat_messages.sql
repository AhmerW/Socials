CREATE TABLE chat.chat_messages (
    message_id BIGSERIAL PRIMARY KEY,
    chat_message_created_at bigint default extract(epoch from NOW());,
    chat_message_parent_id integer REFERENCES chat.chat_messages,
    chat_message_chat_id integer REFERENCES chat.chats,
    chat_message_author integer REFERENCES users,
    chat_message_content text
);