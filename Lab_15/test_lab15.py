"""Narrow validation checks for Lab 15's required known answers."""

from copy import deepcopy
import unittest

import portfolio


class Lab15Tests(unittest.TestCase):
    def test_meridian_as_loaded_answer(self):
        answer = portfolio.search_lowest_risk_mix(portfolio.SLEEVES, portfolio.CORRELATIONS, 0.065, portfolio.RESERVE_ELIGIBLE, 0.03)
        self.assertEqual(answer["weights"], {"bills": 0.0, "ten_year": 0.20, "ig_bonds": 0.25, "equity": 0.55})
        self.assertAlmostEqual(answer["return"], 0.0651, places=4)
        self.assertAlmostEqual(answer["volatility"], 0.0944, places=4)

    def test_one_point_lower_equity_estimate_changes_answer(self):
        sleeves = deepcopy(portfolio.SLEEVES)
        sleeves["equity"]["return"] = 0.07
        answer = portfolio.search_lowest_risk_mix(sleeves, portfolio.CORRELATIONS, 0.065, portfolio.RESERVE_ELIGIBLE, 0.03)
        self.assertEqual(answer["weights"], {"bills": 0.0, "ten_year": 0.10, "ig_bonds": 0.10, "equity": 0.80})
        self.assertAlmostEqual(answer["return"], 0.0653, places=4)
        self.assertAlmostEqual(answer["volatility"], 0.1294, places=4)

    def test_engine_change_reaches_new_answer(self):
        correlations = deepcopy(portfolio.CORRELATIONS)
        correlations["ig_bonds"]["equity"] = 0.50
        correlations["equity"]["ig_bonds"] = 0.50
        answer = portfolio.search_lowest_risk_mix(portfolio.SLEEVES, correlations, 0.065, portfolio.RESERVE_ELIGIBLE, 0.03)
        self.assertEqual(answer["weights"], {"bills": 0.0, "ten_year": 0.40, "ig_bonds": 0.0, "equity": 0.60})
        self.assertAlmostEqual(answer["return"], 0.0652, places=4)
        self.assertAlmostEqual(answer["volatility"], 0.0973, places=4)

    def test_csv_estimates_are_usable(self):
        sleeves, correlations = portfolio.estimate_from_csv("prices.csv")
        answer = portfolio.search_lowest_risk_mix(sleeves, correlations, 0.065, ("BIL", "IEF"), 0.03)
        self.assertIsNotNone(answer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
