import pandas as pd

from energy.models.appliances import TYPE_LABELS

PRETTY_COLUMNS = {
    "name": "Name",
    "type": "Type",
    "consumption_wh": "Consumption (Wh)",
    "brand": "Brand",
    "capacity_wp": "Capacity (Wp)",
    "capacity_kwh": "Capacity (kWh)",
    "date": "Date",
    "hour_start": "Hour start",
    "hour_end": "Hour end",
    "production_wh": "Production (Wh)",
    "device_id": "Device ID",
    "start": "Start",
    "end": "End",
    "address": "Address",
    "appliance_ids": "Appliances",
    "import_price_eur_per_kwh": "Import price (€/kWh)",
    "export_price_eur_per_kwh": "Export price (€/kWh)",
    "end_soc_kwh": "End-of-day SoC (kWh)",
    "max_power_kw": "Max power (kW)",
    "round_trip_efficiency": "Round-trip η",
    "performance_ratio": "Performance ratio",
    "max_charge_kw": "Max charge (kW)",
    "current_soc_kwh": "Current SoC (kWh)",
    "target_soc_kwh": "Target SoC (kWh)",
    "charge_start_hour": "Charge window start (h)",
    "charge_end_hour": "Charge window end (h)",
    "category": "Category",
    "valid_from": "Valid from",
    "valid_to": "Valid to",
    "peak_kw": "Peak (kW)",
    "min_soc_kwh": "Min SoC (kWh)",
    "moveable": "Moveable?",
    "temperature_c": "Temperature (°C)",
    "wind_kmh": "Wind (km/h)",
    "precipitation_mm": "Rain (mm)",
    "humidity_pct": "Humidity (%)",
}


def display(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    cleaned = df.drop(columns=[c for c in ["rec_id"] if c in df.columns]).copy()

    if "type" in cleaned.columns:
        cleaned["type"] = cleaned["type"].map(lambda v: TYPE_LABELS.get(v, v))

    return cleaned.rename(columns=PRETTY_COLUMNS)
