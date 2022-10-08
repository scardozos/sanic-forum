import pytest
from unittest.mock import AsyncMock, Mock, patch
from pydantic_factories import ModelFactory

from sanic.exceptions import BadRequest
from sanic_forum.api.categories.service import CategoryService
from sanic_forum.api.categories.models.requests import (
    AllowedCategoryType,
    CreateCategoryRequest,
)
from sanic_forum.database.models.category.model import Category


class CategoryFactory(ModelFactory):
    __model__ = Category


@pytest.fixture
def executor():
    executor_ = AsyncMock()
    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor_.transaction = Mock(return_value=transaction)
    return executor_


@pytest.fixture
def mayim(executor):
    mock = Mock()
    mock.get = Mock(return_value=executor)
    return mock


@pytest.fixture
def service(mayim):
    with patch("sanic_forum.api.categories.service.Mayim", mayim):
        yield CategoryService()


@pytest.mark.asyncio
async def test_get_by_id(service: CategoryService, executor: AsyncMock):
    executor.select_by_id = AsyncMock(return_value="foo")
    result = await service.get_by_id(1)
    executor.select_by_id.assert_awaited_once_with(1)
    assert result == "foo"


@pytest.mark.asyncio
async def test_get_root(service: CategoryService, executor: AsyncMock):
    executor.select_root = AsyncMock(return_value="foo")
    result = await service.get_root()
    executor.select_root.assert_awaited_once_with()
    assert result == "foo"


@pytest.mark.asyncio
async def test_get_children(service: CategoryService, executor: AsyncMock):
    executor.select_by_id = AsyncMock()
    executor.select_children = AsyncMock(return_value="foo")
    result = await service.get_children(1)
    executor.select_by_id.assert_awaited_once_with(1)
    executor.select_children.assert_awaited_once_with(1)
    assert result == "foo"


@pytest.mark.asyncio
async def test_create(service: CategoryService, executor: AsyncMock):
    parent = CategoryFactory.build()
    executor.select_by_id = AsyncMock(return_value=parent)
    executor.update_for_insert = AsyncMock()
    executor.insert_and_return = AsyncMock(return_value="foo")

    body = CreateCategoryRequest(
        name="foo", type=AllowedCategoryType.FORUM_CATEGORY, display_order=1
    )

    result = await service.create(body, parent.id)

    executor.select_by_id.assert_awaited_once_with(parent.id)
    executor.update_for_insert.assert_awaited_once_with(
        parent.id, body.display_order
    )
    executor.insert_and_return.assert_awaited_once_with(
        parent.id, body.type.value, body.name, body.display_order
    )

    assert result == "foo"


@pytest.mark.asyncio
async def test_create_divider_outside_root(
    service: CategoryService, executor: AsyncMock
):
    parent = CategoryFactory.build()
    parent.type = AllowedCategoryType.FORUM_DIVIDER.value

    executor.select_by_id = AsyncMock(return_value=parent)

    body = CreateCategoryRequest(
        name="foo", type=AllowedCategoryType.FORUM_DIVIDER, display_order=1
    )

    with pytest.raises(BadRequest):
        await service.create(body, parent.id)

    executor.select_by_id.assert_awaited_once_with(parent.id)
