from __future__ import annotations

from typing import Optional
from uuid import UUID

from sanic_forum.enums import ApiVersion
from .types import CategoryV1
from ..__base__ import BaseModel


class Category(BaseModel):
    def __init__(
        self,
        *,
        id: UUID,
        parent_category_id: Optional[UUID],
        name: Optional[str],
        type: int,
        display_order: Optional[int],
    ) -> None:
        self.id = id
        self.parent_category_id = parent_category_id
        self.name = name
        self.type = type
        self.display_order = display_order

    def serialize(self, version: ApiVersion) -> CategoryV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return {
            "id": str(self.id),
            "parent_category_id": (
                str(self.parent_category_id)
                if self.parent_category_id
                else None
            ),
            "name": self.name,
            "type": self.type,
            "display_order": self.display_order,
        }
