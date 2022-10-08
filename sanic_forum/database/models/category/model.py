from __future__ import annotations

from typing import cast, Optional

from pydantic import BaseModel
from sanic_forum.enums import ApiVersion, CategoryType
from .types import CategoryV1


class Category(BaseModel):
    id: int
    parent_category_id: Optional[int]
    name: Optional[str]
    type: CategoryType
    display_order: Optional[int]

    def serialize(self, version: ApiVersion) -> CategoryV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return cast(
            CategoryV1,
            self.dict(
                include={
                    "id",
                    "parent_category_id",
                    "name",
                    "type",
                    "display_order",
                }
            )
        )
