from typing import List

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import validate, openapi

from sanic_forum.database.models.category.types import CategoryV1
from sanic_forum.enums import ApiVersion

from .models.responses import ListRootCategoriesResponseV1, ListChildrenCategoriesResponseV1, CreateCategoryResponseV1
from .models.requests import CreateCategoryRequest
from .service import CategoryService

SERVICE = CategoryService()
OPENAPI_TAG = "Categories"

bp = Blueprint("api-v1-categories", url_prefix="/categories", version=1)


@bp.get("/__root__")
@openapi.tag(OPENAPI_TAG)
@openapi.response(200, ListRootCategoriesResponseV1)
async def list_root_categories(_: Request) -> HTTPResponse:
    root_categories = await SERVICE.get_root()
    response = [cat.serialize(ApiVersion.V1) for cat in root_categories]
    return json({"categories": response})


@bp.get("/<category_id:int>")
@openapi.tag(OPENAPI_TAG)
@openapi.response(200, ListChildrenCategoriesResponseV1)
async def list_children_categories(
    _: Request, category_id: int
) -> HTTPResponse:
    child_categories = await SERVICE.get_children(category_id)
    response = [cat.serialize(ApiVersion.V1) for cat in child_categories]
    return json({"categories": response})


@bp.post("/<category_id:int>")
@openapi.tag(OPENAPI_TAG)
@openapi.body(CreateCategoryRequest)
@openapi.response(200, CreateCategoryResponseV1)
@validate(json=CreateCategoryRequest)
async def create_category(
    _: Request, body: CreateCategoryRequest, category_id: int
) -> HTTPResponse:
    print(f"reqBody:{body}")
    new_category = await SERVICE.create(body, category_id)
    return json({"category": new_category.serialize(ApiVersion.V1)})
