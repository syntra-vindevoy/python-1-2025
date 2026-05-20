from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

import numpy as np
from scipy.optimize import linprog

from energy import state
from energy.models.appliances import ApplianceType
from energy.models.electric_cars import available_hours

CALC_MODES = {
    "greedy": "Greedy — store first, export the rest (peak-capped)",
    "linear": "Linear — LP optimum on deterministic forecast",
    "stochastic": "Stochastic — LP over perturbed forecast scenarios",
}

STOCHASTIC_SCENARIOS = 10
PRODUCTION_PERTURB = (0.85, 1.15)
PRICE_PERTURB = (0.95, 1.10)


@dataclass(slots=True)
class DayResult:
    consumption_wh: list[float] = field(default_factory=list)
    production_wh: list[float] = field(default_factory=list)
    soc_kwh: list[float] = field(default_factory=list)
    end_soc_kwh: float = 0.0
    grid_flow_wh: list[float] = field(default_factory=list)
    battery_to_load_wh: list[float] = field(default_factory=list)
    ev_charge_wh: list[float] = field(default_factory=list)
    ev_end_soc_kwh: float = 0.0
    cost_mean_eur: float = 0.0
    cost_min_eur: float = 0.0
    cost_max_eur: float = 0.0
    n_scenarios: int = 1


