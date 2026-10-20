"""Automated checks for the Lab 14 known answers and validation behavior."""

from copy import deepcopy
import unittest

import mandate
import portfolio


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        portfolio.validate_correlations(portfolio.SLEEVES, portfolio.CORRELATIONS)
        self.covariance = portfolio.covariance_matrix(portfolio.SLEEVES, portfolio.CORRELATIONS)
        self.portfolios = portfolio.build_portfolios(portfolio.SLEEVES)

    def test_known_answers(self):
        expected = {
            "Benchmark": (0.0680, 0.1046, 0.000),
            "Equal weight": (0.0520, 0.0521, 0.500),
            "Inverse volatility": (0.0377, 0.0105, 0.903),
        }
        for name, (result_return, result_volatility, reserve) in expected.items():
            weights = self.portfolios[name]
            self.assertAlmostEqual(portfolio.expected_return(weights, portfolio.SLEEVES), result_return, places=4)
            self.assertAlmostEqual(portfolio.portfolio_volatility(weights, self.covariance), result_volatility, places=4)
            self.assertAlmostEqual(portfolio.reserve_eligible_weight(weights, portfolio.RESERVE_ELIGIBLE), reserve, places=3)

    def test_higher_ig_equity_correlation_raises_benchmark_volatility_to_11_percent(self):
        correlations = deepcopy(portfolio.CORRELATIONS)
        correlations["ig_bonds"]["equity"] = 0.50
        correlations["equity"]["ig_bonds"] = 0.50
        covariance = portfolio.covariance_matrix(portfolio.SLEEVES, correlations)
        volatility = portfolio.portfolio_volatility(self.portfolios["Benchmark"], covariance)
        self.assertAlmostEqual(volatility, 0.1100, places=4)

    def test_out_of_range_correlation_is_refused(self):
        correlations = deepcopy(portfolio.CORRELATIONS)
        correlations["ig_bonds"]["equity"] = 1.30
        correlations["equity"]["ig_bonds"] = 1.30
        with self.assertRaisesRegex(ValueError, "outside"):
            portfolio.validate_correlations(portfolio.SLEEVES, correlations)

    def test_asymmetric_correlation_is_refused(self):
        correlations = deepcopy(portfolio.CORRELATIONS)
        correlations["ig_bonds"]["equity"] = 0.50
        with self.assertRaisesRegex(ValueError, "not symmetric"):
            portfolio.validate_correlations(portfolio.SLEEVES, correlations)


class MandateTests(unittest.TestCase):
    def test_lab_14_benchmark_fails_only_reserve_rule(self):
        checks = mandate.check_candidate(mandate.CANDIDATES["E (Lab 14 benchmark)"])
        failed_labels = [label for label, _value, passed in checks if not passed]
        self.assertEqual(failed_labels, ["Reserve >= 3.0%"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
