from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class PeakConsumption:
    rec_id: int
    valid_from: str
    valid_to: str
    peak_kw: float


class PeakConsumptions(BaseTable):
    _FILE = "peak_consumption.yaml"
    _MODEL = PeakConsumption

    def peak_for(self, date_str: str, default: float = 3.5) -> float:
        if self._df.empty:
            return default

        match = self._df[(self._df["valid_from"] <= date_str) & (self._df["valid_to"] >= date_str)]

        if match.empty:
            return default

        return float(match.iloc[0]["peak_kw"])
