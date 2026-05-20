import json
import urllib.request
from datetime import date, timedelta

from energy import state
from energy.models.productions import Production

FETCH_DAYS = 5
HOURLY_VARS = (
    "shortwave_radiation",
    "temperature_2m",
    "wind_speed_10m",
    "precipitation",
    "relative_humidity_2m",
)


def fetch_production(start_date: date, days: int = FETCH_DAYS) -> list[str]:
    """Fetch hourly weather + production for `days` days starting at `start_date`.

    Pulls shortwave_radiation (drives panel production) plus a small bundle of
    display-only context: temperature_2m, wind_speed_10m, precipitation,
    relative_humidity_2m. Existing rows for any of those dates are removed
    first so re-fetching always overwrites with the freshest forecast.
    """
    end_date = start_date + timedelta(days=days - 1)
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={state.LATITUDE}&longitude={state.LONGITUDE}"
        f"&hourly={','.join(HOURLY_VARS)}"
        f"&timezone=Europe/Brussels"
        f"&start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )

    with urllib.request.urlopen(url, timeout=15) as response:
        payload = json.loads(response.read())

    hourly = payload["hourly"]
    times = hourly["time"]
    irradiances = hourly["shortwave_radiation"]
    temperatures = hourly["temperature_2m"]
    wind_speeds = hourly["wind_speed_10m"]
    precipitations = hourly["precipitation"]
    humidities = hourly["relative_humidity_2m"]
    panel_wp = state.panels.get(1).capacity_wp

    dates_written = sorted({ts.split("T")[0] for ts in times})

    for date_str in dates_written:
        state.productions.delete_date(date_str)

    next_id = state.productions.next_rec_id()

    def _safe(value):
        return round(float(value), 1) if value is not None else 0.0

    for timestamp, irr, temp, wind, rain, hum in zip(times, irradiances, temperatures, wind_speeds, precipitations, humidities):
        date_str, time_str = timestamp.split("T")
        hour = int(time_str.split(":")[0])
        production = round(panel_wp * (irr or 0) / 1000, 2)

        state.productions.add(
            Production(
                rec_id=next_id,
                date=date_str,
                hour_start=hour,
                hour_end=hour + 1,
                production_wh=production,
                temperature_c=_safe(temp),
                wind_kmh=_safe(wind),
                precipitation_mm=_safe(rain),
                humidity_pct=_safe(hum),
            )
        )
        next_id += 1

    state.productions.save()

    return dates_written
