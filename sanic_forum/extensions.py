from sanic.signals import Event
from sanic_ext import Config
from sanic_ext.extensions.injection.extension import InjectionExtension

from sanic_forum.app import App

from sanic_ext.extensions.openapi.extension import OpenAPIExtension


def setup(app: App) -> None:
    app.extend(
        extensions=[
            InjectionExtension,
            OpenAPIExtension,
        ],
        built_in_extensions=False,
        config=Config(
            injection_signal=Event.HTTP_HANDLER_BEFORE,
            swagger_ui_configuration={
                "apisSorter": "method",
                "operationsSorter": "alpha",
                "docExpansion": "list"
            },
        ),
    )
