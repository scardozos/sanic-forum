from __future__ import annotations

from typing import Callable

from sanic_forum.request import Request


async def check(request: Request, handler: Callable) -> None:
    """Run authentication checks here."""
