from unittest.mock import AsyncMock, Mock

import pytest
from sanic.exceptions import BadRequest

from sanic_forum.api.categories.requests import CreateCategoryRequest
from sanic_forum.api.categories.v1 import do_create, do_validate_create
from sanic_forum.enums import CategoryType

CATEGORY_CREATE_BODY = {
    "name": "Test Category",
    "type": CategoryType.FORUM_CATEGORY.value,
    "display_order": 1,
}


@pytest.mark.asyncio
async def test_do_validate_create_succeeds(executor, forum_root):
    body = CreateCategoryRequest(**CATEGORY_CREATE_BODY)
    executor.select_name_exists = AsyncMock(return_value=False)

    await do_validate_create(executor, body, forum_root)

    executor.select_name_exists.assert_awaited_once_with(
        forum_root.id, body.type, body.name
    )


@pytest.mark.asyncio
async def test_do_validate_create_checks_type(executor, forum_divider):
    create_body = CATEGORY_CREATE_BODY.copy()
    create_body["type"] = CategoryType.FORUM_DIVIDER.value
    body = CreateCategoryRequest(**create_body)
    executor.select_name_exists = AsyncMock(return_value=False)

    with pytest.raises(BadRequest):
        await do_validate_create(executor, body, forum_divider)

    executor.select_name_exists.assert_not_called()


@pytest.mark.asyncio
async def test_do_validate_create_checks_name_doesnt_exist(
    executor, forum_root
):
    body = CreateCategoryRequest(**CATEGORY_CREATE_BODY)
    executor.select_name_exists = AsyncMock(return_value=True)

    with pytest.raises(BadRequest):
        await do_validate_create(executor, body, forum_root)

    executor.select_name_exists.assert_awaited_once_with(
        forum_root.id, body.type, body.name
    )


@pytest.mark.asyncio
async def test_do_create_uses_transaction(
    executor, forum_root
):
    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor.transaction = Mock(return_value=transaction)
    executor.update_for_insert = AsyncMock()
    executor.insert_and_return = AsyncMock()

    body = CreateCategoryRequest(**CATEGORY_CREATE_BODY)
    await do_create(executor, body, forum_root)

    executor.transaction.assert_called_once()


@pytest.mark.asyncio
async def test_do_create_updates_positions(
    executor, forum_root
):
    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor.transaction = Mock(return_value=transaction)
    executor.update_for_insert = AsyncMock()
    executor.insert_and_return = AsyncMock()

    body = CreateCategoryRequest(**CATEGORY_CREATE_BODY)
    await do_create(executor, body, forum_root)

    executor.update_for_insert.assert_awaited_once_with(
        forum_root.id, body.type, body.display_order
    )


@pytest.mark.asyncio
async def test_do_create_inserts_and_returns(
    executor, forum_root
):
    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor.transaction = Mock(return_value=transaction)
    executor.update_for_insert = AsyncMock()
    executor.insert_and_return = AsyncMock(return_value="foo")

    body = CreateCategoryRequest(**CATEGORY_CREATE_BODY)
    returned = await do_create(executor, body, forum_root)

    executor.insert_and_return.assert_awaited_once_with(
        forum_root.id, body.type, body.name, body.display_order
    )
    assert returned == "foo"
