from abc import ABC

import uvicorn
from shiny import App

from shiny_app.core.controller import ShinyAppController
from shiny_app.core.model import ShinyAppModel
from shiny_app.core.utils import enable_tracing, enable_logging
from shiny_app.core.view import ShinyAppView


@enable_logging
@enable_tracing
class ShinyApp(ABC):
    def __init__(
        self,
        *,
        model: type[ShinyAppModel],
        view: type[ShinyAppView],
        controller: type[ShinyAppController],
    ):
        super().__init__()
        self.model = model()
        self.view = view()
        self.controller = controller()
        self.app = App(self.view(), self.controller)

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    def run(self, **kwargs):
        self.logger.success("starting server")

        uvicorn.run(self.app, **kwargs)

        self.logger.critical("stopping server")
