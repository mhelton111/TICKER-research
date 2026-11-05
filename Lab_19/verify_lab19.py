"""Replay Lab 19's COST known answer, threshold probe, and LLY panel from SEC snapshots."""

import json
from pathlib import Path

from legend_panel import analyze, unprinted_numbers


RAW = Path("raw_data")
TICKERS = json.loads((RAW / "company_tickers.json").read_text(encoding="utf-8"))


def saved(ticker):
    facts = json.loads((RAW / f"{ticker}_companyfacts.json").read_text(encoding="utf-8"))
    return facts


def main():
    cost = analyze("COST", saved("COST"), TICKERS)
    current_ratios = [round(row["current_ratio"], 2) for row in cost["rows"]]
    leverage = [round(row["liabilities_to_equity"], 2) for row in cost["rows"]]
    assert current_ratios == [1.02, 1.07, 0.97, 1.03, 1.06]
    assert leverage == [2.11, 1.75, 1.96, 1.64, 1.49]
    assert list(cost["checks"]["Buffett"].values()) == ["pass", "pass", "pass"]
    assert list(cost["checks"]["Graham"].values()) == ["fail", "pass", "pass"]
    assert list(cost["checks"]["Burry"].values()) == ["pass", "pass"]
    assert all(not flags for flags in cost["memo_flags"].values())
    print("PASS COST: ratios, panel checks, and all three memo-number guards match the known answer.")

    probe = analyze("COST", saved("COST"), TICKERS, graham_threshold=1.0)
    assert list(probe["checks"]["Graham"].values()) == ["pass", "pass", "pass"]
    print("PASS threshold probe: Graham passes COST at a 1.0 current-ratio threshold.")

    lly = analyze("LLY", saved("LLY"), TICKERS)
    assert any(row["liabilities"] is None for row in lly["rows"])
    assert lly["checks"]["Burry"]["Liabilities no more than twice equity, latest year"] == "not known"
    assert all(not flags for flags in lly["memo_flags"].values())
    print("PASS LLY: missing facts stay visible and dependent Burry check is not known.")

    altered = dict(cost["memos"])
    altered["Graham"] += "\nHand-added ratio: 40.0.\n"
    assert unprinted_numbers(altered, cost["rows"], cost["graham_threshold"])["Graham"] == ["40.0"]
    print("PASS number guard: an unsupported 40.0 in any investor memo is flagged.")


if __name__ == "__main__":
    main()
