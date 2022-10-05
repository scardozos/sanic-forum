SELECT uuid, username
FROM auth.user
LIMIT $limit
OFFSET $offset;
