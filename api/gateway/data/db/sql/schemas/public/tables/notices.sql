CREATE TABLE IF NOT EXISTS notices (
    notice_id bigserial PRIMARY KEY,
    notice_author integer REFERENCES users,
    notice_target integer REFERENCES users NOT NULL,
    notice_event text,
    notice_title text,
    notice_body text,
    notice_data json
    
);