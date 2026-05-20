from dataclasses import dataclass, field

from energy.models.appliances import Appliance, Appliances
from energy.models.base_table import BaseTable
from energy.models.batteries import Battery
from energy.models.electric_cars import ElectricCar
from energy.models.solar_panels import SolarPanel


@dataclass(slots=True)
class House:
    rec_id: int
    address: str
    appliances: list[Appliance] = field(default_factory=list)
    panels: list[tuple[int, SolarPanel]] = field(default_factory=list)
    batteries: list[tuple[int, Battery]] = field(default_factory=list)
    electric_cars: list[ElectricCar] = field(default_factory=list)

    def add_device(self, appliance: Appliance):
        self.appliances.append(appliance)

    def change_device(self, appliance: Appliance):
        for i, existing in enumerate(self.appliances):
            if existing.rec_id == getattr(appliance, "rec_id", None):
                self.appliances[i] = appliance
                return

    def delete_device(self, appliance: Appliance):
        if appliance in self.appliances:
            self.appliances.remove(appliance)

    def add_solar_panels(self, count: int, panel: SolarPanel):
        self.panels.append((count, panel))

    def add_batteries(self, count: int, battery: Battery):
        self.batteries.append((count, battery))

    def add_electric_car(self, car: ElectricCar):
        self.electric_cars.append(car)

    def show_totals(self):
        total_panel_wp = sum(count * panel.capacity_wp for count, panel in self.panels)
        total_battery_kwh = sum(count * battery.capacity_kwh for count, battery in self.batteries)

        print(f"Total solar panel capacity: {total_panel_wp} Wp")
        print(f"Total battery capacity: {total_battery_kwh} kWh")


class Houses(BaseTable):
    _FILE = "house.yaml"
    _MODEL = House

    def __init__(self, appliances: Appliances | None = None):
        super().__init__()

        self._appliances = appliances

    def _row_to_model(self, row) -> House:
        data = row.to_dict()
        ids = data.get("appliance_ids") or []

        if not isinstance(ids, list):
            ids = []

        apps = []

        if self._appliances is not None:
            for aid in ids:
                apps.append(self._appliances.get(int(aid)))

        return House(rec_id=int(data["rec_id"]), address=data["address"], appliances=apps)

    def _model_to_row(self, record: House) -> dict:
        return {
            "rec_id": record.rec_id,
            "address": record.address,
            "appliance_ids": [a.rec_id for a in record.appliances],
        }
