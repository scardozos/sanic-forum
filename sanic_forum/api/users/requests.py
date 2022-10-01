from dataclasses import dataclass

from sanic.exceptions import BadRequest


@dataclass
class CreateUserRequest:
    username: str

    def __post_init__(self):
        self.validate_username()

    def validate_username(self):
        length = len(self.username)
        min_, max_ = 5, 20

        if length < min_ or length > max_:
            raise BadRequest(
                f"Username must be between {min_} and {max_} characters"
            )
