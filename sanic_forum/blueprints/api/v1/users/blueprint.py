from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Blueprint
from sanic.exceptions import BadRequest
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import validate

from sanic_forum.database.models import UserExecutor
from sanic_forum.enums import ApiVersion
from sanic_forum.pagination import Pagination
from .requests import CreateUserRequest

bp = Blueprint("api-v1-users", url_prefix="/users")


@bp.get("")
async def list_all_users(_: Request, pagination: Pagination) -> HTTPResponse:
    executor = Mayim.get(UserExecutor)
    users = await executor.select_all_users(
        pagination.limit, pagination.offset
    )
    return json([user.serialize(ApiVersion.V1) for user in users])


@bp.post("")
@validate(json=CreateUserRequest)
async def create_user(_: Request, body: CreateUserRequest) -> HTTPResponse:
    executor = Mayim.get(UserExecutor)

    async with executor.transaction():
        try:
            await executor.select_user_by_username(body.username)
        except RecordNotFound:
            pass
        else:
            raise BadRequest("Username is not available")

        user = await executor.insert_user(body.username)

    return json(user.serialize(ApiVersion.V1))
