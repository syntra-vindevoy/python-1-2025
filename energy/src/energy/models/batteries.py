from dataclasses import dataclass

from energy.models.base_table import BaseTable
from energy.models.device import Device


@dataclass(slots=True)
class Battery(Device):
    rec_id: int
    brand: str
    capacity_kwh: float
    max_power_kw: float = 5.0
    round_trip_efficiency: float = 0.9
    min_soc_kwh: float = 0.0

    def store_energy(self):
        pass

    def emit_energy(self):
        pass


class Batteries(BaseTable):
    _FILE = "battery.yaml"
    _MODEL = Battery
