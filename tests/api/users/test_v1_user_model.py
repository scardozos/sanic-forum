import uuid

from sanic_forum.enums import ApiVersion
from sanic_forum.api.users.model import User


def test_user_has_expected_properties():
    id = uuid.uuid4()
    user = User(id=id, username="test")
    assert user.id == id
    assert user.username == "test"


def test_user_serialize_method(user):
    assert user.serialize(ApiVersion.V1) == {
        "id": str(user.id),
        "username": user.username,
    }
