import uuid
import pytest

from sanic_forum.database.models import Category
from sanic_forum.enums import ApiVersion


@pytest.mark.parametrize(
    "id,parent_category_id,name,type,display_order",
    [
        (uuid.uuid4(), None, "Root divider", 1, 0),
        (uuid.uuid4(), None, "Root forum", 2, 1),
        (uuid.uuid4(), uuid.uuid4(), "Child forum", 2, 0),
    ]
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
    category = request.getfixturevalue(category)

    assert category.serialize(ApiVersion.V1) == {
        "id": str(category.id),
        "parent_category_id": (
            str(category.parent_category_id)
            if category.parent_category_id else None
        ),
        "name": category.name,
        "type": category.type,
        "display_order": category.display_order,
    }
