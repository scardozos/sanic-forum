-- depends: 20220701_01_oieqe-create-forum-schema


CREATE TABLE forum.category (
    id SERIAL,
    parent_category_id INT NULL DEFAULT NULL,
    name CITEXT NULL DEFAULT NULL,
    type SMALLINT NOT NULL,
    display_order SMALLINT NULL DEFAULT NULL,
    CONSTRAINT category_pk PRIMARY KEY (id),
    CONSTRAINT category_parent_category_id_fk FOREIGN KEY (parent_category_id)
        REFERENCES forum.category (id)
);

CREATE UNIQUE INDEX category_display_order_uk ON forum.category (parent_category_id, display_order ASC);
CREATE INDEX category_type_ix ON forum.category (type) WHERE type = 1; -- Used to get root categories, no need to index all

INSERT INTO forum.category (type) VALUES (1);
