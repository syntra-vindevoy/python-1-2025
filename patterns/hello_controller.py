from shiny import reactive, render

from shiny_controller import ShinyController


class HelloController(ShinyController):
    def __call__(self, inputs, outputs, session):
        @render.text
        @reactive.event(inputs.greet)
        def greeting():
            name = inputs.name().strip()

            if name:
                return f"hello {name}"

            return "hello stranger"
