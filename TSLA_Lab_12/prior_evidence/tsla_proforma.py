"""Lab 10 — Tesla, Inc. (TSLA) pro forma and equity-value model.

Dollar amounts are USD millions except per-share amounts. Run: python tsla_proforma.py
"""
from math import isclose

# FY2025 opening balance sheet; Tesla 2025 Form 10-K, Consolidated Balance Sheets, p. 49.
# Cash includes cash equivalents plus short-term investments because both are liquid balances.
OPENING_CASH_AND_INVESTMENTS = 44_059.0
OPENING_INVENTORY = 12_392.0
OPENING_PPE = 40_643.0
OPENING_OTHER_ASSETS = 40_712.0
OPENING_DEBT_AND_FINANCE_LEASES = 8_376.0
OPENING_OTHER_LIABILITIES = 46_565.0
OPENING_EQUITY = 82_865.0

YEARS = [2026, 2027, 2028, 2029, 2030]
REVENUE_GROWTH = [0.06, 0.10, 0.12, 0.12, 0.10]
GROSS_MARGIN = [0.18, 0.20, 0.22, 0.24, 0.26]
R_AND_D_PCT_REVENUE = [0.075] * 5
SGA_PCT_GROSS_PROFIT = [0.33, 0.31, 0.29, 0.27, 0.25]
TAX_RATE = 0.27
INVENTORY_DAYS = [58, 56, 54, 53, 52]
DEPRECIATION_PCT_PPE = 0.124
CAPEX = [20_000, 17_000, 14_000, 12_000, 10_000]
OTHER_ASSET_PCT_REVENUE_CHANGE = 0.010
OTHER_LIABILITY_PCT_REVENUE_CHANGE = 0.015
INTEREST_INCOME_RATE = 0.038
INTEREST_EXPENSE_RATE = 0.040
DEBT_REPAYMENT = [0] * 5
MINIMUM_LIQUIDITY = 2_000.0
REVOLVER_LIMIT = 5_000.0
REVOLVER_RATE = 0.060

# Tesla has no dealership floor-plan financing. This is not an assumed zero operating ratio.
FLOOR_PLAN_FINANCING = 0.0

WACC = 0.10
TERMINAL_GROWTH = 0.03
SHARES = 3_752.431984  # common shares outstanding January 23, 2026; 2025 10-K cover.


def pv(amount, year):
    return amount / (1 + WACC) ** year


def build_model():
    rows = []
    revenue = 94_827.0
    cash, inventory, ppe = OPENING_CASH_AND_INVESTMENTS, OPENING_INVENTORY, OPENING_PPE
    other_assets, debt = OPENING_OTHER_ASSETS, OPENING_DEBT_AND_FINANCE_LEASES
    other_liabilities, equity = OPENING_OTHER_LIABILITIES, OPENING_EQUITY
    for i, year in enumerate(YEARS):
        opening_revenue = revenue
        revenue *= 1 + REVENUE_GROWTH[i]
        gross_profit = revenue * GROSS_MARGIN[i]
        cost_of_revenue = revenue - gross_profit
        rnd = revenue * R_AND_D_PCT_REVENUE[i]
        sga = gross_profit * SGA_PCT_GROSS_PROFIT[i]
        depreciation = ppe * DEPRECIATION_PCT_PPE
        interest_income = cash * INTEREST_INCOME_RATE
        interest_expense = debt * INTEREST_EXPENSE_RATE
        ebit = gross_profit - rnd - sga - depreciation
        pretax_income = ebit + interest_income - interest_expense
        taxes = max(pretax_income, 0) * TAX_RATE
        net_income = pretax_income - taxes

        new_inventory = cost_of_revenue / 365 * INVENTORY_DAYS[i]
        new_ppe = ppe + CAPEX[i] - depreciation
        delta_revenue = revenue - opening_revenue
        new_other_assets = other_assets + delta_revenue * OTHER_ASSET_PCT_REVENUE_CHANGE
        new_other_liabilities = other_liabilities + delta_revenue * OTHER_LIABILITY_PCT_REVENUE_CHANGE
        repayment = min(DEBT_REPAYMENT[i], debt)
        new_debt = debt - repayment
        fcfe = (net_income + depreciation - CAPEX[i] - (new_inventory - inventory)
                - (new_other_assets - other_assets) + (new_other_liabilities - other_liabilities)
                - repayment)
        new_cash = cash + fcfe
        revolver_draw = 0.0
        if new_cash < MINIMUM_LIQUIDITY:
            revolver_draw = min(MINIMUM_LIQUIDITY - new_cash, REVOLVER_LIMIT)
            new_cash += revolver_draw
            new_debt += revolver_draw
        new_equity = equity + net_income  # Tesla has no cash dividends in the filed history.
        check = new_cash + new_inventory + new_ppe + new_other_assets - new_debt - new_other_liabilities - new_equity
        if not isclose(check, 0.0, abs_tol=0.01):
            raise AssertionError(f"{year} does not balance: {check:.2f}")
        rows.append(dict(year=year, revenue=revenue, gross_profit=gross_profit, rnd=rnd, sga=sga,
                         ebit=ebit, net_income=net_income, depreciation=depreciation, capex=CAPEX[i],
                         inventory=new_inventory, ppe=new_ppe, cash=new_cash, debt=new_debt,
                         equity=new_equity, fcfe=fcfe, floor_plan=FLOOR_PLAN_FINANCING,
                         revolver_draw=revolver_draw, balance_check=check))
        cash, inventory, ppe, other_assets, debt, other_liabilities, equity = new_cash, new_inventory, new_ppe, new_other_assets, new_debt, new_other_liabilities, new_equity
    return rows


def value(rows):
    pv_fcfe = sum(pv(row["fcfe"], i + 1) for i, row in enumerate(rows))
    terminal_fcfe = rows[-1]["fcfe"] * (1 + TERMINAL_GROWTH)
    terminal_value = terminal_fcfe / (WACC - TERMINAL_GROWTH)
    equity_value = pv_fcfe + pv(terminal_value, len(rows))
    return pv_fcfe, terminal_value, equity_value, equity_value / SHARES


if __name__ == "__main__":
    rows = build_model()
    print("TSLA Lab 10 pro forma (USD millions except per-share data)")
    print("Year | Revenue | Net income | FCFE | Cash + investments | Debt | Equity | Balance check")
    for row in rows:
        print(f"{row['year']} | {row['revenue']:,.1f} | {row['net_income']:,.1f} | {row['fcfe']:,.1f} | {row['cash']:,.1f} | {row['debt']:,.1f} | {row['equity']:,.1f} | {row['balance_check']:,.1f}")
    pv_fcfe, terminal_value, equity_value, per_share = value(rows)
    print(f"\nPV explicit FCFE: ${pv_fcfe:,.1f}\nTerminal value: ${terminal_value:,.1f}\nEquity value: ${equity_value:,.1f}\nValue per share: ${per_share:,.2f}")
