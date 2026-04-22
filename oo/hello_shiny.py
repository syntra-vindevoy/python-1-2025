from typing import Any

from shiny import ui, render

from shiny_application import ShinyApplication


class HelloWorldApplication(ShinyApplication):
    def __init__(self):
        self.logger.trace(f"entering {__class__.__name__}.__init__")

        super().__init__()

        self.logger.trace(f"exiting {__class__.__name__}.__init__")

    @property
    def layout(self):
        self.logger.trace("entering layout")

        page = ui.page_fluid(
            ui.h1("Hello World Example"),
            ui.input_text(id="input_name", label="Enter your name:"),
            ui.output_text(id="label_greeting"),
        )

        self.logger.debug(f"exiting layout with layout:\n\n {page}")

        return page

    @classmethod
    def serve(cls, inputs: Any, outputs: Any, session: Any) -> None:
        cls.logger.trace("entering serve")
        cls.logger.trace(f"inputs={inputs}")
        cls.logger.trace(f"outputs={outputs}")
        cls.logger.trace(f"session={session}")

        @outputs(id="label_greeting")
        @render.text
        def render_label_greeting() -> str:
            cls.logger.trace("entering render_label_greeting")

            name = inputs.input_name()
            message = "Hello, stranger"

            if name:
                message = f"Hello, {name}"

            cls.logger.debug(f"greeting name={name}")
            cls.logger.trace("exiting render_label_greeting")

            return message

        cls.logger.trace("exiting serve")


app = HelloWorldApplication()


def main():
    app.run(log_config="logging.yaml")


if __name__ == "__main__":
    main()
