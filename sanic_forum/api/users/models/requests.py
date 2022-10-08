from pydantic import BaseModel, validator
from sanic.exceptions import BadRequest


class CreateUserRequest(BaseModel):
    username: str

    @validator("username")
    def validate_username(cls, username: str):
        length = len(username)
        min_, max_ = 5, 20

        if length < min_ or length > max_:
            raise BadRequest(
                f"Username must be between {min_} and {max_} characters"
            )

        if not username.isprintable():
            raise BadRequest("Invalid username")

        return username
