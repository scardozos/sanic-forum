from typing import Optional, TypedDict
from sanic_forum.enums import CategoryType


class CategoryV1(TypedDict):
    id: int
    parent_category_id: Optional[int]
    name: Optional[str]
    type: CategoryType
    display_order: Optional[int]