def overlap_seconds(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> float:
    return max(0.0, (min(a_end, b_end) - max(a_start, b_start)).total_seconds())


def hourly_consumption(target: date, schedule_entries=None) -> list[float]:
    if schedule_entries is None:
        schedule_entries = state.schedule.all()

    baseline = sum(a.consumption_wh for a in state.house.appliances if a.type == ApplianceType.ALWAYS_ON)
    light_w = sum(a.consumption_wh for a in state.house.appliances if a.type == ApplianceType.LIGHT)

    hourly = [baseline] * 24

    for entry in schedule_entries:
        start = datetime.fromisoformat(entry.start)
        end = datetime.fromisoformat(entry.end)
        device = state.appliances.get(entry.device_id)

        for h in range(24):
            hour_start = datetime.combine(target, time(h))
            hour_end = hour_start + timedelta(hours=1)
            seconds = overlap_seconds(start, end, hour_start, hour_end)

            if seconds > 0:
                hourly[h] += device.consumption_wh * (seconds / 3600)

    wake = datetime.combine(target, state.WAKE)
    sleep = datetime.combine(target, state.SLEEP)
    sunrise = datetime.combine(target, state.SUNRISE)
    sunset = datetime.combine(target, state.SUNSET)

    dark_intervals = []

    if wake < sunrise:
        dark_intervals.append((wake, min(sunrise, sleep)))

    if sunset < sleep:
        dark_intervals.append((max(sunset, wake), sleep))

    for h in range(24):
        hour_start = datetime.combine(target, time(h))
        hour_end = hour_start + timedelta(hours=1)

        for s, e in dark_intervals:
            seconds = overlap_seconds(s, e, hour_start, hour_end)

            if seconds > 0:
                hourly[h] += light_w * (seconds / 3600)

    return hourly


def hourly_consumption_by_category(target: date) -> dict[str, list[float]]:
    """Same hourly consumption walk as `hourly_consumption`, but bucketed by
    appliance.category so the UI can render a 100%-stacked breakdown.
    """
    categories: dict[str, list[float]] = {}

    def add(category: str, hour: int, wh: float):
        if category not in categories:
            categories[category] = [0.0] * 24
        categories[category][hour] += wh

    for appliance in state.house.appliances:
        if appliance.type == ApplianceType.ALWAYS_ON:
            for h in range(24):
                add(appliance.category, h, appliance.consumption_wh)

    for entry in state.schedule.all():
        device = state.appliances.get(entry.device_id)
        start = datetime.fromisoformat(entry.start)
        end = datetime.fromisoformat(entry.end)

        for h in range(24):
            hour_start = datetime.combine(target, time(h))
            hour_end = hour_start + timedelta(hours=1)
            seconds = overlap_seconds(start, end, hour_start, hour_end)

            if seconds > 0:
                add(device.category, h, device.consumption_wh * (seconds / 3600))

    wake = datetime.combine(target, state.WAKE)
    sleep = datetime.combine(target, state.SLEEP)
    sunrise = datetime.combine(target, state.SUNRISE)
    sunset = datetime.combine(target, state.SUNSET)

    dark_intervals = []

    if wake < sunrise:
        dark_intervals.append((wake, min(sunrise, sleep)))

    if sunset < sleep:
        dark_intervals.append((max(sunset, wake), sleep))

    for appliance in state.house.appliances:
        if appliance.type != ApplianceType.LIGHT:
            continue

        for h in range(24):
            hour_start = datetime.combine(target, time(h))
            hour_end = hour_start + timedelta(hours=1)

            for s, e in dark_intervals:
                seconds = overlap_seconds(s, e, hour_start, hour_end)

                if seconds > 0:
                    add(appliance.category, h, appliance.consumption_wh * (seconds / 3600))

    return categories


def hourly_production(target: date) -> list[float]:
    """Stored per-panel theoretical Wh × panel count × average performance ratio."""
    panel_count = sum(count for count, _ in state.house.panels)
    avg_perf = state.house.panels[0][1].performance_ratio if state.house.panels else 1.0
    by_hour = {p.hour_start: p.production_wh for p in state.productions.for_date(target.isoformat())}

    return [by_hour.get(h, 0.0) * panel_count * avg_perf for h in range(24)]


def _battery_specs() -> tuple[float, float, float, float]:
    capacity = sum(count * b.capacity_kwh for count, b in state.house.batteries)
    power = sum(count * b.max_power_kw for count, b in state.house.batteries)
    min_soc = sum(count * b.min_soc_kwh for count, b in state.house.batteries)
    round_trip = state.house.batteries[0][1].round_trip_efficiency if state.house.batteries else 1.0

    return capacity, power, round_trip**0.5, min_soc


def _resolve_start_soc(target: date, start_soc_kwh: float | None, capacity: float, min_soc: float = 0.0) -> float:
    if start_soc_kwh is None:
        prev_date = (target - timedelta(days=1)).isoformat()
        start_soc_kwh = state.battery_states.end_soc_for(prev_date)

    return max(min_soc, min(capacity, start_soc_kwh))


def _greedy_ev_schedule(
    target: date,
    ev_min_kwh: float,
    ev_target_kwh: float,
    ev_max_kw: float,
    peak_kw: float,
    ev_hours: list[int],
) -> list[float]:
    """Two-phase EV scheduler.

    Phase 1: must hit `ev_min_kwh` — uses cheapest hours at full ev_max_kw,
             ignoring peak (Belgian peak is a soft contractual target, but the
             minimum charge is hard: the car must be drivable in the morning).
    Phase 2: tries to top up toward `ev_target_kwh` — respects peak so this
             top-up doesn't trigger the capaciteitstarief surcharge.
    """
    if not ev_hours or ev_target_kwh <= 0:
        return [0.0] * 24

    tariffs_by_hour = {t.hour_start: t for t in state.tariffs.for_date(target.isoformat())}
    sorted_hours = sorted(
        ev_hours,
        key=lambda h: tariffs_by_hour[h].import_price_eur_per_kwh if h in tariffs_by_hour else 1.0,
    )

    schedule = [0.0] * 24

    remaining = ev_min_kwh

    for h in sorted_hours:
        if remaining <= 0:
            break

        slot = min(ev_max_kw, remaining)
        schedule[h] = slot
        remaining -= slot

    extra = max(0.0, ev_target_kwh - ev_min_kwh)

    for h in sorted_hours:
        if extra <= 0:
            break

        current = schedule[h]
        room_under_peak = max(0.0, peak_kw - current)
        room_under_ev_rate = max(0.0, ev_max_kw - current)
        slot = min(extra, room_under_peak, room_under_ev_rate)

        if slot > 0:
            schedule[h] += slot
            extra -= slot

    return schedule


def simulate_day_greedy(target: date, start_soc_kwh: float | None = None) -> DayResult:
    """Model 1 — produce → use → store → spill to grid; deficit drawn from
    battery, then from grid but never above PEAK_KW per hour. EV (if any) is
    pre-allocated to the cheapest grid hours within its charge window."""
    consumption = hourly_consumption(target)
    production = hourly_production(target)

    capacity_kwh, max_power_kw, one_way_eff, battery_min_soc = _battery_specs()
    soc_kwh = _resolve_start_soc(target, start_soc_kwh, capacity_kwh, battery_min_soc)
    peak_kw = state.peak_kw_for(target)

    ev = state.house.electric_cars[0] if state.house.electric_cars else None
    ev_min_need_kwh = max(0.0, ev.min_soc_kwh - ev.current_soc_kwh) if ev else 0.0
    ev_target_kwh = max(0.0, ev.target_soc_kwh - ev.current_soc_kwh) if ev else 0.0
    ev_hours = available_hours(ev.charge_start_hour, ev.charge_end_hour) if ev else []
    ev_schedule = _greedy_ev_schedule(
        target,
        ev_min_need_kwh,
        ev_target_kwh,
        ev.max_charge_kw if ev else 0.0,
        peak_kw,
        ev_hours,
    )

    result = DayResult()
    max_hourly_kwh = max_power_kw

    for h in range(24):
        net_kwh = (production[h] - consumption[h]) / 1000

        grid_kwh = 0.0
        from_battery_kwh = 0.0

        if net_kwh > 0:
            max_in = min(net_kwh, max_hourly_kwh)
            potentially_stored = max_in * one_way_eff
            room = capacity_kwh - soc_kwh
            actually_stored = min(potentially_stored, room)
            consumed_by_charging = actually_stored / one_way_eff if one_way_eff > 0 else 0.0
            soc_kwh += actually_stored
            grid_kwh = net_kwh - consumed_by_charging
        elif net_kwh < 0:
            need = -net_kwh
            max_out = min(need, max_hourly_kwh)
            potentially_drawn = max_out / one_way_eff if one_way_eff > 0 else float("inf")
            # Respect the battery's reserve floor (battery_min_soc).
            available_for_discharge = max(0.0, soc_kwh - battery_min_soc)
            actually_drawn = min(potentially_drawn, available_for_discharge)
            delivered = actually_drawn * one_way_eff
            soc_kwh -= actually_drawn
            from_battery_kwh = delivered

            remaining = need - delivered
            grid_import = min(remaining, peak_kw)
            grid_kwh = -grid_import

        # Minimum EV charge is non-negotiable, so the pre-allocated schedule
        # is delivered as-is — even if that pushes total grid import above
        # peak. The schedule itself already balanced "must reach min" against
        # "stay under peak for the optional top-up to target", so any over-peak
        # hour here is the cost of guaranteeing the morning charge.
        ev_kwh = ev_schedule[h]

        if ev_kwh > 0:
            grid_kwh -= ev_kwh

        result.soc_kwh.append(soc_kwh)
        result.grid_flow_wh.append(grid_kwh * 1000)
        result.battery_to_load_wh.append(from_battery_kwh * 1000)
        result.ev_charge_wh.append(ev_kwh * 1000)

    result.consumption_wh = consumption
    result.production_wh = production
    result.end_soc_kwh = result.soc_kwh[-1] if result.soc_kwh else 0.0
    result.ev_end_soc_kwh = (ev.current_soc_kwh + sum(ev_schedule)) if ev else 0.0

    state.battery_states.upsert(target.isoformat(), round(result.end_soc_kwh, 3))
    state.battery_states.save()

    return result


def _solve_linear_lp(
    consumption: list[float],
    production: list[float],
    import_p: list[float],
    export_p: list[float],
    start_soc_kwh: float,
    capacity_kwh: float,
    max_power_kw: float,
    one_way_eff: float,
    battery_min_soc_kwh: float,
    ev_min_kwh: float,
    ev_max_kwh: float,
    ev_window: set[int],
    ev_max_kw: float,
    peak_kw: float,
) -> DayResult:
    """Core LP solver. Inputs are plain lists / numbers so callers can feed
    perturbed forecasts without depending on global state.
    """
    cons_kwh = [c / 1000 for c in consumption]
    prod_kwh = [p / 1000 for p in production]

    offsets = {
        "s2l": 0,
        "s2b": 1,
        "s2g": 2,
        "b2l": 3,
        "b2g": 4,
        "g2l": 5,
        "g2b": 6,
        "s2c": 7,
        "b2c": 8,
        "g2c": 9,
    }
    N = 10 * 24

    def idx(name, h):
        return offsets[name] * 24 + h

    c = np.zeros(N)

    for h in range(24):
        c[idx("g2l", h)] = import_p[h]
        c[idx("g2b", h)] = import_p[h]
        c[idx("g2c", h)] = import_p[h]
        c[idx("s2g", h)] = -export_p[h]
        c[idx("b2g", h)] = -export_p[h]

    A_eq, b_eq = [], []

    for h in range(24):
        row = np.zeros(N)
        row[idx("s2l", h)] = 1
        row[idx("s2b", h)] = 1
        row[idx("s2g", h)] = 1
        row[idx("s2c", h)] = 1
        A_eq.append(row)
        b_eq.append(prod_kwh[h])

        row = np.zeros(N)
        row[idx("s2l", h)] = 1
        row[idx("b2l", h)] = 1
        row[idx("g2l", h)] = 1
        A_eq.append(row)
        b_eq.append(cons_kwh[h])

    A_ub, b_ub = [], []

    if ev_max_kwh > 0:
        # Upper bound (≤ ev_max_kwh): ev_total ≤ target − current
        row = np.zeros(N)
        for h in range(24):
            row[idx("s2c", h)] = 1
            row[idx("b2c", h)] = 1
            row[idx("g2c", h)] = 1
        A_ub.append(row)
        b_ub.append(ev_max_kwh)

    if ev_min_kwh > 0:
        # Lower bound (≥ ev_min_kwh): −ev_total ≤ −ev_min_kwh
        row = np.zeros(N)
        for h in range(24):
            row[idx("s2c", h)] = -1
            row[idx("b2c", h)] = -1
            row[idx("g2c", h)] = -1
        A_ub.append(row)
        b_ub.append(-ev_min_kwh)

    for h in range(24):
        row = np.zeros(N)
        row[idx("s2b", h)] = 1
        row[idx("g2b", h)] = 1
        A_ub.append(row)
        b_ub.append(max_power_kw)

        row = np.zeros(N)
        row[idx("b2l", h)] = 1
        row[idx("b2g", h)] = 1
        row[idx("b2c", h)] = 1
        A_ub.append(row)
        b_ub.append(max_power_kw)

        row = np.zeros(N)
        row[idx("g2l", h)] = 1
        row[idx("g2b", h)] = 1
        row[idx("g2c", h)] = 1
        A_ub.append(row)
        b_ub.append(peak_kw)

        row = np.zeros(N)
        row[idx("s2c", h)] = 1
        row[idx("b2c", h)] = 1
        row[idx("g2c", h)] = 1
        A_ub.append(row)
        b_ub.append(ev_max_kw if h in ev_window else 0.0)

    for h in range(24):
        row = np.zeros(N)

        for k in range(h + 1):
            row[idx("s2b", k)] = one_way_eff
            row[idx("g2b", k)] = one_way_eff
            row[idx("b2l", k)] = -1 / one_way_eff
            row[idx("b2g", k)] = -1 / one_way_eff
            row[idx("b2c", k)] = -1 / one_way_eff

        A_ub.append(row)
        b_ub.append(capacity_kwh - start_soc_kwh)
        A_ub.append(-row)
        b_ub.append(start_soc_kwh - battery_min_soc_kwh)

    bounds = [(0, None)] * N
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"LP failed: {res.message}")

    x = res.x
    result = DayResult()
    soc = start_soc_kwh

    for h in range(24):
        s2b = x[idx("s2b", h)]
        g2b = x[idx("g2b", h)]
        b2l = x[idx("b2l", h)]
        b2g = x[idx("b2g", h)]
        b2c = x[idx("b2c", h)]
        s2g = x[idx("s2g", h)]
        g2l = x[idx("g2l", h)]
        s2c = x[idx("s2c", h)]
        g2c = x[idx("g2c", h)]

        soc += one_way_eff * (s2b + g2b) - (b2l + b2g + b2c) / one_way_eff
        soc = max(0.0, min(capacity_kwh, soc))
        result.soc_kwh.append(soc)
        result.grid_flow_wh.append(((s2g + b2g) - (g2l + g2b + g2c)) * 1000)
        result.battery_to_load_wh.append(b2l * 1000)
        result.ev_charge_wh.append((s2c + b2c + g2c) * 1000)

    result.consumption_wh = consumption
    result.production_wh = production
    result.end_soc_kwh = result.soc_kwh[-1] if result.soc_kwh else 0.0
    result.cost_mean_eur = float(res.fun)
    result.cost_min_eur = float(res.fun)
    result.cost_max_eur = float(res.fun)

    return result


