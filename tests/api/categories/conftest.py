from unittest.mock import Mock

import pytest

from sanic_forum.api.categories.model import Category
from sanic_forum.enums import CategoryType


@pytest.fixture
def forum_root():
    return Category(
        id=1,
        parent_category_id=None,
        name=None,
        display_order=None,
        type=CategoryType.FORUM_ROOT.value,
    )


@pytest.fixture
def forum_divider(forum_root: Category):
    return Category(
        id=2,
        parent_category_id=forum_root.id,
        name="All categories",
        display_order=1,
        type=CategoryType.FORUM_DIVIDER.value,
    )


@pytest.fixture
def forum_category(forum_divider: Category):
    return Category(
        id=3,
        parent_category_id=forum_divider.id,
        name="General",
        display_order=1,
        type=CategoryType.FORUM_CATEGORY.value,
    )


@pytest.fixture
def executor():
    executor = Mock()
    return executor


@pytest.fixture
def mayim(executor):
    mayim = Mock()
    mayim.get = Mock(return_value=executor)
    return mayim
