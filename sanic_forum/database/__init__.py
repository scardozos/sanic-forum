from __future__ import annotations

from typing import TYPE_CHECKING

from mayim import Mayim

if TYPE_CHECKING:
    from sanic_forum.app import App


def setup(app: App) -> None:
    @app.before_server_start
    async def setup_database(*_):
        app.ctx.mayim = Mayim(dsn=app.config.DATABASE_URL, strict=True)
