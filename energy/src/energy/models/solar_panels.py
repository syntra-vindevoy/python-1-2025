from dataclasses import dataclass

from energy.models.base_table import BaseTable
from energy.models.device import Device


@dataclass(slots=True)
class SolarPanel(Device):
    rec_id: int
    brand: str
    capacity_wp: float
    performance_ratio: float = 0.85

    def produce_energy(self):
        pass


class SolarPanels(BaseTable):
    _FILE = "panel.yaml"
    _MODEL = SolarPanel
