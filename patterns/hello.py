from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_text("name", "Your name"),
    ui.input_action_button("greet", "Greet"),
    ui.output_text("greeting"),
)


def server(inputs, outputs, session):
    @render.text
    @reactive.event(inputs.greet)
    def greeting():
        name = inputs.name().strip()

        if name:
            return f"hello {name}"

        return "hello stranger"


app = App(app_ui, server)