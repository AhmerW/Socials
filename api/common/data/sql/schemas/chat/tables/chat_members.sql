CREATE TABLE chat.chat_members (
    chat_id integer REFERENCES chat.chats,
    chat_member_uid integer REFERENCES users
);