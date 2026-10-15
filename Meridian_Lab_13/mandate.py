"""Lab 13 — Meridian Foundation mandate checker (standard library only)."""

from __future__ import annotations

import argparse


# Editable inputs: all weights are percent of the portfolio; reserve size is USD millions.
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # AI-proposed test portfolio: passes the mechanical rules but exposes S9.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 97, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def candidate_with_all_holdings(weights: dict[str, float]) -> dict[str, float]:
    """Return every holding, assigning zero to an omitted holding."""
    unknown = set(weights).difference(HOLDINGS)
    if unknown:
        raise ValueError(f"Unknown holding(s): {sorted(unknown)}")
    return {holding: float(weights.get(holding, 0.0)) for holding in HOLDINGS}


def issuer_exposures(weights: dict[str, float]) -> dict[str, float]:
    exposures: dict[str, float] = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            exposures[issuer] = exposures.get(issuer, 0.0) + weight
    return exposures


def report_candidate(name: str, entered_weights: dict[str, float], reserve_minimum: float) -> None:
    weights = candidate_with_all_holdings(entered_weights)
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight for holding, weight in weights.items() if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight for holding, weight in weights.items()
        if HOLDINGS[holding]["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )
    company_exposures = issuer_exposures(weights)
    largest_company = max(company_exposures.values(), default=0.0)

    checks = [
        ("Weights sum to 100", total_weight, abs(total_weight - 100.0) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0.0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company, largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failed_checks = 0
    for label, value, passed in checks:
        status = "pass" if passed else "FAIL"
        print(f"{label}: {value:.1f} {status}")
        failed_checks += not passed
    print("Calendar-year loss: requires CIO clarification")
    if failed_checks:
        print(f"Verdict: fails {failed_checks} rule(s)")
    else:
        print("Verdict: passes every checkable rule")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Meridian Foundation candidate portfolios.")
    parser.add_argument(
        "--probe",
        action="store_true",
        help="replace candidate A with the Lab 13 negative-cash known-answer probe",
    )
    args = parser.parse_args()

    candidates = dict(CANDIDATES)
    if args.probe:
        candidates["A"] = dict(CANDIDATES["A"], Cash=-2, **{"Global equity index fund": 64})

    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100.0
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in candidates.items():
        report_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
