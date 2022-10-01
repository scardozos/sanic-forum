from unittest.mock import AsyncMock, patch

from sanic_forum.enums import ApiVersion


def test_users_can_be_listed(
    bp_testing_app, mayim, executor, forum_root, forum_divider, forum_category
):
    executor.select_all = AsyncMock(
        return_value=[forum_root, forum_divider, forum_category]
    )

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        _, resp = bp_testing_app.test_client.get("/api/v1/categories")

    category_dicts = [
        category.serialize(ApiVersion.V1)
        for category in executor.select_all.return_value
    ]

    assert resp.json == category_dicts
