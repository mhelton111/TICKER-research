"""Focused readiness checks. Run: python -m unittest -v test_lab20.py"""

from pathlib import Path
import unittest

from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict


ROOT = Path(__file__).resolve().parent


class Lab20Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sleeves, cls.correlations = load_estimates(ROOT / "data" / "prices_through_2026-10-19.csv")

    def test_two_baselines_have_explained_mandate_failures(self):
        equal = evaluate(equal_weight(self.sleeves), self.sleeves, self.correlations)
        reference = evaluate(benchmark(self.sleeves), self.sleeves, self.correlations)
        self.assertIn("return objective", verdict(equal))
        self.assertIn("reserve minimum", verdict(reference))

    def test_constrained_portfolio_meets_checkable_mandate_rules(self):
        result = optimize(self.sleeves, self.correlations)
        self.assertIsNotNone(result)
        self.assertEqual(verdict(result), "PASS")
        self.assertAlmostEqual(sum(result["weights"].values()), 1.0)
        self.assertGreaterEqual(result["return"], .065)
        self.assertGreaterEqual(result["reserve"], .03)

    def test_stress_is_feasible_and_riskier(self):
        base = optimize(self.sleeves, self.correlations)
        stress = optimize(self.sleeves, self.correlations, objective=.075)
        self.assertIsNotNone(stress)
        self.assertGreater(stress["volatility"], base["volatility"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
