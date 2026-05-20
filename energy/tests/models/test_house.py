"""
Tests for House:
- construction sets the rec_id and address
- add_device returns None
- change_device returns None
- delete_device returns None
- add_solar_panels returns None
- add_batteries returns None
- slots prevent setting unknown attributes
"""

import unittest

from energy.models.batteries import Battery
from energy.models.houses import House
from energy.models.solar_panels import SolarPanel


class TestHouse(unittest.TestCase):
    def test_construction(self):
        house = House(rec_id=1, address="Nederenamestraat 15, 9700 Oudenaarde")

        self.assertEqual(house.rec_id, 1)
        self.assertEqual(house.address, "Nederenamestraat 15, 9700 Oudenaarde")

    def test_add_device_returns_none(self):
        house = House(rec_id=1, address="X")

        self.assertIsNone(house.add_device(None))

    def test_change_device_returns_none(self):
        house = House(rec_id=1, address="X")

        self.assertIsNone(house.change_device(None))

    def test_delete_device_returns_none(self):
        house = House(rec_id=1, address="X")

        self.assertIsNone(house.delete_device(None))

    def test_add_solar_panels_returns_none(self):
        house = House(rec_id=1, address="X")
        panel = SolarPanel(rec_id=1, brand="SunPower Maxeon 6", capacity_wp=425.0)

        self.assertIsNone(house.add_solar_panels(20, panel))

    def test_add_batteries_returns_none(self):
        house = House(rec_id=1, address="X")
        battery = Battery(rec_id=1, brand="Tesla Powerwall 3", capacity_kwh=13.5)

        self.assertIsNone(house.add_batteries(2, battery))

    def test_slots_prevent_new_attribute(self):
        house = House(rec_id=1, address="X")

        with self.assertRaises(AttributeError):
            house.extra = 1


if __name__ == "__main__":
    unittest.main()
