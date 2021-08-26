CREATE TABLE IF NOT EXISTS users(
    uid bigserial PRIMARY KEY,
    verified boolean default False,
    premium boolean default False,
    email text,
    username text,
    password text NOT NULL
);