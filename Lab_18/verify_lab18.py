"""Replay Lab 18's COST known-answer and JPM missing-input checks from SEC snapshots."""

import json
from pathlib import Path

from edgar_buffett import analysis_for_ticker, unprinted_memo_numbers


RAW = Path("raw_data")
TICKERS = json.loads((RAW / "company_tickers.json").read_text(encoding="utf-8"))


def saved_analysis(ticker):
    facts = json.loads((RAW / f"{ticker}_companyfacts.json").read_text(encoding="utf-8"))
    return analysis_for_ticker(ticker, facts=facts, ticker_map=TICKERS)


def main():
    cost = saved_analysis("COST")
    expected = [
        ("2022-08-28", 226954.0, 5844.0, 7392.0, 3891.0, 20642.0, 28.3, 3501.0),
        ("2023-09-03", 242290.0, 6292.0, 11068.0, 4323.0, 25058.0, 25.1, 6745.0),
        ("2024-09-01", 254453.0, 7367.0, 11339.0, 4710.0, 23622.0, 31.2, 6629.0),
        ("2025-08-31", 275235.0, 8099.0, 13335.0, 5498.0, 29164.0, 27.8, 7837.0),
        ("2026-08-30", 303154.0, 9226.0, 15817.0, 6435.0, 35803.0, 25.8, 9382.0),
    ]
    for row, values in zip(cost["rows"], expected):
        actual = (row["fiscal_year_end"], row["revenue"], row["net_income"], row["operating_cash_flow"], row["capital_spending"], row["equity"], round(row["roe"], 1), row["owner_earnings"])
        assert actual == values, f"COST mismatch: {actual} != {values}"
    assert set(cost["checks"].values()) == {"pass"}
    assert unprinted_memo_numbers(cost["memo"], cost["rows"], cost["checks"]) == []
    print("PASS COST: five rows, three checks, and memo-number guard match the known answer.")

    jpm = saved_analysis("JPM")
    assert all(row["capital_spending"] is None for row in jpm["rows"])
    assert jpm["checks"]["Owner earnings positive every year"] == "not known"
    assert jpm["checks"]["Owner earnings grew, first year to last"] == "not known"
    print("PASS JPM: capital spending and owner earnings remain not found/not known.")


if __name__ == "__main__":
    main()
