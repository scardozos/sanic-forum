import copy
import pytest

from sanic.exceptions import BadRequest
from sanic_forum.api.users.models.requests import CreateUserRequest

VALID_REQUEST = {
    "username": "Perry",
}


def test_valid_request():
    CreateUserRequest(**VALID_REQUEST)


def test_short_username():
    request = copy.copy(VALID_REQUEST)
    request["username"] = ""
    with pytest.raises(BadRequest):
        CreateUserRequest(**request)


def test_min_len_username():
    request = copy.copy(VALID_REQUEST)
    request["username"] = "aaaaa"
    CreateUserRequest(**request)


def test_max_len_username():
    request = copy.copy(VALID_REQUEST)
    request["username"] = "a" * 20
    CreateUserRequest(**request)


def test_long_username():
    request = copy.copy(VALID_REQUEST)
    request["username"] = "a" * 21
    with pytest.raises(BadRequest):
        CreateUserRequest(**request)
