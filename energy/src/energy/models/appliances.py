from dataclasses import dataclass
from enum import Enum

from energy.models.base_table import BaseTable
from energy.models.device import Device

TYPE_LABELS = {
    "always_on": "Always on",
    "switchable": "Switchable",
    "light": "Light",
}


class ApplianceType(str, Enum):
    ALWAYS_ON = "always_on"
    SWITCHABLE = "switchable"
    LIGHT = "light"


@dataclass(slots=True)
class Appliance(Device):
    rec_id: int
    name: str
    type: ApplianceType
    consumption_wh: float
    category: str = "Other"


class Appliances(BaseTable):
    _FILE = "device.yaml"
    _MODEL = Appliance

    def _row_to_model(self, row) -> Appliance:
        data = row.to_dict()
        raw_type = data.get("type")

        if not isinstance(raw_type, ApplianceType):
            raw_type = ApplianceType(raw_type)

        return Appliance(
            rec_id=int(data["rec_id"]),
            name=str(data["name"]),
            type=raw_type,
            consumption_wh=float(data["consumption_wh"]),
            category=str(data.get("category", "Other") or "Other"),
        )

    def _model_to_row(self, record: Appliance) -> dict:
        return {
            "rec_id": record.rec_id,
            "name": record.name,
            "type": record.type.value if isinstance(record.type, ApplianceType) else record.type,
            "consumption_wh": record.consumption_wh,
            "category": record.category,
        }
