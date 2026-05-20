from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class BatteryState:
    rec_id: int
    date: str
    end_soc_kwh: float


class BatteryStates(BaseTable):
    _FILE = "battery_state.yaml"
    _MODEL = BatteryState

    def end_soc_for(self, date: str) -> float:
        if self._df.empty or "date" not in self._df.columns:
            return 0.0

        matches = self._df[self._df["date"] == date]

        if matches.empty:
            return 0.0

        return float(matches.iloc[0]["end_soc_kwh"])

    def upsert(self, date: str, end_soc_kwh: float):
        if not self._df.empty and "date" in self._df.columns:
            self._df = self._df[self._df["date"] != date].reset_index(drop=True)

        self.add(BatteryState(rec_id=self.next_rec_id(), date=date, end_soc_kwh=end_soc_kwh))
