from __future__ import annotations

from typing import Optional

from sanic_forum.enums import ApiVersion

from .responses import CategoryV1


class Category(object):
    def __init__(
        self,
        *,
        id: int,
        parent_category_id: Optional[int],
        name: Optional[str],
        type: int,
        display_order: Optional[int],
        **_,
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
            "id": self.id,
            "parent_category_id": (
                self.parent_category_id
                if self.parent_category_id is not None
                else None
            ),
            "name": self.name,
            "type": self.type,
            "display_order": self.display_order,
        }
