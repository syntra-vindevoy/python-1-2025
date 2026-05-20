from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class Tariff:
    rec_id: int
    date: str
    hour_start: int
    hour_end: int
    import_price_eur_per_kwh: float
    export_price_eur_per_kwh: float


class Tariffs(BaseTable):
    _FILE = "tariff.yaml"
    _MODEL = Tariff

    def for_date(self, date: str) -> list[Tariff]:
        filtered = self._df[self._df["date"] == date].sort_values("hour_start")

        return [self._row_to_model(row) for _, row in filtered.iterrows()]
