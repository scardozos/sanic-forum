-- depends: 20220627_02_n96OM-create-auth-schema

CREATE TABLE auth.user (
    uuid UUID DEFAULT uuid_generate_v4(),
    username CITEXT NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY (uuid),
    CONSTRAINT uk_username UNIQUE (username)
);
