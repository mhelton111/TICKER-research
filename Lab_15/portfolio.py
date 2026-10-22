"""Lab 15 portfolio engine. Run with: python portfolio.py"""

import csv
from itertools import product
from math import sqrt


# Meridian's course-authored training inputs. Values are decimals.
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

OBJECTIVE_RETURN = 0.065
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
        left: {right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
               for right in sleeves}
        for left in sleeves
    }


def expected_return(weights, sleeves):
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_variance(weights, covariance):
    return sum(weights[left] * weights[right] * covariance[left][right]
               for left in weights for right in weights)


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


def search_lowest_risk_mix(sleeves, correlations, objective_return, eligible_sleeves=(), minimum_reserve=0.0, step=0.05):
    """Try each long-only, step-sized mix and return the feasible mix with least volatility."""
    validate_correlations(sleeves, correlations)
    if not 0 < step <= 1 or round(1 / step) * step != 1:
        raise ValueError("Step must divide 100% exactly.")
    if set(eligible_sleeves).difference(sleeves):
        raise ValueError("Reserve-eligible assets must be in sleeves.")
    names = tuple(sleeves)
    units = round(1 / step)
    covariance = covariance_matrix(sleeves, correlations)
    best = None
    for first_weights in product(range(units + 1), repeat=len(names) - 1):
        final_weight = units - sum(first_weights)
        if final_weight < 0:
            continue
        weights = dict(zip(names, (round(weight * step, 12) for weight in (*first_weights, final_weight))))
        result_return = expected_return(weights, sleeves)
        reserve_weight = reserve_eligible_weight(weights, eligible_sleeves)
        if result_return < objective_return or reserve_weight < minimum_reserve:
            continue
        volatility = portfolio_volatility(weights, covariance)
        candidate = {"weights": weights, "return": result_return, "volatility": volatility,
                     "reserve_weight": reserve_weight}
        if best is None or candidate["volatility"] < best["volatility"]:
            best = candidate
    return best


def _read_price_rows(source):
    if hasattr(source, "read"):
        content = source.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")
        return list(csv.DictReader(content.splitlines()))
    with open(source, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def estimate_from_csv(source, last_36_months=False):
    """Estimate annual returns, volatilities, and correlations from monthly price CSV data."""
    rows = _read_price_rows(source)
    if not rows or not rows[0] or "Date" not in rows[0]:
        raise ValueError("CSV needs a Date column followed by one price column per ticker.")
    names = tuple(name for name in rows[0] if name != "Date")
    if len(rows) < 37 and last_36_months:
        raise ValueError("The last-36-month option needs at least 37 monthly prices.")
    rows = rows[-37:] if last_36_months else rows
    if len(rows) < 2:
        raise ValueError("CSV needs at least two monthly prices.")
    returns = {}
    for name in names:
        prices = [float(row[name]) for row in rows]
        if any(price <= 0 for price in prices):
            raise ValueError("Prices must be positive numbers.")
        returns[name] = [prices[index] / prices[index - 1] - 1 for index in range(1, len(prices))]
    means = {name: sum(values) / len(values) for name, values in returns.items()}
    if len(next(iter(returns.values()))) < 2:
        raise ValueError("CSV needs at least three monthly prices for sample volatility.")
    sleeves = {
        name: {"label": name, "return": means[name] * 12,
               "volatility": sqrt(sum((value - means[name]) ** 2 for value in values) / (len(values) - 1)) * sqrt(12)}
        for name, values in returns.items()
    }
    correlations = {}
    for left in names:
        correlations[left] = {}
        for right in names:
            numerator = sum((a - means[left]) * (b - means[right]) for a, b in zip(returns[left], returns[right]))
            denominator = sqrt(sum((a - means[left]) ** 2 for a in returns[left]) * sum((b - means[right]) ** 2 for b in returns[right]))
            correlations[left][right] = numerator / denominator if denominator else (1.0 if left == right else 0.0)
    return sleeves, correlations


def main():
    validate_correlations(SLEEVES, CORRELATIONS)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    for name, weights in build_portfolios(SLEEVES).items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN, RESERVE_ELIGIBLE)


if __name__ == "__main__":
    main()
