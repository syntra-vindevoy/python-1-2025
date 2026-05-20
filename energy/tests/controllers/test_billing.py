"""
Tests for energy.controllers.billing:
- hourly_grid_flow_wh: net_wh - battery_change_wh; positive = export, negative = import
- daily_cost_eur splits import vs export against tariff rows
- hours_over_peak flags hours whose import exceeds the configured peak
"""

import unittest

from energy.controllers.billing import (
    consumption_breakdown,
    daily_cost_eur,
    hours_over_peak,
)


class TestDailyCost(unittest.TestCase):
    def test_daily_cost_uses_existing_tariffs(self):
        flow = [-1000.0] * 24
        imp, exp, net = daily_cost_eur("2026-05-21", flow)

        self.assertGreater(imp, 0)
        self.assertEqual(exp, 0)
        self.assertAlmostEqual(net, imp, places=6)

    def test_daily_cost_export_only(self):
        flow = [1000.0] * 24
        imp, exp, net = daily_cost_eur("2026-05-21", flow)

        self.assertEqual(imp, 0)
        self.assertGreater(exp, 0)
        self.assertAlmostEqual(net, -exp, places=6)

    def test_daily_cost_unknown_date_is_zero(self):
        flow = [-1000.0] * 24

        self.assertEqual(daily_cost_eur("1999-01-01", flow), (0.0, 0.0, 0.0))


class TestPeakWatch(unittest.TestCase):
    def test_no_violation_when_within_peak(self):
        flow = [-1000.0] * 24

        self.assertEqual(hours_over_peak(flow, peak_kw=2.5), [])

    def test_violations_when_import_exceeds_peak(self):
        flow = [-3000.0 if h in (18, 19) else -500.0 for h in range(24)]

        self.assertEqual(hours_over_peak(flow, peak_kw=2.5), [18, 19])

    def test_export_never_counts_as_peak(self):
        flow = [5000.0] * 24

        self.assertEqual(hours_over_peak(flow, peak_kw=2.5), [])


class TestConsumptionBreakdown(unittest.TestCase):
    def test_breakdown_sums_to_consumption(self):
        consumption = [500.0] * 24
        production = [100.0] * 24
        battery_to_load = [0.0] * 24
        from_p, from_b, paid, credited = consumption_breakdown(
            consumption,
            production,
            battery_to_load,
            "2026-05-21",
        )

        for h in range(24):
            self.assertAlmostEqual(from_p[h] + from_b[h] + paid[h] + credited[h], consumption[h], places=3)

    def test_breakdown_direct_solar_first(self):
        consumption = [200.0] * 24
        production = [1000.0] * 24
        battery_to_load = [0.0] * 24
        from_p, from_b, paid, credited = consumption_breakdown(
            consumption,
            production,
            battery_to_load,
            "2026-05-21",
        )

        self.assertTrue(all(p == 200.0 for p in from_p))
        self.assertTrue(all(b == 0 for b in from_b))
        self.assertTrue(all(g == 0 for g in paid))
        self.assertTrue(all(g == 0 for g in credited))

    def test_breakdown_battery_after_panels(self):
        consumption = [200.0] * 24
        production = [0.0] * 24
        battery_to_load = [200.0] * 24
        from_p, from_b, paid, credited = consumption_breakdown(
            consumption,
            production,
            battery_to_load,
            "2026-05-21",
        )

        self.assertTrue(all(p == 0 for p in from_p))
        self.assertTrue(all(b == 200.0 for b in from_b))
        self.assertTrue(all(g == 0 for g in paid))
        self.assertTrue(all(g == 0 for g in credited))

    def test_breakdown_grid_when_panels_and_battery_empty(self):
        consumption = [200.0] * 24
        production = [0.0] * 24
        battery_to_load = [0.0] * 24
        from_p, from_b, paid, credited = consumption_breakdown(
            consumption,
            production,
            battery_to_load,
            "2026-05-21",
        )

        self.assertTrue(all(p == 200.0 for p in paid))
        self.assertTrue(all(c == 0 for c in credited))


if __name__ == "__main__":
    unittest.main()
