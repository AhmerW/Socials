CREATE TABLE IF NOT EXISTS user_profiles (
    uid integer REFERENCES users,
    pfp text,
    display_name text,
    first_name text,
    last_name text
);