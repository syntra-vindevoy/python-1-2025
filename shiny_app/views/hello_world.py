from shiny import ui

from shiny_app.core.utils import enable_tracing, enable_logging
from shiny_app.core.view import ShinyAppView


@enable_logging
@enable_tracing
class HelloWorldView(ShinyAppView):
    def __call__(self):
        page = ui.page_fluid(
            ui.h1("Hello World Example"),
            ui.input_text(id="input_name", label="Enter your name:"),
            ui.output_text(id="label_greeting"),
        )

        self.logger.debug(f"page:\n\n{page}\n")

        return page
