from __future__ import annotations

from typing import Optional
from uuid import UUID

from sanic_forum.enums import ApiVersion
from .responses import CategoryV1


class Category(object):
    def __init__(
        self,
        *,
        uuid: UUID,
        parent_category_uuid: Optional[UUID],
        name: Optional[str],
        type: int,
        display_order: Optional[int],
        **_
    ) -> None:
        self.uuid = uuid
        self.parent_category_uuid = parent_category_uuid
        self.name = name
        self.type = type
        self.display_order = display_order

    def serialize(self, version: ApiVersion) -> CategoryV1:
        if version != ApiVersion.V1:
            raise NotImplementedError()

        return {
            "uuid": str(self.uuid),
            "parent_category_uuid": (
                str(self.parent_category_uuid)
                if self.parent_category_uuid
                else None
            ),
            "name": self.name,
            "type": self.type,
            "display_order": self.display_order,
        }
