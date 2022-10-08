from typing import List, TypedDict

from sanic_forum.database.models.user.types import UserV1


class UserResponseV1(TypedDict):
    user: UserV1


class UsersResponseV1(TypedDict):
    users: List[UserV1]
