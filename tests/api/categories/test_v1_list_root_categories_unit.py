from unittest.mock import AsyncMock, patch

import pytest

from sanic_forum.api.categories.executor import CategoryExecutor
from sanic_forum.api.categories.v1 import do_get_root


@pytest.mark.asyncio
async def test_do_get_root(executor, mayim):
    executor.select_root = AsyncMock(return_value="foo")
    with patch("sanic_forum.api.categories.v1.Mayim", mayim):
        result = await do_get_root()

    assert result == "foo"
    mayim.get.assert_called_once_with(CategoryExecutor)
    executor.select_root.assert_called_once_with()
