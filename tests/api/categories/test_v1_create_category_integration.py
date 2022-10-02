from unittest.mock import AsyncMock, patch

from sanic_forum.enums import ApiVersion, CategoryType

CATEGORY_CREATE_BODY = {
    "name": "Test Category",
    "type": CategoryType.FORUM_CATEGORY.value,
    "display_order": 1,
}


@patch("sanic_forum.api.categories.v1.do_validate_create")
@patch("sanic_forum.api.categories.v1.do_create")
def test_create_category(
    do_create,
    do_validate_create,
    bp_testing_app,
    executor,
    mayim,
    forum_root,
    forum_category,
):
    do_validate_create.return_value = None
    do_create.return_value = forum_category
    executor.select_by_id = AsyncMock(return_value=forum_root)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_root.id}", json=CATEGORY_CREATE_BODY
        )

    expected = {"category": forum_category.serialize(ApiVersion.V1)}

    executor.select_by_id.assert_awaited_once_with(forum_root.id)
    do_validate_create.assert_awaited_once()
    do_create.assert_awaited_once()
    assert resp.status == 200
    assert resp.json == expected
