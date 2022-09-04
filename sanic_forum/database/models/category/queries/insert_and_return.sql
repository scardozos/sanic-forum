INSERT INTO forum.categories (parent_category_id, name, type, display_order)
VALUES ($parent_category_id, $name, $type, $display_order)
RETURNING id, parent_category_id, name, type, display_order;