def _lp_inputs_for(target: date, start_soc_kwh: float | None, schedule_entries=None):
    consumption = hourly_consumption(target, schedule_entries=schedule_entries)
    production = hourly_production(target)

    tariffs_by_hour = {t.hour_start: t for t in state.tariffs.for_date(target.isoformat())}
    import_p = [tariffs_by_hour[h].import_price_eur_per_kwh if h in tariffs_by_hour else 1.0 for h in range(24)]
    export_p = [tariffs_by_hour[h].export_price_eur_per_kwh if h in tariffs_by_hour else 0.0 for h in range(24)]

    capacity_kwh, max_power_kw, one_way_eff, battery_min_soc = _battery_specs()
    start = _resolve_start_soc(target, start_soc_kwh, capacity_kwh, battery_min_soc)

    ev = state.house.electric_cars[0] if state.house.electric_cars else None
    ev_min_kwh = max(0.0, ev.min_soc_kwh - ev.current_soc_kwh) if ev else 0.0
    ev_max_kwh = max(0.0, ev.target_soc_kwh - ev.current_soc_kwh) if ev else 0.0
    ev_window = set(available_hours(ev.charge_start_hour, ev.charge_end_hour)) if ev else set()
    ev_max_kw = ev.max_charge_kw if ev else 0.0
    peak_kw = state.peak_kw_for(target)

    return {
        "consumption": consumption,
        "production": production,
        "import_p": import_p,
        "export_p": export_p,
        "start_soc_kwh": start,
        "capacity_kwh": capacity_kwh,
        "max_power_kw": max_power_kw,
        "one_way_eff": one_way_eff,
        "battery_min_soc_kwh": battery_min_soc,
        "ev_min_kwh": ev_min_kwh,
        "ev_max_kwh": ev_max_kwh,
        "ev_window": ev_window,
        "ev_max_kw": ev_max_kw,
        "peak_kw": peak_kw,
        "ev": ev,
    }


