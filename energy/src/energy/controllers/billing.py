from energy import state


def hourly_cost_eur(date_str: str, grid_flow_wh: list[float]) -> list[float]:
    """Hourly net cost in €. Positive = paid, negative = received."""
    tariffs_by_hour = {t.hour_start: t for t in state.tariffs.for_date(date_str)}

    hourly = []

    for h in range(24):
        tariff = tariffs_by_hour.get(h)

        if tariff is None:
            hourly.append(0.0)
            continue

        kwh = grid_flow_wh[h] / 1000

        if kwh < 0:
            hourly.append(abs(kwh) * tariff.import_price_eur_per_kwh)
        else:
            hourly.append(-kwh * tariff.export_price_eur_per_kwh)

    return hourly


def consumption_breakdown(
    consumption: list[float],
    production: list[float],
    battery_to_load_wh: list[float],
    date_str: str,
) -> tuple[list[float], list[float], list[float], list[float]]:
    """Split each hour's consumption (Wh) into four sources:
    - from_panels:         direct solar covering same-hour demand
    - from_battery:        battery discharge delivered to load (post-discharge-efficiency)
    - from_grid_paid:      grid import while the hourly tariff is >= 0
    - from_grid_credited:  grid import while the hourly tariff is < 0
    """
    tariffs_by_hour = {t.hour_start: t for t in state.tariffs.for_date(date_str)}

    from_panels: list[float] = []
    from_battery: list[float] = []
    from_grid_paid: list[float] = []
    from_grid_credited: list[float] = []

    for h in range(24):
        cons = consumption[h]
        prod = production[h]

        direct = min(cons, prod)
        from_bat = min(battery_to_load_wh[h], max(0.0, cons - direct))
        grid_import = max(0.0, cons - direct - from_bat)

        tariff = tariffs_by_hour.get(h)

        if tariff is not None and tariff.import_price_eur_per_kwh < 0:
            paid = 0.0
            credited = grid_import
        else:
            paid = grid_import
            credited = 0.0

        from_panels.append(direct)
        from_battery.append(from_bat)
        from_grid_paid.append(paid)
        from_grid_credited.append(credited)

    return from_panels, from_battery, from_grid_paid, from_grid_credited


def hours_over_peak(grid_flow_wh: list[float], peak_kw: float) -> list[int]:
    """Hours whose grid import (kW) exceeds peak_kw on average."""
    peak_wh_per_hour = peak_kw * 1000

    return [h for h, flow in enumerate(grid_flow_wh) if -flow > peak_wh_per_hour]


def daily_cost_eur(date_str: str, grid_flow_wh: list[float]) -> tuple[float, float, float]:
    """Returns (import_eur, export_eur, net_eur). net = import - export."""
    tariffs_by_hour = {t.hour_start: t for t in state.tariffs.for_date(date_str)}

    import_eur = 0.0
    export_eur = 0.0

    for h in range(24):
        tariff = tariffs_by_hour.get(h)

        if tariff is None:
            continue

        kwh = abs(grid_flow_wh[h]) / 1000

        if grid_flow_wh[h] < 0:
            import_eur += kwh * tariff.import_price_eur_per_kwh
        else:
            export_eur += kwh * tariff.export_price_eur_per_kwh

    return import_eur, export_eur, import_eur - export_eur
