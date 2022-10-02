SELECT EXISTS (
    SELECT 1
    FROM forum.category
    WHERE parent_category_uuid = $parent_category_uuid
    AND type = $type
    AND name = $name
    LIMIT 1
);