def simulate_day_linear(target: date, start_soc_kwh: float | None = None) -> DayResult:
    """Model 2 — deterministic linear program over today's forecast."""
    inputs = _lp_inputs_for(target, start_soc_kwh)
    ev = inputs.pop("ev")
    result = _solve_linear_lp(**inputs)

    if ev is not None:
        result.ev_end_soc_kwh = ev.current_soc_kwh + sum(result.ev_charge_wh) / 1000

    state.battery_states.upsert(target.isoformat(), round(result.end_soc_kwh, 3))
    state.battery_states.save()

    return result


def simulate_day_stochastic(
    target: date,
    start_soc_kwh: float | None = None,
    n_scenarios: int = STOCHASTIC_SCENARIOS,
    seed: int = 42,
) -> DayResult:
    """Model 3 — solve the linear LP for N perturbed forecast scenarios and
    return the mean dispatch plus the cost distribution.

    Each scenario multiplies hourly production by U(0.85, 1.15) (weather
    forecast noise) and hourly import/export prices by U(0.95, 1.10) (spot
    price noise). The fields cost_mean / cost_min / cost_max / n_scenarios on
    DayResult expose the resulting cost spread.
    """
    inputs = _lp_inputs_for(target, start_soc_kwh)
    ev = inputs.pop("ev")
    rng = np.random.default_rng(seed)

    base_production = np.array(inputs["production"])
    base_import = np.array(inputs["import_p"])
    base_export = np.array(inputs["export_p"])

    agg_soc = np.zeros(24)
    agg_grid = np.zeros(24)
    agg_b2l = np.zeros(24)
    agg_ev = np.zeros(24)
    agg_end_soc = 0.0
    costs = []

    for _ in range(n_scenarios):
        prod = (base_production * rng.uniform(*PRODUCTION_PERTURB, size=24)).tolist()
        imp = (base_import * rng.uniform(*PRICE_PERTURB, size=24)).tolist()
        exp = (base_export * rng.uniform(*PRICE_PERTURB, size=24)).tolist()

        scenario_result = _solve_linear_lp(
            consumption=inputs["consumption"],
            production=prod,
            import_p=imp,
            export_p=exp,
            start_soc_kwh=inputs["start_soc_kwh"],
            capacity_kwh=inputs["capacity_kwh"],
            max_power_kw=inputs["max_power_kw"],
            one_way_eff=inputs["one_way_eff"],
            battery_min_soc_kwh=inputs["battery_min_soc_kwh"],
            ev_min_kwh=inputs["ev_min_kwh"],
            ev_max_kwh=inputs["ev_max_kwh"],
            ev_window=inputs["ev_window"],
            ev_max_kw=inputs["ev_max_kw"],
            peak_kw=inputs["peak_kw"],
        )

        agg_soc += np.array(scenario_result.soc_kwh)
        agg_grid += np.array(scenario_result.grid_flow_wh)
        agg_b2l += np.array(scenario_result.battery_to_load_wh)
        agg_ev += np.array(scenario_result.ev_charge_wh)
        agg_end_soc += scenario_result.end_soc_kwh
        costs.append(scenario_result.cost_mean_eur)

    result = DayResult()
    result.consumption_wh = inputs["consumption"]
    result.production_wh = inputs["production"]
    result.soc_kwh = (agg_soc / n_scenarios).tolist()
    result.grid_flow_wh = (agg_grid / n_scenarios).tolist()
    result.battery_to_load_wh = (agg_b2l / n_scenarios).tolist()
    result.ev_charge_wh = (agg_ev / n_scenarios).tolist()
    result.end_soc_kwh = agg_end_soc / n_scenarios
    result.ev_end_soc_kwh = (ev.current_soc_kwh + sum(result.ev_charge_wh) / 1000) if ev else 0.0
    result.cost_mean_eur = float(np.mean(costs))
    result.cost_min_eur = float(np.min(costs))
    result.cost_max_eur = float(np.max(costs))
    result.n_scenarios = n_scenarios

    state.battery_states.upsert(target.isoformat(), round(result.end_soc_kwh, 3))
    state.battery_states.save()

    return result


