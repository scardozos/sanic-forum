from typing import Optional, TypedDict


class CategoryV1(TypedDict):
    uuid: str
    parent_category_uuid: Optional[str]
    name: Optional[str]
    type: int
    display_order: Optional[int]
