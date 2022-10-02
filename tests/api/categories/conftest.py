import pytest
import uuid
from unittest.mock import AsyncMock, Mock

from sanic_forum.api.categories.model import Category
from sanic_forum.enums import CategoryType


@pytest.fixture
def forum_root():
    return Category(
        uuid=uuid.uuid4(),
        parent_category_uuid=None,
        name=None,
        display_order=None,
        type=CategoryType.FORUM_ROOT.value,
    )


@pytest.fixture
def forum_divider(forum_root):
    return Category(
        uuid=uuid.uuid4(),
        parent_category_uuid=forum_root.uuid,
        name="All categories",
        display_order=1,
        type=CategoryType.FORUM_DIVIDER.value,
    )


@pytest.fixture
def forum_category(forum_divider):
    return Category(
        uuid=uuid.uuid4(),
        parent_category_uuid=forum_divider.uuid,
        name="General",
        display_order=1,
        type=CategoryType.FORUM_CATEGORY.value,
    )


@pytest.fixture
def executor():
    executor = Mock()

    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor.transaction = Mock(return_value=transaction)

    return executor


@pytest.fixture
def mayim(executor):
    mayim = Mock()
    mayim.get = Mock(return_value=executor)
    return mayim
