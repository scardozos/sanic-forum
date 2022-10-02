from unittest.mock import AsyncMock, patch

import pytest

from sanic_forum.api.categories.executor import CategoryExecutor
from sanic_forum.api.categories.v1 import do_get_all


@pytest.mark.asyncio
async def test_do_get_all(executor, mayim):
    executor.select_all = AsyncMock(return_value="foo")
    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        result = await do_get_all()

    assert result == "foo"
    mayim.get.assert_called_once_with(CategoryExecutor)
    executor.select_all.assert_called_once_with()
