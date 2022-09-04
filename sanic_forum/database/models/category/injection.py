from uuid import UUID

from mayim import Mayim
from sanic import Request
from sanic.exceptions import NotFound

from sanic_forum.app import App
from .executor import CategoryExecutor
from .category import Category


async def inject_category(
    request: Request, category_id: UUID, **_
) -> Category:
    executor = Mayim.get(CategoryExecutor)
    category = await executor.select_by_id(category_id)

    if category is None:
        raise NotFound("Category not found")

    return category


def setup_category_injection(app: App) -> None:
    app.ext.add_dependency(Category, inject_category)
