"""Lab 14 portfolio baseline risk engine. Run with: python portfolio.py"""

from math import sqrt

# Editable course-authored inputs. Returns and volatilities are decimals.
SLEEVES = {
    "bills": {"label": "Treasury bills", "return": 0.035, "volatility": 0.005},
    "ten_year": {"label": "Treasury 10-year note", "return": 0.043, "volatility": 0.070},
    "ig_bonds": {"label": "Investment-grade bond fund", "return": 0.050, "volatility": 0.060},
    "equity": {"label": "Global equity index fund", "return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "bills": {"bills": 1.00, "ten_year": 0.10, "ig_bonds": 0.05, "equity": 0.00},
    "ten_year": {"bills": 0.10, "ten_year": 1.00, "ig_bonds": 0.80, "equity": -0.10},
    "ig_bonds": {"bills": 0.05, "ten_year": 0.80, "ig_bonds": 1.00, "equity": 0.25},
    "equity": {"bills": 0.00, "ten_year": -0.10, "ig_bonds": 0.25, "equity": 1.00},
}

OBJECTIVE_RETURN = 0.065  # CPI estimate 2.5% + 4.0%
RESERVE_ELIGIBLE = ("bills", "ten_year")


def validate_correlations(sleeves, correlations):
    """Reject correlations outside [-1, 1], missing cells, and asymmetric tables."""
    names = tuple(sleeves)
    if set(correlations) != set(names):
        raise ValueError("Correlation table must contain exactly the sleeve names.")
    for left in names:
        if set(correlations[left]) != set(names):
            raise ValueError(f"Correlation row for {left} must contain every sleeve.")
        for right in names:
            value = correlations[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Correlation {left}/{right} = {value} is outside [-1, 1].")
            if value != correlations[right][left]:
                raise ValueError(f"Correlation table is not symmetric at {left}/{right}.")


def covariance_matrix(sleeves, correlations):
    """Build covariance = correlation x volatility x volatility."""
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_variance(weights, covariance):
    return sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in weights
        for right in weights
    )


def portfolio_volatility(weights, covariance):
    return sqrt(portfolio_variance(weights, covariance))


def reserve_eligible_weight(weights, eligible_sleeves):
    return sum(weights[name] for name in eligible_sleeves)


def equal_weight(sleeves):
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_weight(sleeves):
    inverse_vols = {name: 1 / sleeves[name]["volatility"] for name in sleeves}
    total = sum(inverse_vols.values())
    return {name: inverse_vols[name] / total for name in sleeves}


def build_portfolios(sleeves):
    return {
        "Benchmark": {"bills": 0.0, "ten_year": 0.0, "ig_bonds": 0.40, "equity": 0.60},
        "Equal weight": equal_weight(sleeves),
        "Inverse volatility": inverse_volatility_weight(sleeves),
    }


def print_portfolio(name, weights, sleeves, covariance, objective_return, eligible_sleeves):
    labels = " / ".join(f"{weights[key] * 100:.1f}" for key in sleeves)
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights, eligible_sleeves)
    meets_objective = "yes" if result_return >= objective_return else "no"
    print(name)
    print(f"  weights (bills / 10-year / IG / equity): {labels}")
    print(f"  expected return: {result_return * 100:.2f}%")
    print(f"  volatility: {result_volatility * 100:.2f}%")
    print(f"  reserve-eligible: {reserve_weight * 100:.1f}%")
    print(f"  meets {objective_return * 100:.1f}% objective: {meets_objective}")


def main():
    validate_correlations(SLEEVES, CORRELATIONS)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    for name, weights in build_portfolios(SLEEVES).items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN, RESERVE_ELIGIBLE)


if __name__ == "__main__":
    main()
