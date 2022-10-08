import copy
import pytest

from pydantic import ValidationError
from sanic.exceptions import BadRequest
from sanic_forum.api.categories.models.requests import CreateCategoryRequest

VALID_REQUEST = {
    "name": "Perry",
    "display_order": 1,
    "type": 3,
}


def test_valid_request():
    CreateCategoryRequest(**VALID_REQUEST)


def test_short_name():
    request = copy.copy(VALID_REQUEST)
    request["name"] = ""
    with pytest.raises(BadRequest):
        CreateCategoryRequest(**request)


def test_min_len_name():
    request = copy.copy(VALID_REQUEST)
    request["name"] = "a"
    CreateCategoryRequest(**request)


def test_negative_display_order():
    request = copy.copy(VALID_REQUEST)
    request["display_order"] = -1
    with pytest.raises(BadRequest):
        CreateCategoryRequest(**request)


def test_zero_display_order():
    request = copy.copy(VALID_REQUEST)
    request["display_order"] = 0
    with pytest.raises(BadRequest):
        CreateCategoryRequest(**request)


def test_min_display_order():
    request = copy.copy(VALID_REQUEST)
    request["display_order"] = 1
    CreateCategoryRequest(**request)


@pytest.mark.parametrize("type_", [2, 3])
def test_valid_type(type_):
    request = copy.copy(VALID_REQUEST)
    request["type"] = type_
    CreateCategoryRequest(**request)


@pytest.mark.parametrize("type_", [1, 4])
def test_invalid_type(type_):
    request = copy.copy(VALID_REQUEST)
    request["type"] = type_
    with pytest.raises(ValidationError):
        CreateCategoryRequest(**request)
