"""Lab 16: reproduce a point-in-time panel from the course training table.

Run: python asof.py
Only Python's standard library is used.  Change DECISION_DATE to test another
information set; the input table and calculations are never hard-coded answers.
"""

from collections import defaultdict
from datetime import date


DECISION_DATE = date.fromisoformat("2026-03-31")

# Course-authored fictional card-spend-index training table.
ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "index": 111.0},
]


def show_removal(label, removed):
    print(f"{label}: {len(removed)} removed; row(s): " + ", ".join(str(row["row"]) for row in removed))


def remove_exact_duplicates(rows):
    """Keep the first occurrence; compare data fields, never the source row number."""
    seen, kept, removed = set(), [], []
    for row in rows:
        fingerprint = (row["ticker"], row["month"], row["published"], row["index"])
        if fingerprint in seen:
            removed.append(row)
        else:
            seen.add(fingerprint)
            kept.append(row)
    return kept, removed


def latest_publication_per_month(rows):
    """For each ticker/month, retain the latest publication that passed the as-of gate."""
    groups = defaultdict(list)
    for row in rows:
        groups[(row["ticker"], row["month"])].append(row)
    kept, removed = [], []
    for group in groups.values():
        latest = max(group, key=lambda row: date.fromisoformat(row["published"]))
        kept.append(latest)
        removed.extend(row for row in group if row is not latest)
    return kept, removed


def apply_rules(rows, decision_date):
    """Apply the four course rules in their required order and return the audit trail."""
    no_ticker = [row for row in rows if not row["ticker"]]
    remaining = [row for row in rows if row["ticker"]]

    remaining, duplicates = remove_exact_duplicates(remaining)

    after_date = [row for row in remaining if date.fromisoformat(row["published"]) > decision_date]
    remaining = [row for row in remaining if date.fromisoformat(row["published"]) <= decision_date]

    panel, older_vintages = latest_publication_per_month(remaining)
    return panel, [("Quarantined: no ticker", no_ticker),
                   ("Exact duplicate", duplicates),
                   (f"Published after {decision_date.isoformat()}", after_date),
                   ("Older vintage replaced by a revision", older_vintages)]


def signals(panel):
    """Return latest month-over-month index changes by ticker when two months exist."""
    by_ticker = defaultdict(list)
    for row in panel:
        by_ticker[row["ticker"]].append(row)
    result = {}
    for ticker, ticker_rows in by_ticker.items():
        ordered = sorted(ticker_rows, key=lambda row: row["month"])
        if len(ordered) >= 2:
            previous, latest = ordered[-2:]
            result[ticker] = (latest["month"], (latest["index"] / previous["index"] - 1) * 100)
    return result


def print_panel(panel, heading):
    print(f"\n{heading}")
    print("row | ticker | month measured | published on | index")
    for row in sorted(panel, key=lambda item: item["row"]):
        print(f'{row["row"]:>3} | {row["ticker"]:<6} | {row["month"]} | {row["published"]} | {row["index"]:.1f}')


def print_signals(panel, heading):
    print(f"\n{heading}")
    for ticker, (month, change) in sorted(signals(panel).items()):
        print(f"{ticker}: {change:+.2f}% ({month})")


def main():
    panel, funnel = apply_rules(ROWS, DECISION_DATE)
    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print("Row funnel")
    for label, removed in funnel:
        show_removal(label, removed)
    print_panel(panel, "As-of panel")
    print_signals(panel, "As-of signals")

    # The naive comparison deliberately ignores publication date, but still
    # removes invalid/duplicate records and selects the latest vintage.
    valid_rows = [row for row in ROWS if row["ticker"]]
    valid_rows, _ = remove_exact_duplicates(valid_rows)
    naive_panel, _ = latest_publication_per_month(valid_rows)
    print_panel(naive_panel, "Naive panel (publication date ignored)")
    print_signals(naive_panel, "Naive signals")


if __name__ == "__main__":
    main()
