from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import openapi, validate

from sanic_forum.enums import ApiVersion
from sanic_forum.pagination import Pagination

from .models.requests import CreateUserRequest
from .models.responses import UserResponseV1, UsersResponseV1
from .service import UserService

SERVICE = UserService()
OPENAPI_TAG = "Users"

bp = Blueprint("api-v1-users", url_prefix="/users", version=1)


@bp.get("")
@openapi.tag(OPENAPI_TAG)
@openapi.parameter("limit", int, "query", required=False)
@openapi.parameter("offset", int, "query", required=False)
@openapi.response(200, UsersResponseV1)
async def list_all_users(_: Request, pagination: Pagination) -> HTTPResponse:
    users = await SERVICE.get_all(pagination.limit, pagination.offset)
    return json({"users": [user.serialize(ApiVersion.V1) for user in users]})


@bp.post("")
@openapi.tag(OPENAPI_TAG)
@openapi.body(CreateUserRequest)
@openapi.response(200, UserResponseV1)
@validate(json=CreateUserRequest)
async def create_user(_: Request, body: CreateUserRequest) -> HTTPResponse:
    user = await SERVICE.create(body)
    return json({"user": user.serialize(ApiVersion.V1)})
