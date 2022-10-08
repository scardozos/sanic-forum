import pytest
from unittest.mock import AsyncMock, Mock, patch
from pydantic_factories import ModelFactory

from mayim.exception import RecordNotFound
from sanic.exceptions import BadRequest
from sanic_forum.api.users.service import UserService
from sanic_forum.api.users.models.requests import CreateUserRequest
from sanic_forum.database.models.user.model import User


class UserFactory(ModelFactory):
    __model__ = User


@pytest.fixture
def executor():
    executor_ = AsyncMock()
    transaction = AsyncMock()
    transaction.__aenter__ = AsyncMock()
    executor_.transaction = Mock(return_value=transaction)
    return executor_


@pytest.fixture
def mayim(executor):
    mayim_ = Mock()
    mayim_.get = Mock(return_value=executor)
    return mayim_


@pytest.fixture
def service(mayim):
    with patch("sanic_forum.api.users.service.Mayim", mayim):
        yield UserService()


@pytest.mark.asyncio
async def test_get_all(service: UserService, executor: AsyncMock):
    executor.select_all = AsyncMock(return_value="foo")
    result = await service.get_all(1, 0)
    executor.select_all.assert_awaited_once_with(1, 0)
    assert result == "foo"


@pytest.mark.asyncio
async def test_create(service: UserService, executor: AsyncMock):
    executor.select_by_username = AsyncMock(
        side_effect=RecordNotFound("User not found")
    )
    executor.insert_and_return = AsyncMock(return_value="bar")

    request = CreateUserRequest(username="Perry")
    result = await service.create(request)

    executor.select_by_username.assert_awaited_once_with(request.username)
    executor.insert_and_return.assert_awaited_once_with(request.username)
    assert result == "bar"


@pytest.mark.asyncio
async def test_create_dupe_username(service: UserService, executor: AsyncMock):
    user: User = UserFactory.build()
    executor.select_by_username = AsyncMock(return_value=user)

    request = CreateUserRequest(username="Perry")
    with pytest.raises(BadRequest):
        await service.create(request)

    executor.select_by_username.assert_awaited_once_with(request.username)
    executor.insert_and_return.assert_not_called()
