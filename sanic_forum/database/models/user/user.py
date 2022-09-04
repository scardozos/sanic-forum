from uuid import UUID

from sanic_forum.enums import ApiVersion
from .types import UserV1
from ..__base__ import BaseModel


class User(BaseModel):
    def __init__(self, *, id: UUID, username: str) -> None:
        self.id = id
        self.username = username

    def serialize(self, version: ApiVersion) -> UserV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return {
            "id": str(self.id),
            "username": self.username,
        }
