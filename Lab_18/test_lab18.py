"""Offline tests for the deterministic Lab 18 EDGAR calculation rules."""

import unittest

from edgar_buffett import checks, display, printed_numbers, unprinted_memo_numbers


class Lab18Tests(unittest.TestCase):
    def test_all_pass_checks(self):
        rows = [{"roe": 15.0, "owner_earnings": 2.0}, {"roe": 20.0, "owner_earnings": 3.0}]
        result = checks(rows)
        self.assertEqual(set(result.values()), {"pass"})

    def test_missing_capex_makes_owner_earnings_checks_not_known(self):
        rows = [{"roe": 20.0, "owner_earnings": None}, {"roe": 20.0, "owner_earnings": None}]
        result = checks(rows)
        self.assertEqual(result["ROE of 15% or more every year"], "pass")
        self.assertEqual(result["Owner earnings positive every year"], "not known")
        self.assertEqual(result["Owner earnings grew, first year to last"], "not known")

    def test_printed_numbers_include_formatted_facts(self):
        rows = [{"fiscal_year_end": "2026-08-30", "revenue": 303154.0, "net_income": 9226.0, "operating_cash_flow": 15817.0,
                 "capital_spending": 6435.0, "equity": 35803.0, "roe": 25.8, "owner_earnings": 9382.0}]
        self.assertIn("9382.0", printed_numbers(rows, {}))
        self.assertEqual(display(None), "not found")

    def test_hand_typed_memo_number_is_flagged(self):
        rows = [{"fiscal_year_end": "2026-08-30", "revenue": 303154.0, "net_income": 9226.0, "operating_cash_flow": 15817.0,
                 "capital_spending": 6435.0, "equity": 35803.0, "roe": 25.8, "owner_earnings": 9382.0}]
        self.assertEqual(unprinted_memo_numbers("ROE was 25.8%.", rows, {}), [])
        self.assertEqual(unprinted_memo_numbers("ROE was 40.0%.", rows, {}), ["40.0"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
