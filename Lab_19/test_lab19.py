"""Focused offline tests for Lab 19's threshold and missing-data rules."""

import unittest

from legend_panel import burry_checks, graham_checks, unprinted_numbers


class Lab19Tests(unittest.TestCase):
    def test_graham_threshold_probe_changes_only_the_screen(self):
        rows = [{"current_ratio": 1.06, "net_income": 1.0}, {"current_ratio": 1.06, "net_income": 2.0}]
        self.assertEqual(list(graham_checks(rows, 2.0).values())[0], "fail")
        self.assertEqual(list(graham_checks(rows, 1.0).values())[0], "pass")

    def test_burry_keeps_missing_inputs_not_known(self):
        rows = [{"operating_cash_flow": None, "net_income": 1.0, "liabilities_to_equity": None}]
        results = burry_checks(rows)
        self.assertEqual(set(results.values()), {"not known"})

    def test_number_guard_covers_each_memo(self):
        rows = [{"fiscal_year_end": "2026-08-30", "net_income": 9226.0, "operating_cash_flow": 15817.0, "equity": 35803.0,
                 "current_ratio": 1.06, "liabilities_to_equity": 1.49, "owner_earnings": 9382.0}]
        memos = {"Buffett": "ROE is 25.8%.", "Graham": "Ratio is 1.06.", "Burry": "Ratio is 40.0."}
        flags = unprinted_numbers(memos, rows, 2.0)
        self.assertEqual(flags["Buffett"], ["25.8"])
        self.assertEqual(flags["Graham"], [])
        self.assertEqual(flags["Burry"], ["40.0"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
