import matplotlib.pyplot as plt
import numpy as np
from shiny import reactive, render, ui

from energy import state
from energy.controllers.billing import (
    consumption_breakdown,
    daily_cost_eur,
    hours_over_peak,
)
from energy.controllers.simulation import CALC_MODES, hourly_consumption_by_category, simulate_day, suggest_moveable_shifts


def panel():
    return ui.nav_panel(
        "Home",
        ui.h4(f"Tomorrow: {state.SIM_DATE.isoformat()}"),
        ui.input_select("calc_mode", "Calculation model:", choices=CALC_MODES, selected="greedy"),
        ui.input_numeric(
            "start_soc_kwh",
            "Starting battery SoC (kWh):",
            value=0.0,
            min=0.0,
            step=0.5,
        ),
        ui.output_plot("home_plot", height="500px"),
        ui.output_text("home_cost_summary"),
        ui.output_text("home_shift_hints"),
        ui.h5("Consumption by category (100 % per hour)"),
        ui.output_plot("home_category_plot", height="350px"),
    )


def setup(inputs, outputs, session, refresh):

    @reactive.calc
    def simulation():
        refresh.get()
        start_soc = inputs.start_soc_kwh()
        start_value = float(start_soc) if start_soc is not None else 0.0
        mode = inputs.calc_mode() or "greedy"

        return simulate_day(state.SIM_DATE, start_soc_kwh=start_value, mode=mode)

    @render.plot
    def home_plot():
        result = simulation()
        from_panels, from_battery, from_grid_paid, from_grid_credited = consumption_breakdown(
            result.consumption_wh,
            result.production_wh,
            result.battery_to_load_wh,
            state.SIM_DATE.isoformat(),
        )
        total_capacity_kwh = sum(count * b.capacity_kwh for count, b in state.house.batteries)
        mode_label = CALC_MODES.get(inputs.calc_mode() or "greedy", "")

        hours_arr = np.arange(24)
        width = 0.4
        left = hours_arr - width / 2
        right = hours_arr + width / 2

        fig, ax1 = plt.subplots(figsize=(11, 5))

        bottom = np.zeros(24)
        ax1.bar(left, from_panels, width=width, bottom=bottom, color="tab:green", label="Cons.: panels")
        bottom = bottom + np.array(from_panels)
        ax1.bar(left, from_battery, width=width, bottom=bottom, color="tab:orange", label="Cons.: battery")
        bottom = bottom + np.array(from_battery)
        ax1.bar(left, from_grid_paid, width=width, bottom=bottom, color="tab:red", label="Cons.: grid (price ≥ 0)")
        bottom = bottom + np.array(from_grid_paid)
        ax1.bar(left, from_grid_credited, width=width, bottom=bottom, color="tab:blue", label="Cons.: grid (price < 0)")

        ax1.bar(right, result.production_wh, width=width, color="gold", edgecolor="goldenrod", label="Production (sun)")

        ax1.axhline(
            state.peak_kw_for(state.SIM_DATE) * 1000,
            color="black",
            linestyle=":",
            linewidth=1,
            label=f"Peak limit ({state.peak_kw_for(state.SIM_DATE)} kW)",
        )

        ax1.set_xlabel("Hour")
        ax1.set_ylabel("Energy (Wh)")
        ax1.set_xticks(hours_arr)
        ax1.grid(True, axis="y", alpha=0.3)
        ax1.legend(loc="upper left", fontsize=8)
        ax1.set_title(
            f"{state.SIM_DATE.isoformat()} — {mode_label}\n"
            f"battery: {result.soc_kwh[0]:.1f} kWh start → {result.end_soc_kwh:.1f} / {total_capacity_kwh:.1f} kWh end"
        )

        ax2 = ax1.twinx()
        ax2.plot(hours_arr, result.soc_kwh, marker="s", color="tab:olive", linestyle="--", label="Battery SoC (kWh)")
        ax2.set_ylabel("Battery SoC (kWh)")
        ax2.set_ylim(0, total_capacity_kwh * 1.05 if total_capacity_kwh else 1)
        ax2.legend(loc="upper right", fontsize=8)

        return fig

    @render.text
    def home_cost_summary():
        result = simulation()
        grid_flow = result.grid_flow_wh
        import_eur, export_eur, net_eur = daily_cost_eur(state.SIM_DATE.isoformat(), grid_flow)
        import_kwh = sum(-g for g in grid_flow if g < 0) / 1000
        export_kwh = sum(g for g in grid_flow if g > 0) / 1000
        peak_hours = hours_over_peak(grid_flow, state.peak_kw_for(state.SIM_DATE))
        ev_kwh = sum(result.ev_charge_wh) / 1000

        peak_warning = f"    ⚠ peak breached at h={','.join(str(h) for h in peak_hours)}" if peak_hours else "    ✓ peak ≤ limit all day"

        ev_line = ""
        if state.house.electric_cars:
            ev = state.house.electric_cars[0]
            end_soc = ev.current_soc_kwh + ev_kwh
            ev_line = (
                f"\nEV: {ev_kwh:.1f} kWh charged → ends at {end_soc:.1f}/{ev.target_soc_kwh:.0f} kWh "
                f"(min {ev.min_soc_kwh:.0f}, target {ev.target_soc_kwh:.0f})"
            )

            if end_soc < ev.min_soc_kwh - 0.1:
                ev_line += f"    ⚠ below minimum by {ev.min_soc_kwh - end_soc:.1f} kWh"

        scenarios_line = (
            f"\nN={result.n_scenarios} perturbed scenarios: "
            f"cost mean €{result.cost_mean_eur:+.2f}, range [€{result.cost_min_eur:+.2f}, €{result.cost_max_eur:+.2f}]"
            if result.n_scenarios > 1
            else ""
        )

        return (
            f"Grid import: {import_kwh:.2f} kWh → €{import_eur:.2f}    "
            f"|    Grid export: {export_kwh:.2f} kWh → €{export_eur:.2f}    "
            f"|    Net cost: €{net_eur:+.2f}"
            f"{peak_warning}"
            f"{ev_line}"
            f"{scenarios_line}"
        )

    @render.plot
    def home_category_plot():
        refresh.get()
        per_cat = hourly_consumption_by_category(state.SIM_DATE)

        if not per_cat:
            fig, ax = plt.subplots(figsize=(11, 3))
            ax.set_title("No consumption data")
            return fig

        hours_arr = np.arange(24)
        totals = np.array([sum(values[h] for values in per_cat.values()) for h in range(24)])
        safe_totals = np.where(totals > 0, totals, 1.0)

        palette = {
            "Kitchen": "tab:red",
            "Household": "tab:blue",
            "Entertainment": "tab:purple",
            "Office": "tab:green",
            "Lighting": "gold",
            "Network": "tab:gray",
            "Other": "tab:brown",
        }

        fig, ax = plt.subplots(figsize=(11, 3.5))
        bottom = np.zeros(24)

        for category in sorted(per_cat.keys()):
            values = np.array(per_cat[category])
            pct = (values / safe_totals) * 100
            ax.bar(hours_arr, pct, bottom=bottom, color=palette.get(category, "tab:cyan"), label=category)
            bottom = bottom + pct

        ax.set_xlabel("Hour")
        ax.set_ylabel("Share (%)")
        ax.set_xticks(hours_arr)
        ax.set_ylim(0, 100)
        ax.grid(True, axis="y", alpha=0.3)
        ax.legend(loc="upper left", fontsize=8, ncol=4)

        return fig

    @render.text
    def home_shift_hints():
        refresh.get()

        try:
            suggestions = suggest_moveable_shifts(state.SIM_DATE, start_soc_kwh=0.0, max_suggestions=3)
        except Exception:
            return ""

        if not suggestions:
            return "✓ No cheaper time slot found for the moveable loads."

        lines = ["💡 Shift suggestions for moveable loads:"]

        for s in suggestions:
            lines.append(
                f"   • move '{s['device']}' from {s['original_hour']:02d}:00 → {s['new_hour']:02d}:00, save €{s['savings_eur']:.2f}"
            )

        return "\n".join(lines)
