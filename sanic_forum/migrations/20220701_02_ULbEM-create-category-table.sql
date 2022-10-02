-- depends: 20220701_01_oieqe-create-forum-schema


CREATE TABLE forum.category (
    id SERIAL,
    parent_category_id INT NULL DEFAULT NULL,
    name CITEXT NULL DEFAULT NULL,
    type SMALLINT NOT NULL,
    display_order SMALLINT NULL DEFAULT NULL,
    CONSTRAINT pk_category PRIMARY KEY (id),
    CONSTRAINT fk_category_parent_category_id FOREIGN KEY (parent_category_id)
        REFERENCES forum.category(id),
    CONSTRAINT uk_category_name UNIQUE (parent_category_id, type, name),
    CONSTRAINT uk_category_display_order
        UNIQUE (parent_category_id, type, display_order)
);


INSERT INTO forum.category (type) VALUES (1);
