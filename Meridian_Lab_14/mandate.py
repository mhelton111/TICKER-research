"""Meridian Lab 13 mandate checker, extended with Lab 14 Candidate E."""

HOLDINGS = {
    "Cash": ("none", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

CANDIDATES = {
    "A": {"Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10, "Global equity index fund": 60, "Investment-grade bond fund": 26, "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
    "B": {"Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0, "Global equity index fund": 55, "Investment-grade bond fund": 20, "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4},
    "C": {"Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0, "Global equity index fund": 70, "Investment-grade bond fund": 20, "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8},
    # Lab 14 candidate E: Meridian benchmark, 40% IG bonds / 60% global equity.
    "E (Lab 14 benchmark)": {"Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0, "Global equity index fund": 60, "Investment-grade bond fund": 40, "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
}

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def reserve_minimum(reserve_size, quarterly_distribution, quarters_to_cover):
    return quarters_to_cover * quarterly_distribution / reserve_size * 100


def weights_sum(weights):
    return sum(weights.values())


def lowest_weight(weights):
    return min(weights.values())


def reserve_eligible_weight(weights, holdings):
    return sum(weights[name] for name, (_, _, eligible) in holdings.items() if eligible)


def liquid_weight(weights, holdings, liquidity_window):
    return sum(weights[name] for name, (_, days, _) in holdings.items() if days <= liquidity_window)


def largest_single_company_weight(weights, holdings, exempt_issuers):
    issuer_totals = {}
    for holding, weight in weights.items():
        issuer = holdings[holding][0]
        if issuer not in exempt_issuers:
            issuer_totals[issuer] = issuer_totals.get(issuer, 0) + weight
    return max(issuer_totals.values(), default=0.0)


def check_candidate(weights):
    reserve_floor = reserve_minimum(RESERVE_SIZE, QUARTERLY_DISTRIBUTION, QUARTERS_TO_COVER)
    checks = [
        ("Weights sum to 100", weights_sum(weights), weights_sum(weights) == 100.0),
        ("Long-only (lowest weight)", lowest_weight(weights), lowest_weight(weights) >= 0.0),
        (f"Reserve >= {reserve_floor:.1f}%", reserve_eligible_weight(weights, HOLDINGS), reserve_eligible_weight(weights, HOLDINGS) >= reserve_floor),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.0f}%", liquid_weight(weights, HOLDINGS, LIQUIDITY_WINDOW), liquid_weight(weights, HOLDINGS, LIQUIDITY_WINDOW) >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.0f}%", largest_single_company_weight(weights, HOLDINGS, EXEMPT_ISSUERS), largest_single_company_weight(weights, HOLDINGS, EXEMPT_ISSUERS) <= ISSUER_LIMIT),
    ]
    return checks


def print_candidate(name, weights):
    print(f"\nCandidate {name}")
    failed = 0
    for label, value, passed in check_candidate(weights):
        verdict = "pass" if passed else "FAIL"
        print(f"  {label}: {value:.1f} {verdict}")
        failed += not passed
    print("  Calendar-year loss: requires CIO clarification")
    if failed:
        print(f"  Verdict: fails {failed} rule(s)")
    else:
        print("  Verdict: passes every checkable rule")


def main():
    floor = reserve_minimum(RESERVE_SIZE, QUARTERLY_DISTRIBUTION, QUARTERS_TO_COVER)
    print(f"Reserve minimum: {floor:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        print_candidate(name, weights)


if __name__ == "__main__":
    main()
