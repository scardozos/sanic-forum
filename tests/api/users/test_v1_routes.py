from unittest.mock import AsyncMock, patch

from pydantic_factories import ModelFactory
from sanic_forum.api.users.models.requests import CreateUserRequest
from sanic_forum.app import App
from sanic_forum.database.models.user.model import User
from sanic_forum.enums import ApiVersion


class UserFactory(ModelFactory):
    __model__ = User


def test_list_users(bp_testing_app: App):
    user: User = UserFactory.build()

    get_all = AsyncMock(return_value=[user])

    with patch("sanic_forum.api.users.v1.SERVICE.get_all", get_all):
        _, resp = bp_testing_app.test_client.get(
            "/api/v1/users?limit=1&offset=0",
        )

    assert resp.status == 200
    assert resp.json == {"users": [user.serialize(ApiVersion.V1)]}
    get_all.assert_awaited_once_with(1, 0)


def test_create_user(bp_testing_app: App):
    created: User = UserFactory.build()

    create_mock = AsyncMock(return_value=created)

    with patch("sanic_forum.api.users.v1.SERVICE.create", create_mock):
        _, resp = bp_testing_app.test_client.post(
            "/api/v1/users?limit=1&offset=0",
            json=dict(username=created.username),
        )

    expected_request = CreateUserRequest(username=created.username)

    assert resp.status == 200
    assert resp.json == {"user": created.serialize(ApiVersion.V1)}
    create_mock.assert_awaited_once_with(expected_request)
