from uuid import UUID
from mayim import Mayim
from sanic import Blueprint
from sanic.exceptions import BadRequest
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import validate

from .executor import CategoryExecutor
from sanic_forum.enums import ApiVersion, CategoryType
from .requests import CreateCategoryRequest


bp = Blueprint("api-v1-categories", url_prefix="/categories", version=1)


@bp.get("")
async def list_categories(_: Request) -> HTTPResponse:
    executor = Mayim.get(CategoryExecutor)
    categories = await executor.select_all()
    return json([category.serialize(ApiVersion.V1) for category in categories])


@bp.post("/<category_id:uuid>")
@validate(json=CreateCategoryRequest)
async def create_category(
    _: Request, body: CreateCategoryRequest, category_id: UUID, **__
) -> HTTPResponse:
    executor = Mayim.get(CategoryExecutor)

    parent = await executor.select_by_id(category_id)

    if (
        body.type == CategoryType.FORUM_DIVIDER
        and parent.type != CategoryType.FORUM_ROOT
    ):
        raise BadRequest("Divider type can only exist at forum root")

    # Name does not exist
    qargs = (parent.id, body.type, body.name)
    if await executor.check_name_exists(*qargs):
        raise BadRequest("Name is already in use")

    async with executor.transaction():
        qargs = (parent.id, body.type, body.display_order)
        await executor.update_for_insert(*qargs)

        qargs = (
            parent.id,
            body.type,
            body.name,
            body.display_order,
        )
        category = await executor.insert(*qargs)

    return json(category.serialize(ApiVersion.V1))
