from __future__ import annotations

from importlib import import_module
from typing import Optional, Sequence, cast

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic_ext import Extend

import sanic_forum.config as config
import sanic_forum.request as request
from sanic_forum.constants import APP_NAME, ENV_PREFIX

DEFAULT_MODULES = (
    "sanic_forum.api",
    "sanic_forum.database",
    "sanic_forum.security",
    "sanic_forum.extensions",
    "sanic_forum.pagination",
)


class App(Sanic):
    config: config.Config
    ext: Extend
    request: request.Request

    @classmethod
    def get_app(
        cls, name: Optional[str] = None, *, force_create: bool = False
    ) -> App:
        return cast(App, super().get_app(name, force_create=force_create))


def create(module_names: Optional[Sequence[str]] = None) -> App:
    try:
        app = App.get_app(APP_NAME)
    except SanicException:
        app = App(
            APP_NAME,
            config=config.Config(env_prefix=ENV_PREFIX),
            request_class=request.Request,
            strict_slashes=True,
        )

    if module_names is None:
        module_names = DEFAULT_MODULES

    for module_name in module_names:
        module = import_module(module_name)

        if setup := getattr(module, "setup", None):
            setup(app)

    return app
