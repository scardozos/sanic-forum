from __future__ import annotations

from typing import cast

from pydantic import BaseModel
from sanic_forum.enums import ApiVersion
from .types import UserV1


class User(BaseModel):
    id: int
    username: str

    def serialize(self, version: ApiVersion) -> UserV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return cast(
            UserV1,
            self.dict(
                include={
                    "id",
                    "username",
                }
            ),
        )
