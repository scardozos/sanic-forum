SELECT id, parent_category_id, name, type, display_order
FROM forum.categories
WHERE id = $id
LIMIT 1;
