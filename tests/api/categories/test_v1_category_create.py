import copy
import pytest
from unittest.mock import AsyncMock, patch

from sanic_forum.enums import ApiVersion, CategoryType


VALID_REQUEST_BODY = {
    "name": "abcdefg",
    "display_order": 1,
    "type": CategoryType.FORUM_CATEGORY.value,
}


def test_unknown_parameters_raise_bad_request_error(
    bp_testing_app, forum_root
):
    data = {"invalid_field": "abcdefg"}
    _, resp = bp_testing_app.test_client.post(
        f"/api/v1/categories/{forum_root.uuid}", json=data
    )

    assert resp.status == 400


def test_valid_request_body_succeeds(
    bp_testing_app, executor, forum_divider, forum_root, mayim
):
    executor.select_by_id = AsyncMock(return_value=forum_root)
    executor.check_name_exists = AsyncMock(return_value=False)
    executor.update_for_insert = AsyncMock()
    executor.insert = AsyncMock(return_value=forum_divider)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_root.uuid}", json=VALID_REQUEST_BODY
        )

    assert resp.status == 200


@pytest.mark.parametrize(
    "name,val,expected",
    [
        ("name", "a" * 0, 400),
        ("name", "a" * 1, 200),
        ("name", "a" * 250, 200),
        ("name", "a" * 251, 400),
        ("display_order", -1, 400),
        ("display_order", 0, 400),
        ("display_order", 1, 200),
        ("type", 1, 400),
        ("type", 2, 200),
        ("type", 3, 200),
    ],
)
def test_parameter_validation(
    bp_testing_app,
    executor,
    forum_divider,
    forum_root,
    mayim,
    name,
    val,
    expected,
):
    executor.select_by_id = AsyncMock(return_value=forum_root)
    executor.check_name_exists = AsyncMock(return_value=False)
    executor.update_for_insert = AsyncMock()
    executor.insert = AsyncMock(return_value=forum_divider)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        # Valid request data by default
        data = copy.copy(VALID_REQUEST_BODY)
        data[name] = val

        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_root.uuid}", json=data
        )

    assert resp.status == expected


def test_divider_cannot_be_created_if_not_under_root(
    bp_testing_app,
    executor,
    forum_category,
    forum_divider,
    mayim,
):
    executor.select_by_id = AsyncMock(return_value=forum_category)
    executor.check_name_exists = AsyncMock(return_value=False)
    executor.update_for_insert = AsyncMock()
    executor.insert = AsyncMock(return_value=forum_divider)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        # Valid request data by default
        data = copy.copy(VALID_REQUEST_BODY)
        data["type"] = CategoryType.FORUM_DIVIDER.value

        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_category.uuid}", json=data
        )

    assert resp.status == 400


def test_duplicate_category_name_raises_bad_request(
    bp_testing_app,
    executor,
    forum_root,
    mayim,
):
    executor.select_by_id = AsyncMock(return_value=forum_root)
    executor.check_name_exists = AsyncMock(return_value=True)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_root.uuid}", json=VALID_REQUEST_BODY
        )

    assert resp.status == 400


def test_created_category_is_returned(
    bp_testing_app, executor, forum_divider, forum_root, mayim
):
    executor.select_by_id = AsyncMock(return_value=forum_root)
    executor.check_name_exists = AsyncMock(return_value=False)
    executor.update_for_insert = AsyncMock()
    executor.insert = AsyncMock(return_value=forum_divider)

    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        data = {
            "name": forum_divider.name,
            "display_order": forum_divider.display_order,
            "type": forum_divider.type,
        }

        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{forum_divider.parent_category_uuid}",
            json=data,
        )

    assert resp.status == 200
    assert resp.json == forum_divider.serialize(ApiVersion.V1)
