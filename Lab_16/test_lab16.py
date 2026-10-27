"""Regression checks for the Lab 16 known answer and later-date crossover."""

from datetime import date
import unittest

import asof


class Lab16Tests(unittest.TestCase):
    def test_required_funnel_and_asof_panel(self):
        panel, funnel = asof.apply_rules(asof.ROWS, date(2026, 3, 31))
        self.assertEqual([[row["row"] for row in removed] for _, removed in funnel], [[11], [7], [3, 8, 10], [2]])
        self.assertEqual([row["row"] for row in sorted(panel, key=lambda row: row["row"])], [1, 4, 5, 6, 9, 12])

    def test_known_asof_signals(self):
        panel, _ = asof.apply_rules(asof.ROWS, date(2026, 3, 31))
        result = asof.signals(panel)
        expected = {"AAA": ("2026-02", 1.980198019801982),
                    "BBB": ("2026-02", -1.0204081632653068),
                    "CCC": ("2026-02", 0.9090909090909038)}
        for ticker, (month, change) in expected.items():
            self.assertEqual(result[ticker][0], month)
            self.assertAlmostEqual(result[ticker][1], change, places=12)

    def test_later_date_equals_naive_signals(self):
        panel, _ = asof.apply_rules(asof.ROWS, date(2026, 4, 15))
        valid_rows = [row for row in asof.ROWS if row["ticker"]]
        valid_rows, _ = asof.remove_exact_duplicates(valid_rows)
        naive, _ = asof.latest_publication_per_month(valid_rows)
        self.assertEqual(asof.signals(panel), asof.signals(naive))


if __name__ == "__main__":
    unittest.main(verbosity=2)
