from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class Production:
    rec_id: int
    date: str
    hour_start: int
    hour_end: int
    production_wh: float
    temperature_c: float = 0.0
    wind_kmh: float = 0.0
    precipitation_mm: float = 0.0
    humidity_pct: float = 0.0


class Productions(BaseTable):
    _FILE = "production.yaml"
    _MODEL = Production

    def for_date(self, date: str) -> list[Production]:
        filtered = self._df[self._df["date"] == date].sort_values("hour_start")

        return [self._row_to_model(row) for _, row in filtered.iterrows()]

    def delete_date(self, date: str):
        self._df = self._df[self._df["date"] != date].reset_index(drop=True)
