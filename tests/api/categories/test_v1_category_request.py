import pytest

from sanic.exceptions import BadRequest
from sanic_forum.api.categories.requests import CreateCategoryRequest
from sanic_forum.enums import CategoryType


def test_create_category_request_succeeds():
    request = CreateCategoryRequest(
        name="Test Category",
        display_order=1,
        type=CategoryType.FORUM_DIVIDER.value,
    )
    assert request.name == "Test Category"
    assert request.display_order == 1
    assert request.type == CategoryType.FORUM_DIVIDER.value


@pytest.mark.parametrize(
    ["name", "success"],
    [
        ("", False),
        ("1", True),
        ("12345", True),
        ("Lorem ipsum", True),
        ("a" * 250, True),
        ("a" * 251, False),
    ]
)
def test_create_category_request_validates_name(name: str, success: bool):
    if success:
        return CreateCategoryRequest(
            name=name, display_order=1, type=CategoryType.FORUM_DIVIDER.value
        )

    with pytest.raises(BadRequest):
        CreateCategoryRequest(
            name=name, display_order=1, type=CategoryType.FORUM_DIVIDER.value
        )


@pytest.mark.parametrize(
    ["display_order", "success"],
    [
        (0, False),
        (1, True),
        (21, True),
    ]
)
def test_create_category_request_validates_order(
    display_order: int, success: bool
):
    if success:
        return CreateCategoryRequest(
            name="Lorem ipsum",
            display_order=display_order,
            type=CategoryType.FORUM_DIVIDER.value
        )

    with pytest.raises(BadRequest):
        CreateCategoryRequest(
            name="Lorem ipsum",
            display_order=display_order,
            type=CategoryType.FORUM_DIVIDER.value
        )


@pytest.mark.parametrize(
    ["type", "success"],
    [
        (CategoryType.FORUM_ROOT.value, False),
        (CategoryType.FORUM_DIVIDER.value, True),
        (CategoryType.FORUM_CATEGORY.value, True),
    ]
)
def test_create_category_request_validates_type(
    type: int, success: bool
):
    if success:
        return CreateCategoryRequest(
            name="Lorem ipsum",
            display_order=1,
            type=type
        )

    with pytest.raises(BadRequest):
        CreateCategoryRequest(
            name="Lorem ipsum",
            display_order=1,
            type=type
        )
