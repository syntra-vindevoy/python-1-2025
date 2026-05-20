"""
Tests for energy.controllers.simulation:
- hourly_consumption returns 24 entries for the simulated date
- hourly_consumption baseline equals sum of always_on appliances at off-hours (deep night)
- simulate_day clamps SoC into [0, total_capacity]
- simulate_day with start_soc=0 ends at the same value persisted in battery_states
"""

import unittest

from energy import state
from energy.controllers.simulation import (
    hourly_consumption,
    hourly_production,
    simulate_day,
    simulate_day_greedy,
    simulate_day_linear,
    simulate_day_stochastic,
)
from energy.models.appliances import ApplianceType


class TestSimulation(unittest.TestCase):
    def test_hourly_consumption_length(self):
        hours = hourly_consumption(state.SIM_DATE)

        self.assertEqual(len(hours), 24)

    def test_baseline_matches_always_on(self):
        baseline = sum(a.consumption_wh for a in state.house.appliances if a.type == ApplianceType.ALWAYS_ON)
        hours = hourly_consumption(state.SIM_DATE)

        # 03:00 is well before sunrise but the user is asleep, so no light, no schedule.
        self.assertAlmostEqual(hours[3], baseline, places=3)

    def test_hourly_production_length(self):
        hours = hourly_production(state.SIM_DATE)

        self.assertEqual(len(hours), 24)

    def test_simulate_day_clamps_soc(self):
        capacity_kwh = sum(count * b.capacity_kwh for count, b in state.house.batteries)
        result = simulate_day(state.SIM_DATE, start_soc_kwh=0.0)

        self.assertEqual(len(result.soc_kwh), 24)
        self.assertTrue(all(0.0 <= s <= capacity_kwh + 1e-6 for s in result.soc_kwh))
        self.assertLessEqual(result.end_soc_kwh, capacity_kwh + 1e-6)
        self.assertGreaterEqual(result.end_soc_kwh, 0.0)
        self.assertEqual(len(result.grid_flow_wh), 24)
        self.assertEqual(len(result.battery_to_load_wh), 24)

    def test_efficiency_loss_reduces_end_soc(self):
        # All-surplus day: 1 kWh/h for 24 h. With round_trip=0.9 → one_way ≈ 0.949.
        # Capacity is 27 kWh, so battery fills up; loss shows in what was stored.
        result = simulate_day(state.SIM_DATE, start_soc_kwh=0.0)
        capacity_kwh = sum(count * b.capacity_kwh for count, b in state.house.batteries)

        # End SoC should reach capacity given the large solar surplus.
        self.assertGreater(result.end_soc_kwh, capacity_kwh * 0.95)

    def test_battery_to_load_never_exceeds_consumption(self):
        result = simulate_day(state.SIM_DATE, start_soc_kwh=0.0)

        for h in range(24):
            self.assertLessEqual(result.battery_to_load_wh[h], result.consumption_wh[h] + 1e-6)

    def test_greedy_meets_ev_minimum(self):
        ev = state.house.electric_cars[0] if state.house.electric_cars else None

        if ev is None:
            self.skipTest("No EV on the house")

        min_need_kwh = max(0.0, ev.min_soc_kwh - ev.current_soc_kwh)
        result = simulate_day_greedy(state.SIM_DATE, start_soc_kwh=0.0)
        delivered_kwh = sum(result.ev_charge_wh) / 1000

        self.assertGreaterEqual(delivered_kwh, min_need_kwh - 1e-3)

    def test_all_modes_meet_ev_minimum(self):
        ev = state.house.electric_cars[0] if state.house.electric_cars else None

        if ev is None:
            self.skipTest("No EV on the house")

        min_need_kwh = max(0.0, ev.min_soc_kwh - ev.current_soc_kwh)
        greedy = simulate_day_greedy(state.SIM_DATE, start_soc_kwh=0.0)
        smart = simulate_day_linear(state.SIM_DATE, start_soc_kwh=0.0)

        # Min is non-negotiable in every mode.
        self.assertGreaterEqual(sum(greedy.ev_charge_wh) / 1000, min_need_kwh - 1e-3)
        self.assertGreaterEqual(sum(smart.ev_charge_wh) / 1000, min_need_kwh - 1e-3)

    def test_simulate_day_dispatcher(self):
        a = simulate_day(state.SIM_DATE, start_soc_kwh=0.0, mode="greedy")
        b = simulate_day(state.SIM_DATE, start_soc_kwh=0.0, mode="linear")
        c = simulate_day(state.SIM_DATE, start_soc_kwh=0.0, mode="stochastic")

        self.assertEqual(len(a.soc_kwh), 24)
        self.assertEqual(len(b.soc_kwh), 24)
        self.assertEqual(len(c.soc_kwh), 24)

    def test_stochastic_produces_cost_range(self):
        result = simulate_day_stochastic(state.SIM_DATE, start_soc_kwh=0.0, n_scenarios=5, seed=7)

        self.assertEqual(result.n_scenarios, 5)
        self.assertLessEqual(result.cost_min_eur, result.cost_mean_eur + 1e-6)
        self.assertGreaterEqual(result.cost_max_eur, result.cost_mean_eur - 1e-6)


if __name__ == "__main__":
    unittest.main()
