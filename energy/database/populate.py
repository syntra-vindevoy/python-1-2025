"""Load all YAML resource files into the database.

Idempotent — wipes every table first, then inserts fresh rows. Useful both
for the first SQLite spin-up and for resetting a Postgres dev database back
to the YAML "source of truth".

Run manually:
    PYTHONPATH=src:. uv run python -m database.populate
or with a Postgres URL:
    ENERGY_DATABASE_URL=postgresql://... uv run python -m database.populate
"""

import sys
from datetime import date
from pathlib import Path

from sqlalchemy.engine import Engine

# Allow running as a script. populate.py is at database/populate.py so
# parents[1] is the project root (energy/).
PROJECT_ROOT = Path(__file__).resolve().parents[1]

for path in (PROJECT_ROOT, PROJECT_ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from database import get_engine  # noqa: E402
from database.schema import (  # noqa: E402
    appliances_t,
    batteries_t,
    battery_states_t,
    electric_cars_t,
    house_appliances_t,
    houses_t,
    metadata,
    meter_readings_t,
    peak_consumptions_t,
    productions_t,
    schedule_t,
    solar_panels_t,
    tariffs_t,
)
from energy.models.appliances import Appliances, ApplianceType  # noqa: E402
from energy.models.batteries import Batteries  # noqa: E402
from energy.models.battery_states import BatteryStates  # noqa: E402
from energy.models.electric_cars import ElectricCars  # noqa: E402
from energy.models.houses import Houses  # noqa: E402
from energy.models.meter_readings import MeterReadings  # noqa: E402
from energy.models.peak_consumptions import PeakConsumptions  # noqa: E402
from energy.models.productions import Productions  # noqa: E402
from energy.models.schedule import Schedule  # noqa: E402
from energy.models.solar_panels import SolarPanels  # noqa: E402
from energy.models.tariffs import Tariffs  # noqa: E402


def _to_date(value):
    if isinstance(value, date):
        return value

    return date.fromisoformat(str(value))


def populate(engine: Engine) -> dict[str, int]:
    """Insert all YAML data into the DB. Returns a per-table row count."""
    counts: dict[str, int] = {}

    appliances = Appliances()
    solar_panels = SolarPanels()
    batteries = Batteries()
    electric_cars = ElectricCars()
    productions = Productions()
    schedule = Schedule()
    tariffs = Tariffs()
    battery_states = BatteryStates()
    peak_consumptions = PeakConsumptions()
    meter_readings = MeterReadings()
    houses = Houses(appliances=appliances)

    with engine.begin() as conn:
        # Wipe in FK-safe order
        for table in reversed(metadata.sorted_tables):
            conn.execute(table.delete())

        appl_rows = [
            {
                "rec_id": a.rec_id,
                "name": a.name,
                "type": a.type.value if isinstance(a.type, ApplianceType) else a.type,
                "consumption_wh": a.consumption_wh,
                "category": a.category,
            }
            for a in appliances.all()
        ]

        if appl_rows:
            conn.execute(appliances_t.insert(), appl_rows)
            counts["appliances"] = len(appl_rows)

        panel_rows = [
            {"rec_id": p.rec_id, "brand": p.brand, "capacity_wp": p.capacity_wp, "performance_ratio": p.performance_ratio}
            for p in solar_panels.all()
        ]

        if panel_rows:
            conn.execute(solar_panels_t.insert(), panel_rows)
            counts["solar_panels"] = len(panel_rows)

        battery_rows = [
            {
                "rec_id": b.rec_id,
                "brand": b.brand,
                "capacity_kwh": b.capacity_kwh,
                "max_power_kw": b.max_power_kw,
                "round_trip_efficiency": b.round_trip_efficiency,
                "min_soc_kwh": b.min_soc_kwh,
            }
            for b in batteries.all()
        ]

        if battery_rows:
            conn.execute(batteries_t.insert(), battery_rows)
            counts["batteries"] = len(battery_rows)

        car_rows = [
            {
                "rec_id": c.rec_id,
                "brand": c.brand,
                "capacity_kwh": c.capacity_kwh,
                "max_charge_kw": c.max_charge_kw,
                "current_soc_kwh": c.current_soc_kwh,
                "min_soc_kwh": c.min_soc_kwh,
                "target_soc_kwh": c.target_soc_kwh,
                "charge_start_hour": c.charge_start_hour,
                "charge_end_hour": c.charge_end_hour,
            }
            for c in electric_cars.all()
        ]

        if car_rows:
            conn.execute(electric_cars_t.insert(), car_rows)
            counts["electric_cars"] = len(car_rows)

        prod_rows = [
            {
                "rec_id": p.rec_id,
                "date": _to_date(p.date),
                "hour_start": p.hour_start,
                "hour_end": p.hour_end,
                "production_wh": p.production_wh,
                "temperature_c": p.temperature_c,
                "wind_kmh": p.wind_kmh,
                "precipitation_mm": p.precipitation_mm,
                "humidity_pct": p.humidity_pct,
            }
            for p in productions.all()
        ]

        if prod_rows:
            conn.execute(productions_t.insert(), prod_rows)
            counts["productions"] = len(prod_rows)

        sched_rows = [
            {
                "rec_id": s.rec_id,
                "device_id": s.device_id,
                "start": s.start,
                "end": s.end,
                "moveable": bool(s.moveable),
            }
            for s in schedule.all()
        ]

        if sched_rows:
            conn.execute(schedule_t.insert(), sched_rows)
            counts["schedule"] = len(sched_rows)

        tariff_rows = [
            {
                "rec_id": t.rec_id,
                "date": _to_date(t.date),
                "hour_start": t.hour_start,
                "hour_end": t.hour_end,
                "import_price_eur_per_kwh": t.import_price_eur_per_kwh,
                "export_price_eur_per_kwh": t.export_price_eur_per_kwh,
            }
            for t in tariffs.all()
        ]

        if tariff_rows:
            conn.execute(tariffs_t.insert(), tariff_rows)
            counts["tariffs"] = len(tariff_rows)

        bs_rows = [{"rec_id": s.rec_id, "date": _to_date(s.date), "end_soc_kwh": s.end_soc_kwh} for s in battery_states.all()]

        if bs_rows:
            conn.execute(battery_states_t.insert(), bs_rows)
            counts["battery_states"] = len(bs_rows)

        peak_rows = [
            {
                "rec_id": p.rec_id,
                "valid_from": _to_date(p.valid_from),
                "valid_to": _to_date(p.valid_to),
                "peak_kw": p.peak_kw,
            }
            for p in peak_consumptions.all()
        ]

        if peak_rows:
            conn.execute(peak_consumptions_t.insert(), peak_rows)
            counts["peak_consumptions"] = len(peak_rows)

        meter_rows = [
            {
                "rec_id": m.rec_id,
                "date": _to_date(m.date),
                "hour": m.hour,
                "imported_kwh": m.imported_kwh,
                "exported_kwh": m.exported_kwh,
            }
            for m in meter_readings.all()
        ]

        if meter_rows:
            conn.execute(meter_readings_t.insert(), meter_rows)
            counts["meter_readings"] = len(meter_rows)

        # Houses last (FK target for the junction).
        house_rows = []
        house_appliance_rows = []

        for h in houses.all():
            house_rows.append({"rec_id": h.rec_id, "address": h.address})

            for a in h.appliances:
                house_appliance_rows.append({"house_rec_id": h.rec_id, "appliance_rec_id": a.rec_id})

        if house_rows:
            conn.execute(houses_t.insert(), house_rows)
            counts["houses"] = len(house_rows)

        if house_appliance_rows:
            conn.execute(house_appliances_t.insert(), house_appliance_rows)
            counts["house_appliances"] = len(house_appliance_rows)

    return counts


if __name__ == "__main__":
    engine = get_engine()
    counts = populate(engine)
    print(f"Populated {engine.url}:")

    for table, n in counts.items():
        print(f"  {table:<20} {n} rows")
