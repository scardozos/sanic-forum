from typing import Optional, List, Union
from uuid import UUID

from mayim import PostgresExecutor, register

from .category import Category


@register
class CategoryExecutor(PostgresExecutor):
    async def insert_and_return(
        self,
        parent_category_id: Union[str, UUID],
        type: int,
        name: str,
        display_order: int,
    ) -> Category:
        ...

    async def select_all(self) -> List[Category]:
        ...

    async def select_by_id(self, id: Union[str, UUID]) -> Optional[Category]:
        ...

    async def select_bool_by_name(
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
