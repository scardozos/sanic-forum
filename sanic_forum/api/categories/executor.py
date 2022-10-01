from typing import List, Union
from uuid import UUID

from mayim import register

from sanic_forum.base.executor import BaseExecutor
from .model import Category


@register
class CategoryExecutor(BaseExecutor):
    async def insert(
        self,
        parent_category_id: Union[str, UUID],
        type: int,
        name: str,
        display_order: int,
    ) -> Category:
        ...

    async def select_all(self) -> List[Category]:
        ...

    async def select_by_id(self, id: Union[str, UUID]) -> Category:
        ...

    async def check_name_exists(
        self, parent_category_id: Union[str, UUID], type: int, name: str
    ) -> bool:
        ...

    async def update_for_insert(
        self,
        parent_category_id: Union[str, UUID],
        type: int,
        display_order: int,
    ) -> None:
        ...
