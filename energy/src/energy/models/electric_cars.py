from dataclasses import dataclass

from energy.models.base_table import BaseTable
from energy.models.device import Device


@dataclass(slots=True)
class ElectricCar(Device):
    rec_id: int
    brand: str
    capacity_kwh: float
    max_charge_kw: float
    current_soc_kwh: float = 0.0
    min_soc_kwh: float = 0.0
    target_soc_kwh: float = 0.0
    charge_start_hour: int = 18
    charge_end_hour: int = 8


class ElectricCars(BaseTable):
    _FILE = "car.yaml"
    _MODEL = ElectricCar


def available_hours(start: int, end: int) -> list[int]:
    if start <= end:
        return list(range(start, end))

    return list(range(start, 24)) + list(range(0, end))
