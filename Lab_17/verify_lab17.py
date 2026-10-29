"""Verify Lab 17's required point-in-time checks from preserved raw downloads.

Run: python verify_lab17.py
The CSV snapshots in raw_data were downloaded from the public FRED/ALFRED URLs
listed in SOURCES.md on 2026-10-29.
"""

from pathlib import Path

from asof_core import calculate_audit, parse_fred_csv


RAW = Path("raw_data")
KNOWN_ANSWER = {
    "BAA": ("BAA_2026-10-05.csv", "2026-09-01", 6.47),
    "FEDFUNDS": ("FEDFUNDS_2026-10-05.csv", "2026-09-01", 3.75),
    "DGS10": ("DGS10_2026-10-05.csv", "2026-10-02", 5.28),
    "MORTGAGE30US": ("MORTGAGE30US_2026-10-05.csv", "2026-10-01", 7.28),
}


def read_snapshot(filename, series_id):
    return parse_fred_csv((RAW / filename).read_text(encoding="utf-8"), series_id)


def main():
    print("Lab 17 known-answer check: ALFRED vintage date 2026-10-05")
    for series_id, (filename, expected_date, expected_value) in KNOWN_ANSWER.items():
        values = read_snapshot(filename, series_id)
        actual_date = values.index.max().date().isoformat()
        actual_value = float(values.iloc[-1]["value"])
        assert actual_date == expected_date, f"{series_id}: expected date {expected_date}, got {actual_date}"
        assert actual_value == expected_value, f"{series_id}: expected {expected_value}, got {actual_value}"
        print(f"  PASS {series_id}: {actual_date} = {actual_value:,.2f}")

    vintage = read_snapshot("PAYEMS_2025-01-15.csv", "PAYEMS")
    current = read_snapshot("PAYEMS_current.csv", "PAYEMS")
    audit = calculate_audit(current, vintage, "2025-01-15")
    old_value = float(vintage.loc["2024-12-01", "value"])
    current_value = float(current.loc["2024-12-01", "value"])
    assert old_value == 159536, f"Expected PAYEMS vintage value 159536, got {old_value}"
    assert current_value < old_value, "Current PAYEMS value should be lower than its January 2025 vintage."
    assert audit["revised_count"] > 0, "PAYEMS revision count should be above zero."
    print("PAYEMS probe: PASS")
    print(f"  December 2024 known on 2025-01-15: {old_value:,.0f}")
    print(f"  December 2024 current value: {current_value:,.0f}")
    print(f"  Same-date revised observations: {audit['revised_count']}")


if __name__ == "__main__":
    main()
