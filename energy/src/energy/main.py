from shiny import App, reactive, ui

from energy import state
from energy.views import base_tables, home, production_by_date

app_ui = ui.page_navbar(
    home.panel(),
    production_by_date.panel(),
    base_tables.panel(),
    title=state.house.address,
)


def server(inputs, outputs, session):
    refresh = reactive.value(0)

    home.setup(inputs, outputs, session, refresh)
    production_by_date.setup(inputs, outputs, session, refresh)
    base_tables.setup(inputs, outputs, session, refresh)


app = App(app_ui, server)
