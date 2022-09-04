from sanic_forum.app import App
from .category import Category, CategoryExecutor, setup_category_injection
from .user import User, UserExecutor

__all__ = (
    "Category",
    "CategoryExecutor",
    "User",
    "UserExecutor",
    "setup_injection",
)


def setup_injection(app: App) -> None:
    setup_category_injection(app)
