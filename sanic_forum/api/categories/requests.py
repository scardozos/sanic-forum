from dataclasses import dataclass

from sanic.exceptions import BadRequest

from sanic_forum.enums import CategoryType


@dataclass
class CreateCategoryRequest:
    name: str
    display_order: int
    type: int

    def __post_init__(self):
        self.validate_name()
        self.validate_display_order()
        self.validate_type()

    def validate_display_order(self):
        min_ = 1
        if self.display_order < min_:
            raise BadRequest(
                f"Display order must be an integer greater than {min_}"
            )

    def validate_name(self) -> None:
        name_len = len(self.name)
        min_, max_ = 1, 250
        if name_len < min_ or name_len > max_:
            raise BadRequest(
                f"Name must be between {min_} and {max_} characters"
            )

    def validate_type(self) -> None:
        valid_types = (
            CategoryType.FORUM_DIVIDER.value,
            CategoryType.FORUM_CATEGORY.value,
        )
        if self.type not in valid_types:
            raise BadRequest(f"Type must be one of {valid_types}")
