SELECT * FROM forum.category
WHERE parent_category_id = $1
ORDER BY display_order ASC;
