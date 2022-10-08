from typing import List

from mayim import register

from sanic_forum.base.executor import BaseExecutor

from .model import Category


@register
class CategoryExecutor(BaseExecutor):
    async def insert_and_return(
        self,
        parent_category_id: int,
        type: int,
        name: str,
        display_order: int,
    ) -> Category:
        ...

    async def select_children(self, category_id: int) -> List[Category]:
        ...

    async def select_by_id(self, id: int) -> Category:
        ...

    async def select_name_exists(
        self, parent_category_id: int, type: int, name: str
    ) -> bool:
        ...

    async def select_root(self) -> List[Category]:
        ...

    async def update_for_insert(
        self,
        parent_category_id: int,
        display_order: int,
    ) -> None:
        ...
