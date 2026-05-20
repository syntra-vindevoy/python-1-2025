"""
Tests for Grid:
- construction sets the name
- deliver_energy returns None (pass)
- absorb_energy returns None (pass)
- slots prevent setting unknown attributes
"""

import unittest

from energy.models.grid import Grid


class TestGrid(unittest.TestCase):
    def test_construction(self):
        grid = Grid(name="Fluvius")

        self.assertEqual(grid.name, "Fluvius")

    def test_deliver_energy_returns_none(self):
        grid = Grid(name="Fluvius")

        self.assertIsNone(grid.deliver_energy())

    def test_absorb_energy_returns_none(self):
        grid = Grid(name="Fluvius")

        self.assertIsNone(grid.absorb_energy())

    def test_slots_prevent_new_attribute(self):
        grid = Grid(name="Fluvius")

        with self.assertRaises(AttributeError):
            grid.extra = 1


if __name__ == "__main__":
    unittest.main()
