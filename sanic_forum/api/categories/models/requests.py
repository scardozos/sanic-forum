from enum import IntEnum
from pydantic import BaseModel, validator
from sanic.exceptions import BadRequest

from sanic_forum.enums import CategoryType


class AllowedCategoryType(IntEnum):
    FORUM_DIVIDER = CategoryType.FORUM_DIVIDER.value
    FORUM_CATEGORY = CategoryType.FORUM_CATEGORY.value


class CreateCategoryRequest(BaseModel):
    name: str
    display_order: int
    type: AllowedCategoryType

    @validator("display_order")
    def validate_display_order(cls, display_order: int) -> int:
        min_ = 1
        if display_order < min_:
            raise BadRequest(
                f"Display order must be an integer greater or equal to {min_}"
            )
        return display_order

    @validator("name")
    def validate_name(cls, name: str) -> str:
        name_len = len(name)
        min_, max_ = 1, 250
        if name_len < min_ or name_len > max_:
            raise BadRequest(
                f"Name must be between {min_} and {max_} characters"
            )
        return name
