SELECT EXISTS (
    SELECT 1
    FROM forum.category
    WHERE parent_category_id = $parent_category_id
    AND type = $type
    AND name = $name
    LIMIT 1
);
