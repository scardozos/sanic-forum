from uuid import UUID

from sanic_forum.enums import ApiVersion

from .responses import UserV1


class User(object):
    def __init__(self, *, id: UUID, username: str, **_) -> None:
        self.id = id
        self.username = username

    def serialize(self, version: ApiVersion) -> UserV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return {
            "id": str(self.id),
            "username": self.username,
        }
