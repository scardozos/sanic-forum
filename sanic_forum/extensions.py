from sanic_ext.extensions.injection.extension import InjectionExtension
# from sanic_ext.extensions.openapi.extension import OpenAPIExtension

from sanic_forum.app import App
from sanic_forum.database import models


def setup(app: App) -> None:
    app.extend(
        extensions=[
            InjectionExtension,
            # OpenAPIExtension,
        ],
        built_in_extensions=False,
    )

    models.setup_injection(app)
