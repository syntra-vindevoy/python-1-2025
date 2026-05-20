"""
Tests for SolarPanel:
- construction sets the rec_id, brand and capacity_wp (Watt-peak)
- produce_energy returns None
- SolarPanel is a subclass of Device
- slots prevent setting unknown attributes
"""

import unittest

from energy.models.device import Device
from energy.models.solar_panels import SolarPanel


class TestSolarPanel(unittest.TestCase):
    def test_construction(self):
        panel = SolarPanel(rec_id=1, brand="SunPower Maxeon 6", capacity_wp=425.0)

        self.assertEqual(panel.rec_id, 1)
        self.assertEqual(panel.brand, "SunPower Maxeon 6")
        self.assertEqual(panel.capacity_wp, 425.0)

    def test_produce_energy_returns_none(self):
        panel = SolarPanel(rec_id=1, brand="X", capacity_wp=425.0)

        self.assertIsNone(panel.produce_energy())

    def test_is_device(self):
        self.assertTrue(issubclass(SolarPanel, Device))

    def test_slots_prevent_new_attribute(self):
        panel = SolarPanel(rec_id=1, brand="X", capacity_wp=425.0)

        with self.assertRaises(AttributeError):
            panel.extra = 1


if __name__ == "__main__":
    unittest.main()
