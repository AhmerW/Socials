CREATE TABLE IF NOT EXISTS user_profiles (
    uid integer REFERENCES users,
    display_name text,
    first_name text,
    last_name text
);