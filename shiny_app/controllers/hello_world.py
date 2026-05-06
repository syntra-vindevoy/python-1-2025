from typing import Any

from shiny import render

from shiny_app.core.controller import ShinyAppController
from shiny_app.core.utils import trace, enable_tracing, enable_logging


@enable_logging
@enable_tracing
class HelloWorldController(ShinyAppController):
    def __call__(self, inputs: Any, outputs: Any, session: Any) -> None:
        @outputs(id="label_greeting")
        @render.text
        @trace
        def render_label_greeting() -> str:
            name = inputs.input_name()
            message = "Hello, stranger"

            if name:
                message = f"Hello, {name}"

            self.logger.debug(f"greeting name={name}")

            return message
