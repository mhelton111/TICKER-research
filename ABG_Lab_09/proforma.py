"""Lab 09 ABG pro-forma engine. Run: python proforma.py"""


YEARS = [2026, 2027, 2028, 2029, 2030]

# Assumptions (USD millions except percentages and shares)
ORGANIC_REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_AS_PERCENT_OF_GROSS_PROFIT = [0.665, 0.655, 0.645, 0.645, 0.645]
DEPRECIATION_AS_PERCENT_OF_OPENING_PPE = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_AS_PERCENT_OF_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# FY2025 opening balance sheet (USD millions)
OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

# Leave empty for the working model. Example break test: {2026: 40.4}.
CASH_OVERRIDES: dict[int, float] = {}


def assert_balanced(year: int, gap: float, cash: float) -> None:
    """Reject a year whose balance sheet does not balance or misses minimum cash."""
    if abs(gap) > 0.05:
        raise ValueError(f"FY{year}E is not balanced: assets - liabilities - equity = {gap:.1f}")
    if cash + 0.05 < MINIMUM_CASH:
        raise ValueError(f"FY{year}E cash is below the minimum: {cash:.1f} < {MINIMUM_CASH:.1f}")


def project_year(year: int, opening: dict[str, float], sga_ratio: float) -> dict[str, float]:
    """Project one year in the calculation order specified by the Lab 09 handout."""
    revenue = opening["revenue"] * (1 + ORGANIC_REVENUE_GROWTH)
    gross_profit = revenue * GROSS_MARGIN
    sga = gross_profit * sga_ratio
    depreciation = opening["ppe"] * DEPRECIATION_AS_PERCENT_OF_OPENING_PPE
    impairment = IMPAIRMENT
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (
        opening["floor_plan"] * FLOOR_PLAN_RATE
        + opening["term_debt"] * TERM_DEBT_RATE
        + opening["revolver"] * REVOLVER_RATE
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
    floor_plan = inventory * FLOOR_PLAN_AS_PERCENT_OF_INVENTORY
    ppe = opening["ppe"] + CAPEX - depreciation
    revenue_change = revenue - opening["revenue"]
    other_working_capital_change = OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE * revenue_change
    other_assets = opening["other_assets"] + other_working_capital_change - impairment
    term_debt = opening["term_debt"] - DEBT_REPAYMENT
    other_liabilities = opening["other_liabilities"]
    equity = opening["equity"] + net_income - SHARE_BUYBACK

    fcfe = (
        net_income
        + depreciation
        + impairment
        - CAPEX
        - (inventory - opening["inventory"])
        - other_working_capital_change
        + (floor_plan - opening["floor_plan"])
        - DEBT_REPAYMENT
    )
    cash_before_revolver = opening["cash"] + fcfe - SHARE_BUYBACK
    revolver = opening["revolver"]
    if cash_before_revolver < MINIMUM_CASH:
        draw = MINIMUM_CASH - cash_before_revolver
        if revolver + draw > REVOLVER_LIMIT:
            raise ValueError(f"FY{year}E requires revolver borrowing above the {REVOLVER_LIMIT:.1f} limit.")
        revolver += draw
        cash = MINIMUM_CASH
    else:
        repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
        revolver -= repayment
        cash = cash_before_revolver - repayment

    if year in CASH_OVERRIDES:
        cash = CASH_OVERRIDES[year]

    assets = inventory + ppe + other_assets + cash
    liabilities = floor_plan + term_debt + revolver + other_liabilities
    gap = assets - liabilities - equity
    if abs(gap) <= 0.05:
        gap = 0.0
    assert_balanced(year, gap, cash)
    return {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": impairment,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash": cash,
        "floor_plan": floor_plan,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
        "fcfe": fcfe,
        "other_working_capital_change": other_working_capital_change,
        "capex": CAPEX,
        "change_inventory": inventory - opening["inventory"],
        "change_floor_plan": floor_plan - opening["floor_plan"],
        "debt_repayment": DEBT_REPAYMENT,
        "share_buyback": SHARE_BUYBACK,
        "assets": assets,
        "liabilities": liabilities,
        "gap": gap,
    }


def print_table(title: str, rows: list[tuple[str, str]], projections: dict[int, dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
    for label, key in rows:
        print(f"{label:<34}" + "".join(f"{projections[year][key]:>12.1f}" for year in YEARS))


def main() -> None:
    projections: dict[int, dict[str, float]] = {}
    opening = OPENING.copy()
    for year, sga_ratio in zip(YEARS, SGA_AS_PERCENT_OF_GROSS_PROFIT):
        projection = project_year(year, opening, sga_ratio)
        projections[year] = projection
        opening = {**opening, **projection}

    print_table(
        "Income Statement",
        [
            ("Revenue", "revenue"),
            ("Gross profit", "gross_profit"),
            ("SG&A", "sga"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Operating income", "operating_income"),
            ("Interest", "interest"),
            ("Pretax income", "pretax_income"),
            ("Tax", "tax"),
            ("Net income", "net_income"),
        ],
        projections,
    )
    print_table(
        "Balance Sheet",
        [
            ("Inventory", "inventory"),
            ("PP&E", "ppe"),
            ("Other assets", "other_assets"),
            ("Cash", "cash"),
            ("Total assets", "assets"),
            ("Floor plan", "floor_plan"),
            ("Term debt", "term_debt"),
            ("Revolver", "revolver"),
            ("Other liabilities", "other_liabilities"),
            ("Equity", "equity"),
            ("Total liabilities", "liabilities"),
        ],
        projections,
    )
    print_table(
        "Cash Flow / FCFE",
        [
            ("Net income", "net_income"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Capital spending", "capex"),
            ("Change in inventory", "change_inventory"),
            ("Change in other working capital", "other_working_capital_change"),
            ("Change in floor plan", "change_floor_plan"),
            ("Debt repayment", "debt_repayment"),
            ("Share buyback", "share_buyback"),
            ("Free cash flow to equity", "fcfe"),
        ],
        projections,
    )
    print("\nChecks")
    print(f"{'Check':<34}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
    print(f"{'Assets - liabilities - equity':<34}" + "".join(f"{projections[year]['gap']:>12.1f}" for year in YEARS))
    print(f"{'Cash at or above minimum':<34}" + "".join(f"{'yes' if projections[year]['cash'] >= MINIMUM_CASH else 'no':>12}" for year in YEARS))

    present_value_fcfe = sum(
        projections[year]["fcfe"] / (1 + COST_OF_EQUITY) ** index
        for index, year in enumerate(YEARS, start=1)
    )
    terminal_value_2030 = (
        (projections[2030]["fcfe"] + DEBT_REPAYMENT)
        * (1 + TERMINAL_GROWTH)
        / (COST_OF_EQUITY - TERMINAL_GROWTH)
    )
    present_value_terminal = terminal_value_2030 / (1 + COST_OF_EQUITY) ** len(YEARS)
    equity_value = present_value_fcfe + present_value_terminal
    after_2030_share = present_value_terminal / equity_value
    value_per_share = equity_value / SHARES_OUTSTANDING
    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:.1f} million")
    print(f"Share of value after 2030: {after_2030_share:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")


if __name__ == "__main__":
    main()
