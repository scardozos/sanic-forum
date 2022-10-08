-- depends: 20220627_02_n96OM-create-auth-schema

CREATE TABLE auth.user (
    id SERIAL,
    username CITEXT NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (id),
    CONSTRAINT username_uk UNIQUE (username)
);
