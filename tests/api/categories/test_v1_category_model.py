import pytest

from sanic_forum.api.categories.model import Category
from sanic_forum.enums import ApiVersion


@pytest.mark.parametrize(
    "id,parent_category_id,name,type,display_order",
    [
        (1, None, "Root divider", 1, 0),
        (2, None, "Root forum", 2, 1),
        (3, 2, "Child forum", 2, 0),
    ],
)
def test_category_properties(
    id, parent_category_id, name, type, display_order
):
    category = Category(
        id=id,
        parent_category_id=parent_category_id,
        name=name,
        type=type,
        display_order=display_order,
    )
    assert category.id == id
    assert category.parent_category_id == parent_category_id
    assert category.name == name
    assert category.type == type
    assert category.display_order == display_order


@pytest.mark.parametrize(
    "category",
    [
        "forum_root",
        "forum_divider",
        "forum_category",
    ],
)
def test_category_serialization(category, request):
    category_: Category = request.getfixturevalue(category)

    assert category_.serialize(ApiVersion.V1) == {
        "id": category_.id,
        "parent_category_id": (
            category_.parent_category_id
            if category_.parent_category_id is not None
            else None
        ),
        "name": category_.name,
        "type": category_.type,
        "display_order": category_.display_order,
    }
