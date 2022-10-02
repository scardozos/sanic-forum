import uuid
from unittest.mock import AsyncMock, Mock

import pytest

from sanic_forum.api.users.model import User


@pytest.fixture
def user():
    return User(id=uuid.uuid4(), username="prryplatypus")


@pytest.fixture
def user_executor(user):
    executor = Mock()
    executor.insert = AsyncMock(return_value=user)
    executor.select_all = AsyncMock(return_value=[user])
    executor.select_by_username = AsyncMock(return_value=user)

    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor.transaction = Mock(return_value=transaction)

    return executor


@pytest.fixture
def mayim(user_executor):
    mayim = Mock()
    mayim.get = Mock(return_value=user_executor)
    return mayim
