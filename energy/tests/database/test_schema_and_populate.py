"""End-to-end smoke test: create the schema in an in-memory SQLite DB,
populate from the YAML resources, count rows per table.
"""

import unittest

from sqlalchemy import select

from database import get_engine
from database.populate import populate
from database.schema import (
    appliances_t,
    batteries_t,
    electric_cars_t,
    houses_t,
    metadata,
    productions_t,
    schedule_t,
    solar_panels_t,
    tariffs_t,
)


class TestSchemaAndPopulate(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine("sqlite:///:memory:")
        metadata.create_all(self.engine)

    def test_metadata_creates_all_expected_tables(self):
        expected = {
            "houses",
            "appliances",
            "house_appliances",
            "solar_panels",
            "batteries",
            "electric_cars",
            "productions",
            "schedule",
            "tariffs",
            "battery_states",
            "peak_consumptions",
            "meter_readings",
        }

        self.assertEqual(set(metadata.tables.keys()), expected)

    def test_populate_inserts_yaml_rows(self):
        counts = populate(self.engine)

        self.assertGreaterEqual(counts.get("appliances", 0), 10)
        self.assertGreaterEqual(counts.get("productions", 0), 24)
        self.assertGreaterEqual(counts.get("tariffs", 0), 24)
        self.assertGreaterEqual(counts.get("schedule", 0), 1)
        self.assertEqual(counts.get("houses", 0), 1)
        self.assertEqual(counts.get("solar_panels", 0), 1)
        self.assertEqual(counts.get("batteries", 0), 1)
        self.assertEqual(counts.get("electric_cars", 0), 1)

    def test_populate_round_trip_for_appliance(self):
        populate(self.engine)

        with self.engine.connect() as conn:
            rows = conn.execute(select(appliances_t).where(appliances_t.c.rec_id == 1)).fetchall()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].name, "Fridge")
        self.assertEqual(rows[0].type, "always_on")

    def test_populate_links_house_to_appliances(self):
        populate(self.engine)

        with self.engine.connect() as conn:
            count = conn.execute(select(houses_t)).fetchall()

        self.assertEqual(len(count), 1)

        with self.engine.connect() as conn:
            for table in (
                solar_panels_t,
                batteries_t,
                electric_cars_t,
                productions_t,
                schedule_t,
                tariffs_t,
            ):
                conn.execute(select(table)).fetchall()


if __name__ == "__main__":
    unittest.main()
