UPDATE forum.category
SET display_order = display_order + 1
WHERE parent_category_uuid = $parent_category_uuid
AND type = $type
AND display_order >= $display_order;
