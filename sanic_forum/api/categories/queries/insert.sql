INSERT INTO forum.category (parent_category_uuid, name, type, display_order)
VALUES ($parent_category_id, $name, $type, $display_order)
RETURNING *;
