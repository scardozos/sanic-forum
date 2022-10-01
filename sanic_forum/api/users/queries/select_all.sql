SELECT id, username
FROM auth.user
LIMIT $limit
OFFSET $offset;
