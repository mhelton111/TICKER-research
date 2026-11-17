"""Reproducible long-only portfolio calculations for Project 2 readiness."""

import csv
from itertools import product
from math import sqrt


TICKERS = ("BIL", "IEF", "LQD", "VTI", "XLV")
RESERVE_TICKERS = ("BIL", "IEF")
OBJECTIVE_RETURN = 0.065
MINIMUM_RESERVE = 0.03


def load_estimates(path):
    """Convert saved monthly adjusted closes to annualized arithmetic estimates."""
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 3:
        raise ValueError("At least three monthly prices are required.")
    names = tuple(name for name in rows[0] if name != "Date" and name in TICKERS)
    returns = {}
    for name in names:
        prices = [float(row[name]) for row in rows]
        if any(price <= 0 for price in prices):
            raise ValueError("Prices must be positive.")
        returns[name] = [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]
    means = {name: sum(values) / len(values) for name, values in returns.items()}
    sleeves = {
        name: {"return": means[name] * 12,
               "volatility": sqrt(sum((x - means[name]) ** 2 for x in returns[name]) / (len(returns[name]) - 1)) * sqrt(12)}
        for name in names
    }
    correlations = {}
    for left in names:
        correlations[left] = {}
        for right in names:
            top = sum((a - means[left]) * (b - means[right]) for a, b in zip(returns[left], returns[right]))
            bottom = sqrt(sum((a - means[left]) ** 2 for a in returns[left]) * sum((b - means[right]) ** 2 for b in returns[right]))
            correlations[left][right] = top / bottom if bottom else (1.0 if left == right else 0.0)
    return sleeves, correlations


def evaluate(weights, sleeves, correlations):
    """Return annualized estimated return, volatility, and liquid-reserve weight."""
    expected = sum(weights[name] * sleeves[name]["return"] for name in sleeves)
    variance = sum(weights[a] * weights[b] * correlations[a][b] * sleeves[a]["volatility"] * sleeves[b]["volatility"]
                   for a in sleeves for b in sleeves)
    reserve = sum(weights.get(name, 0.0) for name in RESERVE_TICKERS)
    return {"weights": weights, "return": expected, "volatility": sqrt(max(variance, 0.0)), "reserve": reserve}


def verdict(result, objective=OBJECTIVE_RETURN, minimum_reserve=MINIMUM_RESERVE):
    failures = []
    if result["return"] < objective:
        failures.append("misses return objective")
    if result["reserve"] < minimum_reserve:
        failures.append("misses reserve minimum")
    return "PASS" if not failures else "FAIL — " + "; ".join(failures)


def equal_weight(sleeves):
    return {name: 1 / len(sleeves) for name in sleeves}


def benchmark(sleeves):
    """Transparent 60/40 equity benchmark: 60% VTI, 40% LQD."""
    return {name: {"LQD": .40, "VTI": .60}.get(name, 0.0) for name in sleeves}


def optimize(sleeves, correlations, objective=OBJECTIVE_RETURN, minimum_reserve=MINIMUM_RESERVE, step=.05):
    """Select the lowest-volatility long-only 5-point mix satisfying the mandate."""
    names = tuple(sleeves)
    units = round(1 / step)
    best = None
    for prefix in product(range(units + 1), repeat=len(names) - 1):
        final = units - sum(prefix)
        if final < 0:
            continue
        weights = dict(zip(names, [x * step for x in (*prefix, final)]))
        candidate = evaluate(weights, sleeves, correlations)
        if candidate["return"] >= objective and candidate["reserve"] >= minimum_reserve:
            if best is None or candidate["volatility"] < best["volatility"]:
                best = candidate
    return best
