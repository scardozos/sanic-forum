INSERT INTO auth.user (username)
VALUES ($1)
RETURNING id, username;
