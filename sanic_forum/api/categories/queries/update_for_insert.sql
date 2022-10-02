UPDATE forum.category
SET display_order = display_order + 1
WHERE parent_category_id = $parent_category_id
AND type = $type
AND display_order >= $display_order;
