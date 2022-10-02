from typing import List

from mayim import register

from sanic_forum.base.executor import BaseExecutor

from .model import User


@register
class UserExecutor(BaseExecutor):
    async def insert(self, username: str) -> User:
        ...

    async def select_all(self, limit: int, offset: int) -> List[User]:
        ...

    async def select_by_username(self, username: str) -> User:
        ...
