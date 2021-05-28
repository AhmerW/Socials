CREATE TABLE users(
    uid bigserial PRIMARY KEY,
    email text,
    username text,
    password text NOT NULL
);