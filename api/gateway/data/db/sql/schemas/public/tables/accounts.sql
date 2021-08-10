CREATE TABLE accounts (
    account_id bigserial PRIMARY KEY
    account_password text
    account_has_2fa boolean default false
);