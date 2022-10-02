from typing import Optional, TypedDict


class CategoryV1(TypedDict):
    id: int
    parent_category_id: Optional[int]
    name: Optional[str]
    type: int
    display_order: Optional[int]
