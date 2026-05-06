from shiny import ui

from shiny_view import ShinyView


class HelloView(ShinyView):
    def __call__(self):
        return ui.page_fluid(
            ui.input_text("name", "Your name"),
            ui.input_action_button("greet", "Greet"),
            ui.output_text("greeting"),
        )
