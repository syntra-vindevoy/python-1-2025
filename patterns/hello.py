from shiny import reactive, render, ui

from shiny_application import ShinyApplication


class HelloApplication(ShinyApplication):
    def layout(self):
        return ui.page_fluid(
            ui.input_text("name", "Your name"),
            ui.input_action_button("greet", "Greet"),
            ui.output_text("greeting"),
        )

    def server(self, inputs, outputs, session):
        @render.text
        @reactive.event(inputs.greet)
        def greeting():
            name = inputs.name().strip()

            if name:
                return f"hello {name}"

            return "hello stranger"


if __name__ == "__main__":
    HelloApplication().run()