def _shifted_schedule(original_entries, target_entry, shift_hours):
    shifted = []

    for e in original_entries:
        if e.rec_id == target_entry.rec_id:
            new_start = (datetime.fromisoformat(e.start) + timedelta(hours=shift_hours)).isoformat()
            new_end = (datetime.fromisoformat(e.end) + timedelta(hours=shift_hours)).isoformat()
            shifted.append(type(e)(rec_id=e.rec_id, device_id=e.device_id, start=new_start, end=new_end, moveable=e.moveable))
        else:
            shifted.append(e)

    return shifted


def suggest_moveable_shifts(target: date, start_soc_kwh: float | None = None, max_suggestions: int = 3) -> list[dict]:
    """Try shifting each moveable schedule entry by ±2/4/6 hours, re-solve the
    LP, and return shifts that save money. Sorted by savings, top N returned."""
    from energy.controllers.billing import daily_cost_eur

    base_inputs = _lp_inputs_for(target, start_soc_kwh)
    base_inputs.pop("ev")
    base_result = _solve_linear_lp(**base_inputs)
    _, _, baseline_net = daily_cost_eur(target.isoformat(), base_result.grid_flow_wh)

    suggestions = []
    original_entries = list(state.schedule.all())

    for entry in original_entries:
        if not entry.moveable:
            continue

        device = state.appliances.get(entry.device_id)
        best_for_entry = None

        for shift_h in (-4, -3, -2, -1, 1, 2, 3, 4):
            try:
                shifted = _shifted_schedule(original_entries, entry, shift_h)
                inputs = _lp_inputs_for(target, start_soc_kwh, schedule_entries=shifted)
                inputs.pop("ev")
                shifted_result = _solve_linear_lp(**inputs)
                _, _, shifted_net = daily_cost_eur(target.isoformat(), shifted_result.grid_flow_wh)
                savings = baseline_net - shifted_net

                if savings > 0.01 and (best_for_entry is None or savings > best_for_entry["savings_eur"]):
                    original_hour = datetime.fromisoformat(entry.start).hour
                    new_hour = (original_hour + shift_h) % 24
                    best_for_entry = {
                        "device": device.name,
                        "original_hour": original_hour,
                        "new_hour": new_hour,
                        "shift_hours": shift_h,
                        "savings_eur": savings,
                    }
            except RuntimeError:
                continue

        if best_for_entry is not None:
            suggestions.append(best_for_entry)

    suggestions.sort(key=lambda s: -s["savings_eur"])

    return suggestions[:max_suggestions]


def simulate_day(target: date, start_soc_kwh: float | None = None, mode: str = "greedy") -> DayResult:
    if mode == "stochastic":
        return simulate_day_stochastic(target, start_soc_kwh)

    if mode == "linear":
        return simulate_day_linear(target, start_soc_kwh)

    return simulate_day_greedy(target, start_soc_kwh)
