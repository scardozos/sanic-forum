from unittest.mock import AsyncMock, patch

from pydantic_factories import ModelFactory
from sanic_forum.api.categories.models.requests import (
    CreateCategoryRequest,
    AllowedCategoryType,
)
from sanic_forum.app import App
from sanic_forum.database.models.category.model import Category
from sanic_forum.enums import ApiVersion, CategoryType


class CategoryFactory(ModelFactory):
    __model__ = Category

def test_list_root_categories(bp_testing_app: App):
    category: Category = CategoryFactory.build()
    get_root = AsyncMock(return_value=[category])

    with patch("sanic_forum.api.categories.v1.SERVICE.get_root", get_root):
        _, resp = bp_testing_app.test_client.get("/api/v1/categories/__root__")

    assert resp.status == 200
    assert resp.json == {"categories": [category.serialize(ApiVersion.V1)]}
    get_root.assert_awaited_once_with()


def test_list_children_categories(bp_testing_app: App):
    parent: Category = CategoryFactory.build()
    child: Category = CategoryFactory.build()

    get_children = AsyncMock(return_value=[child])

    with patch(
        "sanic_forum.api.categories.v1.SERVICE.get_children", get_children
    ):
        _, resp = bp_testing_app.test_client.get(
            f"/api/v1/categories/{parent.id}"
        )

    assert resp.status == 200
    assert resp.json == {"categories": [child.serialize(ApiVersion.V1)]}
    get_children.assert_awaited_once_with(parent.id)


def test_create_category(bp_testing_app: App):
    parent: Category = CategoryFactory.build()
    created: Category = CategoryFactory.build()
    created.name = "New Category"
    created.display_order = 1
    created.type = CategoryType.FORUM_DIVIDER

    create_mock = AsyncMock(return_value=created)

    with patch("sanic_forum.api.categories.v1.SERVICE.create", create_mock):
        _, resp = bp_testing_app.test_client.post(
            f"/api/v1/categories/{parent.id}",
            json=dict(
                name=created.name,
                display_order=created.display_order,
                type=created.type,
            ),
        )

    expected_request = CreateCategoryRequest(
        name=created.name,
        display_order=created.display_order,
        type=AllowedCategoryType(created.type.value),
    )

    assert resp.status == 200
    assert resp.json == {"category": created.serialize(ApiVersion.V1)}
    create_mock.assert_awaited_once_with(expected_request, parent.id)
