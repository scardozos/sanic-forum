from typing import List

from mayim import Mayim
from sanic import Blueprint
from sanic.exceptions import BadRequest
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import validate

from sanic_forum.enums import ApiVersion, CategoryType

from .executor import CategoryExecutor
from .model import Category
from .requests import CreateCategoryRequest

bp = Blueprint("api-v1-categories", url_prefix="/categories", version=1)


@bp.get("")
async def list_categories(_: Request) -> HTTPResponse:
    all_categories = await do_get_all()
    response = [cat.serialize(ApiVersion.V1) for cat in all_categories]
    return json({"categories": response})


async def do_get_all() -> List[Category]:
    executor = Mayim.get(CategoryExecutor)
    return await executor.select_all()


@bp.get("/__root__")
async def list_root_categories(_: Request) -> HTTPResponse:
    root_categories = await do_get_root()
    response = [cat.serialize(ApiVersion.V1) for cat in root_categories]
    return json({"categories": response})


async def do_get_root() -> List[Category]:
    executor = Mayim.get(CategoryExecutor)
    return await executor.select_root()


@bp.post("/<category_id:int>")
@validate(json=CreateCategoryRequest)
async def create_category(
    _: Request, body: CreateCategoryRequest, category_id: int, **__
) -> HTTPResponse:
    executor = Mayim.get(CategoryExecutor)
    parent = await executor.select_by_id(category_id)
    await do_validate_create(executor, body, parent)
    category = await do_create(executor, body, parent)
    return json({"category": category.serialize(ApiVersion.V1)})


async def do_validate_create(
    executor: CategoryExecutor, body: CreateCategoryRequest, parent: Category
) -> None:
    if (
        body.type == CategoryType.FORUM_DIVIDER
        and parent.type != CategoryType.FORUM_ROOT
    ):
        raise BadRequest("Divider type can only exist at forum root")

    # Name does not exist
    qargs = (parent.id, body.type, body.name)
    if await executor.select_name_exists(*qargs):
        raise BadRequest("Name is already in use")


async def do_create(
    executor: CategoryExecutor, body: CreateCategoryRequest, parent: Category
) -> Category:
    async with executor.transaction():
        qargs = (parent.id, body.type, body.display_order)
        await executor.update_for_insert(*qargs)

        qargs = (
            parent.id,
            body.type,
            body.name,
            body.display_order,
        )
        return await executor.insert_and_return(*qargs)
