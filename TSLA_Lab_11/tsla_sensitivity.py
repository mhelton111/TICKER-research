"""Lab 11 — TSLA one-at-a-time sensitivity built from the Lab 10 pro forma.

Amounts are USD millions except per-share amounts. Run: python tsla_sensitivity.py
"""
from copy import deepcopy
from math import isclose

YEARS = [2026, 2027, 2028, 2029, 2030]
BASE = {
    "revenue_growth": [0.06, 0.10, 0.12, 0.12, 0.10],
    "gross_margin": [0.18, 0.20, 0.22, 0.24, 0.26],
}
LOW = {
    "revenue_growth": [0.04, 0.08, 0.10, 0.10, 0.08],
    "gross_margin": [0.16, 0.18, 0.20, 0.22, 0.24],
}
HIGH = {
    "revenue_growth": [0.08, 0.12, 0.14, 0.14, 0.12],
    "gross_margin": [0.20, 0.22, 0.24, 0.26, 0.28],
}

# FY2025 opening balances from Tesla 2025 Form 10-K, p. 49.
OPENING_CASH = 44_059.0  # cash and equivalents plus short-term investments
OPENING_INVENTORY, OPENING_PPE, OPENING_OTHER_ASSETS = 12_392.0, 40_643.0, 40_712.0
OPENING_DEBT, OPENING_OTHER_LIABILITIES, OPENING_EQUITY = 8_376.0, 46_565.0, 82_865.0
RND_PCT, SGA_PCT_GP, TAX_RATE = 0.075, [0.33, 0.31, 0.29, 0.27, 0.25], 0.27
INVENTORY_DAYS, DEPR_PCT_PPE = [58, 56, 54, 53, 52], 0.124
CAPEX = [20_000, 17_000, 14_000, 12_000, 10_000]
OTHER_ASSET_PCT_CHANGE, OTHER_LIAB_PCT_CHANGE = 0.010, 0.015
INTEREST_INCOME_RATE, INTEREST_EXPENSE_RATE = 0.038, 0.040
WACC, TERMINAL_GROWTH, SHARES = 0.10, 0.03, 3_752.431984
MINIMUM_LIQUIDITY, REVOLVER_LIMIT = 2_000.0, 5_000.0


def run(inputs):
    """Run a fresh linked model. `inputs` is never mutated."""
    growth, margin = inputs["revenue_growth"][:], inputs["gross_margin"][:]
    revenue, cash, inventory, ppe = 94_827.0, OPENING_CASH, OPENING_INVENTORY, OPENING_PPE
    other_assets, debt, other_liabilities, equity = OPENING_OTHER_ASSETS, OPENING_DEBT, OPENING_OTHER_LIABILITIES, OPENING_EQUITY
    rows = []
    for i, year in enumerate(YEARS):
        prior_revenue = revenue
        revenue *= 1 + growth[i]
        gross_profit, cost_revenue = revenue * margin[i], revenue * (1 - margin[i])
        rnd, sga, depreciation = revenue * RND_PCT, gross_profit * SGA_PCT_GP[i], ppe * DEPR_PCT_PPE
        ebit = gross_profit - rnd - sga - depreciation
        pretax = ebit + cash * INTEREST_INCOME_RATE - debt * INTEREST_EXPENSE_RATE
        taxes = max(pretax, 0) * TAX_RATE
        net_income = pretax - taxes
        new_inventory = cost_revenue / 365 * INVENTORY_DAYS[i]
        new_ppe = ppe + CAPEX[i] - depreciation
        revenue_change = revenue - prior_revenue
        new_other_assets = other_assets + revenue_change * OTHER_ASSET_PCT_CHANGE
        new_other_liabilities = other_liabilities + revenue_change * OTHER_LIAB_PCT_CHANGE
        fcfe = net_income + depreciation - CAPEX[i] - (new_inventory - inventory) - (new_other_assets - other_assets) + (new_other_liabilities - other_liabilities)
        new_cash, new_debt, new_equity = cash + fcfe, debt, equity + net_income
        revolver_draw = 0.0
        if new_cash < MINIMUM_LIQUIDITY:
            revolver_draw = min(MINIMUM_LIQUIDITY - new_cash, REVOLVER_LIMIT)
            new_cash += revolver_draw
            new_debt += revolver_draw
        check = new_cash + new_inventory + new_ppe + new_other_assets - new_debt - new_other_liabilities - new_equity
        if not isclose(check, 0.0, abs_tol=0.01):
            raise AssertionError(f"{year} balance check failed: {check:.2f}")
        rows.append({"year": year, "revenue": revenue, "gross_profit": gross_profit, "ebit": ebit,
                     "net_income": net_income, "fcfe": fcfe, "cash": new_cash, "debt": new_debt,
                     "revolver_draw": revolver_draw, "balance_check": check})
        cash, inventory, ppe, other_assets, debt, other_liabilities, equity = new_cash, new_inventory, new_ppe, new_other_assets, new_debt, new_other_liabilities, new_equity
    pv_fcfe = sum(r["fcfe"] / (1 + WACC) ** (i + 1) for i, r in enumerate(rows))
    terminal_value = rows[-1]["fcfe"] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    equity_value = pv_fcfe + terminal_value / (1 + WACC) ** len(rows)
    return {"rows": rows, "operating_profit": rows[-1]["ebit"], "fcfe": rows[-1]["fcfe"],
            "value_per_share": equity_value / SHARES, "equity_value": equity_value}


def scenario(driver, level):
    inputs = deepcopy(BASE)
    if driver:
        inputs[driver] = {"low": LOW, "high": HIGH}[level][driver][:]
    return inputs, run(inputs)


def fmt(x): return f"${x:,.1f}"


if __name__ == "__main__":
    base_inputs, base = scenario(None, None)
    print("BASE (restored model)")
    print(base_inputs)
    print(f"2030 EBIT {fmt(base['operating_profit'])}; FCFE {fmt(base['fcfe'])}; value/share ${base['value_per_share']:.2f}")
    print("Base annual checks:", [round(r["balance_check"], 2) for r in base["rows"]])
    for driver in ("revenue_growth", "gross_margin"):
        print(f"\n{driver}")
        results = {}
        for level in ("low", "base", "high"):
            inputs, result = scenario(driver, level) if level != "base" else scenario(None, None)
            results[level] = result
            print(f"{level:4} input={inputs[driver]} | 2030 EBIT {fmt(result['operating_profit'])} | FCFE {fmt(result['fcfe'])} | value/share ${result['value_per_share']:.2f} | checks {[round(r['balance_check'], 2) for r in result['rows']]}")
        for output in ("operating_profit", "fcfe", "value_per_share"):
            vals = [results[x][output] for x in ("low", "base", "high")]
            print(f"{output} span: {max(vals) - min(vals):,.2f}")
    _, restored = scenario(None, None)
    assert isclose(restored["value_per_share"], base["value_per_share"], abs_tol=0.000001)
    print("\nRestored-base check: PASS")
