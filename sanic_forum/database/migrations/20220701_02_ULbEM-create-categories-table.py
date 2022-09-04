"""
Create categories table
"""

from yoyo import step

__depends__ = {'20220701_01_oieqe-create-forum-schema'}

MIGRATE = """
CREATE TABLE forum.categories(
    id UUID DEFAULT uuid_generate_v4(),
    parent_category_id UUID NULL DEFAULT NULL,
    name CITEXT NULL DEFAULT NULL,
    type SMALLINT NOT NULL,
    display_order SMALLINT NULL DEFAULT NULL,
    CONSTRAINT pk_category PRIMARY KEY (id),
    CONSTRAINT fk_category_parent_category_id FOREIGN KEY (parent_category_id)
        REFERENCES forum.categories(id),
    CONSTRAINT uk_category_name UNIQUE (parent_category_id, type, name),
    CONSTRAINT uk_category_display_order
        UNIQUE (parent_category_id, type, display_order)
)
"""

ROLLBACK = """
DROP TABLE forum.categories
"""

steps = [
    step(MIGRATE, ROLLBACK),
    step(
        """INSERT INTO forum.categories (type) VALUES (1)""",
        """
        DELETE FROM forum.categories
        WHERE parent_category_id IS NULL
        AND type = 1
        """,
    ),
]
