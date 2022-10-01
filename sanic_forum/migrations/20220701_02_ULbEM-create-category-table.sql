-- depends: 20220701_01_oieqe-create-forum-schema


CREATE TABLE forum.category (
    uuid UUID DEFAULT uuid_generate_v4(),
    parent_category_uuid UUID NULL DEFAULT NULL,
    name CITEXT NULL DEFAULT NULL,
    type SMALLINT NOT NULL,
    display_order SMALLINT NULL DEFAULT NULL,
    CONSTRAINT pk_category PRIMARY KEY (uuid),
    CONSTRAINT fk_category_parent_category_uuid FOREIGN KEY (parent_category_uuid)
        REFERENCES forum.category(uuid),
    CONSTRAINT uk_category_name UNIQUE (parent_category_uuid, type, name),
    CONSTRAINT uk_category_display_order
        UNIQUE (parent_category_uuid, type, display_order)
);


INSERT INTO forum.category (type) VALUES (1);
