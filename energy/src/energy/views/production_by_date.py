from dataclasses import asdict

import matplotlib.pyplot as plt
import pandas as pd
from shiny import reactive, render, ui

from energy import state
from energy.controllers.api import fetch_production
from energy.views.helpers import display


def panel():
    return ui.nav_panel(
        "Production by date",
        ui.input_date("production_date", "Date:", value=state.SIM_DATE.isoformat()),
        ui.input_action_button("fetch_btn", "Fetch from open-meteo"),
        ui.output_text("fetch_status"),
        ui.layout_columns(
            ui.output_data_frame("production_by_date_table"),
            ui.output_plot("production_by_date_plot", height="400px"),
            col_widths=[6, 6],
        ),
    )


def setup(inputs, outputs, session, refresh):

    fetch_message = reactive.value("")

    @reactive.effect
    @reactive.event(inputs.fetch_btn)
    def _fetch():
        target = inputs.production_date()

        if target is None:
            fetch_message.set("Pick a date first.")
            return

        try:
            dates = fetch_production(target)
            fetch_message.set(
                f"Refreshed {len(dates)} days of production: {dates[0]} → {dates[-1]} "
                f"(any previously stored rows for those dates were overwritten)."
            )
            refresh.set(refresh.get() + 1)
        except Exception as exc:
            fetch_message.set(f"Fetch failed: {exc}")

    @render.text
    def fetch_status():
        return fetch_message.get()

    @render.plot
    def production_by_date_plot():
        refresh.get()
        target = inputs.production_date()

        fig, ax = plt.subplots(figsize=(8, 5))

        if target is None:
            ax.set_title("Pick a date.")
            return fig

        entries = state.productions.for_date(target.isoformat())

        if not entries:
            ax.set_title(f"No data for {target.isoformat()}. Click Fetch.")
        else:
            hours = [p.hour_start for p in entries]
            values = [p.production_wh for p in entries]

            ax.plot(hours, values, marker="o", color="tab:orange")
            ax.set_title(f"Production per panel — {target.isoformat()}")

        ax.set_xlabel("Hour")
        ax.set_ylabel("Wh per panel")
        ax.grid(True, alpha=0.3)

        return fig

    @render.data_frame
    def production_by_date_table():
        refresh.get()
        target = inputs.production_date()

        if target is None:
            return pd.DataFrame()

        rows = [asdict(p) for p in state.productions.for_date(target.isoformat())]

        return display(pd.DataFrame(rows))
