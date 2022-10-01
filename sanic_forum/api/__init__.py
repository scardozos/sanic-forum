from __future__ import annotations

from typing import TYPE_CHECKING

from sanic import Blueprint

from .categories.v1 import bp as categories_bp
from .users.v1 import bp as users_bp

if TYPE_CHECKING:
    from sanic_forum.app import App


bp = Blueprint.group(
    categories_bp,
    users_bp,
    version_prefix="/api/v",
)


def setup(app: App) -> None:
    app.blueprint(bp)
