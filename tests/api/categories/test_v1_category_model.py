import uuid
import pytest

from sanic_forum.api.categories.model import Category
from sanic_forum.enums import ApiVersion


@pytest.mark.parametrize(
    "uuid,parent_category_uuid,name,type,display_order",
    [
        (uuid.uuid4(), None, "Root divider", 1, 0),
        (uuid.uuid4(), None, "Root forum", 2, 1),
        (uuid.uuid4(), uuid.uuid4(), "Child forum", 2, 0),
    ]
)
def test_category_properties(
    uuid, parent_category_uuid, name, type, display_order
):
    category = Category(
        uuid=uuid,
        parent_category_uuid=parent_category_uuid,
        name=name,
        type=type,
        display_order=display_order,
    )
    assert category.uuid == uuid
    assert category.parent_category_uuid == parent_category_uuid
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
        "uuid": str(category.uuid),
        "parent_category_uuid": (
            str(category.parent_category_uuid)
            if category.parent_category_uuid else None
        ),
        "name": category.name,
        "type": category.type,
        "display_order": category.display_order,
    }
