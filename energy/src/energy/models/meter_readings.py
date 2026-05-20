from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class MeterReading:
    rec_id: int
    date: str
    hour: int
    imported_kwh: float = 0.0
    exported_kwh: float = 0.0


class MeterReadings(BaseTable):
    _FILE = "meter.yaml"
    _MODEL = MeterReading

    def for_date(self, date: str) -> list[MeterReading]:
        if self._df.empty or "date" not in self._df.columns:
            return []

        filtered = self._df[self._df["date"] == date].sort_values("hour")

        return [self._row_to_model(row) for _, row in filtered.iterrows()]

    def actual_grid_flow_wh(self, date: str) -> list[float] | None:
        """24 hourly grid flow values (positive = export, negative = import) in
        Wh, derived from meter readings. Returns None when no meter data exists
        for the date — the caller should fall back to the predicted dispatch.

        Hours without a reading get 0 (treated as "no exchange that hour"),
        which lets a partially-populated day (today, with hours up to "now")
        blend cleanly with the rest of the simulation."""
        readings = {r.hour: r for r in self.for_date(date)}

        if not readings:
            return None

        return [((readings[h].exported_kwh - readings[h].imported_kwh) * 1000) if h in readings else 0.0 for h in range(24)]
