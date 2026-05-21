"""SQLAlchemy Core table definitions matching the YAML resource files.

Every table mirrors the corresponding dataclass field-for-field. `rec_id`
is the primary key everywhere. House-to-appliance ownership becomes a
proper junction table `house_appliances` so the dataclass `appliance_ids`
list serialises naturally.
"""

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()


houses_t = Table(
    "houses",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("address", String, nullable=False),
)

appliances_t = Table(
    "appliances",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("type", String, nullable=False),
    Column("consumption_wh", Float, nullable=False),
    Column("category", String, nullable=False, default="Other"),
)

house_appliances_t = Table(
    "house_appliances",
    metadata,
    Column("house_rec_id", Integer, ForeignKey("houses.rec_id", ondelete="CASCADE"), primary_key=True),
    Column("appliance_rec_id", Integer, ForeignKey("appliances.rec_id", ondelete="CASCADE"), primary_key=True),
)

solar_panels_t = Table(
    "solar_panels",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("brand", String, nullable=False),
    Column("capacity_wp", Float, nullable=False),
    Column("performance_ratio", Float, nullable=False, default=0.85),
)

batteries_t = Table(
    "batteries",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("brand", String, nullable=False),
    Column("capacity_kwh", Float, nullable=False),
    Column("max_power_kw", Float, nullable=False, default=5.0),
    Column("round_trip_efficiency", Float, nullable=False, default=0.9),
    Column("min_soc_kwh", Float, nullable=False, default=0.0),
)

electric_cars_t = Table(
    "electric_cars",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("brand", String, nullable=False),
    Column("capacity_kwh", Float, nullable=False),
    Column("max_charge_kw", Float, nullable=False),
    Column("current_soc_kwh", Float, nullable=False, default=0.0),
    Column("min_soc_kwh", Float, nullable=False, default=0.0),
    Column("target_soc_kwh", Float, nullable=False, default=0.0),
    Column("charge_start_hour", Integer, nullable=False, default=18),
    Column("charge_end_hour", Integer, nullable=False, default=8),
)

productions_t = Table(
    "productions",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("hour_start", Integer, nullable=False),
    Column("hour_end", Integer, nullable=False),
    Column("production_wh", Float, nullable=False, default=0.0),
    Column("temperature_c", Float, nullable=False, default=0.0),
    Column("wind_kmh", Float, nullable=False, default=0.0),
    Column("precipitation_mm", Float, nullable=False, default=0.0),
    Column("humidity_pct", Float, nullable=False, default=0.0),
)

schedule_t = Table(
    "schedule",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("device_id", Integer, ForeignKey("appliances.rec_id"), nullable=False),
    Column("start", String, nullable=False),
    Column("end", String, nullable=False),
    Column("moveable", Boolean, nullable=False, default=False),
)

tariffs_t = Table(
    "tariffs",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("hour_start", Integer, nullable=False),
    Column("hour_end", Integer, nullable=False),
    Column("import_price_eur_per_kwh", Float, nullable=False),
    Column("export_price_eur_per_kwh", Float, nullable=False),
)

battery_states_t = Table(
    "battery_states",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("end_soc_kwh", Float, nullable=False),
)

peak_consumptions_t = Table(
    "peak_consumptions",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("valid_from", Date, nullable=False),
    Column("valid_to", Date, nullable=False),
    Column("peak_kw", Float, nullable=False),
)

meter_readings_t = Table(
    "meter_readings",
    metadata,
    Column("rec_id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("hour", Integer, nullable=False),
    Column("imported_kwh", Float, nullable=False, default=0.0),
    Column("exported_kwh", Float, nullable=False, default=0.0),
)
