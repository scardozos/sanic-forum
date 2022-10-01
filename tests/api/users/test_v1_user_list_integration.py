from unittest.mock import patch

from sanic_forum.enums import ApiVersion


def test_users_can_be_listed(bp_testing_app, mayim, user_executor):
    with patch("sanic_forum.api.users.v1.Mayim", mayim):
        _, resp = bp_testing_app.test_client.get("/api/v1/users")

    user_dicts = [
        user.serialize(ApiVersion.V1)
        for user in user_executor.select_all.return_value
    ]
    assert resp.json == user_dicts
