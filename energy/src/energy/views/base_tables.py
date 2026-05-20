from shiny import reactive, render, ui

from energy import state
from energy.models.appliances import TYPE_LABELS, Appliance, ApplianceType
from energy.models.batteries import Battery
from energy.models.battery_states import BatteryState
from energy.models.electric_cars import ElectricCar
from energy.models.meter_readings import MeterReading
from energy.models.peak_consumptions import PeakConsumption
from energy.models.productions import Production
from energy.models.schedule import ScheduleEntry
from energy.models.solar_panels import SolarPanel
from energy.models.tariffs import Tariff
from energy.views.helpers import display


def _modal_fields(table: str, row: dict | None):
    row = row or {}

    if table == "Devices":
        return [
            ui.input_text("mf_name", "Name", value=str(row.get("name", ""))),
            ui.input_select(
                "mf_type",
                "Type",
                choices={t.value: TYPE_LABELS[t.value] for t in ApplianceType},
                selected=str(row.get("type", ApplianceType.ALWAYS_ON.value)),
            ),
            ui.input_numeric("mf_consumption_wh", "Consumption (Wh)", value=float(row.get("consumption_wh", 0) or 0)),
            ui.input_text("mf_category", "Category", value=str(row.get("category", "Other") or "Other")),
        ]

    if table == "Solar panels":
        return [
            ui.input_text("mf_brand", "Brand", value=str(row.get("brand", ""))),
            ui.input_numeric("mf_capacity_wp", "Capacity (Wp)", value=float(row.get("capacity_wp", 0) or 0)),
            ui.input_numeric(
                "mf_performance_ratio",
                "Performance ratio (0..1)",
                value=float(row.get("performance_ratio", 0.85) or 0.85),
                min=0.0,
                max=1.0,
                step=0.01,
            ),
        ]

    if table == "Batteries":
        return [
            ui.input_text("mf_brand", "Brand", value=str(row.get("brand", ""))),
            ui.input_numeric("mf_capacity_kwh", "Capacity (kWh)", value=float(row.get("capacity_kwh", 0) or 0)),
            ui.input_numeric("mf_max_power_kw", "Max power (kW)", value=float(row.get("max_power_kw", 5.0) or 5.0)),
            ui.input_numeric(
                "mf_round_trip_efficiency",
                "Round-trip efficiency (0..1)",
                value=float(row.get("round_trip_efficiency", 0.9) or 0.9),
                min=0.0,
                max=1.0,
                step=0.01,
            ),
            ui.input_numeric("mf_min_soc_kwh", "Min SoC (kWh)", value=float(row.get("min_soc_kwh", 0) or 0), min=0.0, step=0.1),
        ]

    if table == "Production":
        return [
            ui.input_text("mf_date", "Date (YYYY-MM-DD)", value=str(row.get("date", ""))),
            ui.input_numeric("mf_hour_start", "Hour start", value=int(row.get("hour_start", 0) or 0)),
            ui.input_numeric("mf_hour_end", "Hour end", value=int(row.get("hour_end", 0) or 0)),
            ui.input_numeric("mf_production_wh", "Production (Wh)", value=float(row.get("production_wh", 0) or 0)),
            ui.input_numeric("mf_temperature_c", "Temperature (°C)", value=float(row.get("temperature_c", 0) or 0)),
            ui.input_numeric("mf_wind_kmh", "Wind (km/h)", value=float(row.get("wind_kmh", 0) or 0)),
            ui.input_numeric("mf_precipitation_mm", "Rain (mm)", value=float(row.get("precipitation_mm", 0) or 0)),
            ui.input_numeric("mf_humidity_pct", "Humidity (%)", value=float(row.get("humidity_pct", 0) or 0)),
        ]

    if table == "Consumption":
        return [
            ui.input_numeric("mf_device_id", "Device ID", value=int(row.get("device_id", 0) or 0)),
            ui.input_text("mf_start", "Start (ISO datetime)", value=str(row.get("start", ""))),
            ui.input_text("mf_end", "End (ISO datetime)", value=str(row.get("end", ""))),
            ui.input_checkbox("mf_moveable", "Moveable (LP may shift it to a cheaper hour)", value=bool(row.get("moveable", False))),
        ]

    if table == "Tariffs":
        return [
            ui.input_text("mf_date", "Date (YYYY-MM-DD)", value=str(row.get("date", ""))),
            ui.input_numeric("mf_hour_start", "Hour start", value=int(row.get("hour_start", 0) or 0)),
            ui.input_numeric("mf_hour_end", "Hour end", value=int(row.get("hour_end", 0) or 0)),
            ui.input_numeric("mf_import_price", "Import price (€/kWh)", value=float(row.get("import_price_eur_per_kwh", 0) or 0)),
            ui.input_numeric("mf_export_price", "Export price (€/kWh)", value=float(row.get("export_price_eur_per_kwh", 0) or 0)),
        ]

    if table == "Battery state":
        return [
            ui.input_text("mf_date", "Date (YYYY-MM-DD)", value=str(row.get("date", ""))),
            ui.input_numeric("mf_end_soc_kwh", "End-of-day SoC (kWh)", value=float(row.get("end_soc_kwh", 0) or 0)),
        ]

    if table == "Meter readings":
        return [
            ui.input_text("mf_date", "Date (YYYY-MM-DD)", value=str(row.get("date", ""))),
            ui.input_numeric("mf_hour", "Hour (0..23)", value=int(row.get("hour", 0) or 0), min=0, max=23),
            ui.input_numeric("mf_imported_kwh", "Imported (kWh)", value=float(row.get("imported_kwh", 0) or 0), min=0.0, step=0.01),
            ui.input_numeric("mf_exported_kwh", "Exported (kWh)", value=float(row.get("exported_kwh", 0) or 0), min=0.0, step=0.01),
        ]

    if table == "Electric cars":
        return [
            ui.input_text("mf_brand", "Brand", value=str(row.get("brand", ""))),
            ui.input_numeric("mf_capacity_kwh", "Capacity (kWh)", value=float(row.get("capacity_kwh", 0) or 0)),
            ui.input_numeric("mf_max_charge_kw", "Max charge (kW)", value=float(row.get("max_charge_kw", 11) or 11)),
            ui.input_numeric("mf_current_soc_kwh", "Current SoC (kWh)", value=float(row.get("current_soc_kwh", 0) or 0)),
            ui.input_numeric("mf_target_soc_kwh", "Target SoC (kWh)", value=float(row.get("target_soc_kwh", 0) or 0)),
            ui.input_numeric(
                "mf_charge_start_hour", "Window start (h, 0..23)", value=int(row.get("charge_start_hour", 18) or 18), min=0, max=23
            ),
            ui.input_numeric("mf_charge_end_hour", "Window end (h, 0..23)", value=int(row.get("charge_end_hour", 8) or 8), min=0, max=23),
        ]

    return []


