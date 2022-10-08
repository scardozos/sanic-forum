from typing import List, Optional

from mayim import Mayim
from sanic.exceptions import BadRequest
from sanic_forum.database.models.category.executor import CategoryExecutor
from sanic_forum.database.models.category.model import Category
from sanic_forum.enums import CategoryType
from .models.requests import CreateCategoryRequest


class CategoryService(object):
    def __init__(self):
        self._executor: Optional[CategoryExecutor] = None

    def _get_executor(self) -> CategoryExecutor:
        if self._executor is None:
            self._executor = Mayim.get(CategoryExecutor)
        return self._executor

    async def get_by_id(self, category_id: int) -> Category:
        executor = self._get_executor()
        return await executor.select_by_id(category_id)

    async def get_root(self) -> List[Category]:
        executor = self._get_executor()
        return await executor.select_root()

    async def get_children(self, category_id: int) -> List[Category]:
        executor = self._get_executor()
        await executor.select_by_id(category_id)
        return await executor.select_children(category_id)

    async def create(
        self, body: CreateCategoryRequest, parent_id: int
    ) -> Category:
        executor = self._get_executor()
        parent = await executor.select_by_id(parent_id)

        if (
            body.type == CategoryType.FORUM_DIVIDER
            and parent.type != CategoryType.FORUM_ROOT
        ):
            raise BadRequest("Divider type can only exist at forum root")

        async with executor.transaction():
            qargs = (parent.id, body.display_order)
            await executor.update_for_insert(*qargs)
            qargs = (
                parent.id,
                body.type.value,
                body.name,
                body.display_order,
            )
            return await executor.insert_and_return(*qargs)
