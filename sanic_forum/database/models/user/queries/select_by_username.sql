SELECT id, username
FROM auth.user
WHERE username = $1
LIMIT 1;
