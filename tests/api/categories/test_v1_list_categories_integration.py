from unittest.mock import AsyncMock, patch

from sanic_forum.enums import ApiVersion


def test_categories_can_be_listed(
    bp_testing_app, forum_root, forum_divider, forum_category
):
    all_categories = [forum_root, forum_divider, forum_category]
    do_get_all = AsyncMock(return_value=all_categories)

    with patch("sanic_forum.api.categories.v1.do_get_all", do_get_all):
        _, resp = bp_testing_app.test_client.get("/api/v1/categories")

    expected = {
        "categories": [cat.serialize(ApiVersion.V1) for cat in all_categories]
    }

    do_get_all.assert_called_once_with()
    assert resp.status == 200
    assert resp.json == expected