def _build_modal(table: str, action: str, row: dict | None):
    return ui.modal(
        *_modal_fields(table, row),
        title=f"{action} — {table}",
        footer=ui.tags.div(
            ui.input_action_button("modal_save", "Save", class_="btn btn-primary"),
            ui.modal_button("Cancel"),
        ),
        easy_close=True,
    )


def panel():
    return ui.nav_panel(
        "Base Tables",
        ui.input_select("table_select", "Select table:", choices=list(state.TABLES.keys())),
        ui.output_data_frame("selected_table"),
        ui.tags.div(
            ui.input_action_button("add_btn", "Add", class_="btn btn-primary"),
            ui.input_action_button("edit_btn", "Edit", class_="btn btn-secondary"),
            ui.input_action_button("delete_btn", "Delete", class_="btn btn-danger"),
            style="margin-top: 12px; display: flex; gap: 8px;",
        ),
    )


def setup(inputs, outputs, session, refresh):

    modal_state = reactive.value({"action": None, "table": None, "rec_id": None})

    @render.data_frame
    def selected_table():
        refresh.get()
        choice = inputs.table_select()

        return render.DataGrid(display(state.TABLES[choice].to_dataframe()), selection_mode="row")

    @reactive.effect
    @reactive.event(inputs.add_btn)
    def _open_add():
        table = inputs.table_select()
        modal_state.set({"action": "Add", "table": table, "rec_id": None})
        ui.modal_show(_build_modal(table, "Add", None))

    @reactive.effect
    @reactive.event(inputs.edit_btn)
    def _open_edit():
        table = inputs.table_select()
        sel = selected_table.cell_selection()

        if not sel or not sel.get("rows"):
            ui.notification_show("Please select a row first.", type="warning")
            return

        full_df = state.TABLES[table].to_dataframe()
        row_data = full_df.iloc[sel["rows"][0]].to_dict()
        rec_id = int(row_data["rec_id"])

        modal_state.set({"action": "Edit", "table": table, "rec_id": rec_id})
        ui.modal_show(_build_modal(table, "Edit", row_data))

    @reactive.effect
    @reactive.event(inputs.delete_btn)
    def _open_delete():
        table = inputs.table_select()
        sel = selected_table.cell_selection()

        if not sel or not sel.get("rows"):
            ui.notification_show("Please select a row first.", type="warning")
            return

        full_df = state.TABLES[table].to_dataframe()
        rec_id = int(full_df.iloc[sel["rows"][0]]["rec_id"])

        modal_state.set({"action": "Delete", "table": table, "rec_id": rec_id})
        ui.modal_show(
            ui.modal(
                "Are you sure you want to delete this row?",
                title="Confirm delete",
                footer=ui.tags.div(
                    ui.input_action_button("modal_confirm_delete", "Delete", class_="btn btn-danger"),
                    ui.modal_button("Cancel"),
                ),
                easy_close=True,
            )
        )

    def _build_record(table: str, rec_id: int | None):
        if rec_id is None:
            rec_id = state.TABLES[table].next_rec_id()

        if table == "Devices":
            return Appliance(
                rec_id=rec_id,
                name=inputs.mf_name(),
                type=ApplianceType(inputs.mf_type()),
                consumption_wh=float(inputs.mf_consumption_wh()),
                category=inputs.mf_category(),
            )

        if table == "Solar panels":
            return SolarPanel(
                rec_id=rec_id,
                brand=inputs.mf_brand(),
                capacity_wp=float(inputs.mf_capacity_wp()),
                performance_ratio=float(inputs.mf_performance_ratio()),
            )

        if table == "Batteries":
            return Battery(
                rec_id=rec_id,
                brand=inputs.mf_brand(),
                capacity_kwh=float(inputs.mf_capacity_kwh()),
                max_power_kw=float(inputs.mf_max_power_kw()),
                round_trip_efficiency=float(inputs.mf_round_trip_efficiency()),
                min_soc_kwh=float(inputs.mf_min_soc_kwh()),
            )

        if table == "Production":
            return Production(
                rec_id=rec_id,
                date=inputs.mf_date(),
                hour_start=int(inputs.mf_hour_start()),
                hour_end=int(inputs.mf_hour_end()),
                production_wh=float(inputs.mf_production_wh()),
                temperature_c=float(inputs.mf_temperature_c()),
                wind_kmh=float(inputs.mf_wind_kmh()),
                precipitation_mm=float(inputs.mf_precipitation_mm()),
                humidity_pct=float(inputs.mf_humidity_pct()),
            )

        if table == "Consumption":
            return ScheduleEntry(
                rec_id=rec_id,
                device_id=int(inputs.mf_device_id()),
                start=inputs.mf_start(),
                end=inputs.mf_end(),
                moveable=bool(inputs.mf_moveable()),
            )

        if table == "Tariffs":
            return Tariff(
                rec_id=rec_id,
                date=inputs.mf_date(),
                hour_start=int(inputs.mf_hour_start()),
                hour_end=int(inputs.mf_hour_end()),
                import_price_eur_per_kwh=float(inputs.mf_import_price()),
                export_price_eur_per_kwh=float(inputs.mf_export_price()),
            )

        if table == "Battery state":
            return BatteryState(
                rec_id=rec_id,
                date=inputs.mf_date(),
                end_soc_kwh=float(inputs.mf_end_soc_kwh()),
            )

        if table == "Peak consumption":
            return PeakConsumption(
                rec_id=rec_id,
                valid_from=inputs.mf_valid_from(),
                valid_to=inputs.mf_valid_to(),
                peak_kw=float(inputs.mf_peak_kw()),
            )

        if table == "Meter readings":
            return MeterReading(
                rec_id=rec_id,
                date=inputs.mf_date(),
                hour=int(inputs.mf_hour()),
                imported_kwh=float(inputs.mf_imported_kwh()),
                exported_kwh=float(inputs.mf_exported_kwh()),
            )

        if table == "Electric cars":
            return ElectricCar(
                rec_id=rec_id,
                brand=inputs.mf_brand(),
                capacity_kwh=float(inputs.mf_capacity_kwh()),
                max_charge_kw=float(inputs.mf_max_charge_kw()),
                current_soc_kwh=float(inputs.mf_current_soc_kwh()),
                min_soc_kwh=float(inputs.mf_min_soc_kwh()),
                target_soc_kwh=float(inputs.mf_target_soc_kwh()),
                charge_start_hour=int(inputs.mf_charge_start_hour()),
                charge_end_hour=int(inputs.mf_charge_end_hour()),
            )

        return None

    @reactive.effect
    @reactive.event(inputs.modal_save)
    def _save_modal():
        s = modal_state.get()
        table = s["table"]
        rec_id = s["rec_id"]
        record = _build_record(table, rec_id)

        if record is None:
            ui.modal_remove()
            return

        collection = state.TABLES[table]

        if s["action"] == "Add":
            collection.add(record)
        else:
            collection.edit(rec_id, record)

        ui.modal_remove()
        refresh.set(refresh.get() + 1)

    @reactive.effect
    @reactive.event(inputs.modal_confirm_delete)
    def _confirm_delete():
        s = modal_state.get()
        state.TABLES[s["table"]].delete(s["rec_id"])
        ui.modal_remove()
        refresh.set(refresh.get() + 1)
