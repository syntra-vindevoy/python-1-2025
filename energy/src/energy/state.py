from datetime import date, time

from energy.models.appliances import Appliances
from energy.models.batteries import Batteries
from energy.models.battery_states import BatteryStates
from energy.models.electric_cars import ElectricCars
from energy.models.houses import Houses
from energy.models.meter_readings import MeterReadings
from energy.models.peak_consumptions import PeakConsumptions
from energy.models.productions import Productions
from energy.models.schedule import Schedule
from energy.models.solar_panels import SolarPanels
from energy.models.tariffs import Tariffs

SIM_DATE = date(2026, 5, 21)
LATITUDE = 50.85
LONGITUDE = 3.60
SUNRISE = time(5, 51)
SUNSET = time(21, 43)
WAKE = time(7, 0)
SLEEP = time(23, 0)

# Maximum continuous grid-import power (kW) we are willing to draw. Sized to a
# typical Belgian 3-phase 16 A connection (~11 kW), which is what households
# with a home EV wall box subscribe to. The "capaciteitstarief" target of
# 2.5 kW is uneconomical once a 100 kWh EV needs charging overnight; the
# simulation still flags any hour whose import exceeds this value.
PEAK_KW = 3.5


appliances = Appliances()
panels = SolarPanels()
batteries = Batteries()
productions = Productions()
schedule = Schedule()
tariffs = Tariffs()
battery_states = BatteryStates()
electric_cars = ElectricCars()
peak_consumptions = PeakConsumptions()
meter_readings = MeterReadings()
houses = Houses(appliances=appliances)
house = houses.get(1)

house.add_solar_panels(20, panels.get(1))
house.add_batteries(2, batteries.get(1))
house.add_electric_car(electric_cars.get(1))


def peak_kw_for(target) -> float:
    return peak_consumptions.peak_for(target.isoformat(), default=PEAK_KW)


TABLES = {
    "Devices": appliances,
    "Solar panels": panels,
    "Batteries": batteries,
    "Production": productions,
    "Consumption": schedule,
    "Tariffs": tariffs,
    "Battery state": battery_states,
    "Electric cars": electric_cars,
    "Peak consumption": peak_consumptions,
    "Meter readings": meter_readings,
}
