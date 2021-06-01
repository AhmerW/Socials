CREATE TABLE IF NOT EXISTS users(
    uid bigserial PRIMARY KEY,
    verified boolean default false,
    email text,
    username text,
    password text NOT NULL
);