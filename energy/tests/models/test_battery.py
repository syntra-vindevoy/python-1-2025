"""
Tests for Battery:
- construction sets the rec_id, brand and capacity_kwh
- store_energy returns None
- emit_energy returns None
- Battery is a subclass of Device
- slots prevent setting unknown attributes
"""

import unittest

from energy.models.batteries import Battery
from energy.models.device import Device


class TestBattery(unittest.TestCase):
    def test_construction(self):
        battery = Battery(rec_id=1, brand="Tesla Powerwall 3", capacity_kwh=13.5)

        self.assertEqual(battery.rec_id, 1)
        self.assertEqual(battery.brand, "Tesla Powerwall 3")
        self.assertEqual(battery.capacity_kwh, 13.5)

    def test_store_energy_returns_none(self):
        battery = Battery(rec_id=1, brand="X", capacity_kwh=13.5)

        self.assertIsNone(battery.store_energy())

    def test_emit_energy_returns_none(self):
        battery = Battery(rec_id=1, brand="X", capacity_kwh=13.5)

        self.assertIsNone(battery.emit_energy())

    def test_is_device(self):
        self.assertTrue(issubclass(Battery, Device))

    def test_slots_prevent_new_attribute(self):
        battery = Battery(rec_id=1, brand="X", capacity_kwh=13.5)

        with self.assertRaises(AttributeError):
            battery.extra = 1


if __name__ == "__main__":
    unittest.main()
