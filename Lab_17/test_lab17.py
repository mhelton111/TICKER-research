"""Focused, offline regression tests for Lab 17's calculation layer."""

import unittest

import pandas as pd

import asof_core


class Lab17Tests(unittest.TestCase):
    def test_parser_turns_dot_into_missing_and_sorts_dates(self):
        values = asof_core.parse_fred_csv("observation_date,BAA\n2026-02-01,.\n2026-01-01,6.1\n", "BAA")
        self.assertEqual(values.index.tolist(), [pd.Timestamp("2026-01-01")])
        self.assertEqual(float(values.iloc[0, 0]), 6.1)

    def test_audit_counts_lag_and_revisions(self):
        vintage = pd.DataFrame({"value": [1.0, 2.0]}, index=pd.to_datetime(["2026-01-01", "2026-02-01"]))
        today = pd.DataFrame({"value": [1.0, 2.5, 3.0]}, index=pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"]))
        audit = asof_core.calculate_audit(today, vintage, "2026-02-15")
        self.assertEqual(audit["last_known_date"], pd.Timestamp("2026-02-01"))
        self.assertEqual(audit["published_later_count"], 1)
        self.assertEqual(audit["revised_count"], 1)

    def test_invalid_series_id_rejected(self):
        with self.assertRaises(ValueError):
            asof_core.clean_series_id("BAA&other=PAYEMS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
