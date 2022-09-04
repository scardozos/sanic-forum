from typing import Optional, TypedDict


class CategoryV1(TypedDict):
    id: str
    parent_category_id: Optional[str]
    name: Optional[str]
    type: int
    display_order: Optional[int]
