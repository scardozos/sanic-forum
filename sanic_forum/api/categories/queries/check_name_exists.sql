SELECT EXISTS (
    SELECT 1
    FROM forum.category
    WHERE type = $type
    AND name = $name
    LIMIT 1
);
