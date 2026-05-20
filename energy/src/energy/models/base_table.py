from dataclasses import asdict
from pathlib import Path

import pandas as pd
import yaml

_RESOURCES = Path(__file__).resolve().parents[3] / "resources"


class BaseTable:
    _FILE: str = ""
    _MODEL: type = object

    def __init__(self):
        self._path = _RESOURCES / self._FILE

        with open(self._path) as f:
            data = yaml.safe_load(f) or []

        self._df = pd.DataFrame(data)

    def to_dataframe(self) -> pd.DataFrame:
        return self._df

    def next_rec_id(self) -> int:
        if self._df.empty or "rec_id" not in self._df.columns:
            return 1

        return int(self._df["rec_id"].max()) + 1

    def get(self, rec_id: int):
        rows = self._df[self._df["rec_id"] == rec_id]

        if rows.empty:
            raise KeyError(rec_id)

        return self._row_to_model(rows.iloc[0])

    def all(self) -> list:
        return [self._row_to_model(row) for _, row in self._df.iterrows()]

    def add(self, record):
        new_row = pd.DataFrame([self._model_to_row(record)])
        self._df = pd.concat([self._df, new_row], ignore_index=True)

    def edit(self, rec_id: int, record):
        mask = self._df["rec_id"] == rec_id

        for column, value in self._model_to_row(record).items():
            self._df.loc[mask, column] = value

    def delete(self, rec_id: int):
        self._df = self._df[self._df["rec_id"] != rec_id].reset_index(drop=True)

    def save(self):
        data = self._df.to_dict(orient="records")

        with open(self._path, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    def _row_to_model(self, row):
        return self._MODEL(**row.to_dict())

    def _model_to_row(self, record) -> dict:
        return asdict(record)
