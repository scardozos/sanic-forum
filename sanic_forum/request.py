from __future__ import annotations

from typing import TYPE_CHECKING

from sanic import Request as SanicRequest

if TYPE_CHECKING:
    from sanic_forum.app import App


class Request(SanicRequest):
    app: App
