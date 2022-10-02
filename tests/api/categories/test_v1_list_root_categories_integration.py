from unittest.mock import AsyncMock, patch

from sanic_forum.enums import ApiVersion


def test_root_categories_can_be_listed(bp_testing_app, forum_root):
    root_categories = [forum_root]
    do_get_root = AsyncMock(return_value=root_categories)

    with patch("sanic_forum.api.categories.v1.do_get_root", do_get_root):
        _, resp = bp_testing_app.test_client.get("/api/v1/categories/__root__")

    expected = {
        "categories": [cat.serialize(ApiVersion.V1) for cat in root_categories]
    }

    do_get_root.assert_called_once_with()
    assert resp.status == 200
    assert resp.json == expected
