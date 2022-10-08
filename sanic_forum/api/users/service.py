from typing import List, Optional

from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic.exceptions import BadRequest
from sanic_forum.database.models.user.executor import UserExecutor
from sanic_forum.database.models.user.model import User

from .models.requests import CreateUserRequest


class UserService(object):
    def __init__(self):
        self._executor: Optional[UserExecutor] = None

    def _get_executor(self) -> UserExecutor:
        if self._executor is None:
            self._executor = Mayim.get(UserExecutor)
        return self._executor

    async def get_all(self, limit: int, offset: int) -> List[User]:
        executor = self._get_executor()
        return await executor.select_all(limit, offset)

    async def create(self, body: CreateUserRequest) -> User:
        executor = self._get_executor()

        async with executor.transaction():
            try:
                await executor.select_by_username(body.username)
            except RecordNotFound:
                pass
            else:
                raise BadRequest("Username is not available")

            return await executor.insert_and_return(body.username)
