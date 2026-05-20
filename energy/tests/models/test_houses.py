"""
Tests for Houses:
- get(rec_id) returns the House with that rec_id
- the House loaded from resources/house.yaml has the expected address
"""

import unittest

from energy.models.houses import House, Houses


class TestHouses(unittest.TestCase):
    def test_get_returns_house(self):
        houses = Houses()

        self.assertIsInstance(houses.get(1), House)

    def test_get_rec_id_and_address(self):
        houses = Houses()
        house = houses.get(1)

        self.assertEqual(house.rec_id, 1)
        self.assertEqual(house.address, "Nederenamestraat 15, 9700 Oudenaarde")


if __name__ == "__main__":
    unittest.main()
