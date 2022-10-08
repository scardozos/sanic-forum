import pytest

from sanic_forum.api.categories.models.requests import AllowedCategoryType
from sanic_forum.enums import CategoryType


@pytest.mark.parametrize(
    "attr, expected_value",
    [
        ("FORUM_DIVIDER", CategoryType.FORUM_DIVIDER.value),
        ("FORUM_CATEGORY", CategoryType.FORUM_CATEGORY.value),
    ]
)
def test_values_are_equivalent_to_all_category_types(
    attr: str, expected_value: int
):
    assert getattr(AllowedCategoryType, attr).value == expected_value
