CREATE TYPE chat.message AS (
    created_at integer,
    message_id integer,
    message_author integer,
    message_content text
);