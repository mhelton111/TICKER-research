"""Reverse DCF for Lab 12.

Solves for perpetual terminal growth that reconciles the Lab 10 FCFE model
to TSLA's September 28, 2026 regular-session close, holding all explicit
FCFE, WACC, shares and valuation conventions fixed.
"""

SHARES_MILLIONS = 3_752.431984
MARKET_CLOSE = 357.45  # Sept. 28, 2026, 4:00 p.m. EDT
WACC = 0.10
PV_EXPLICIT_FCFE = -22_326.365369921594
FCFE_2030 = 5_302.420576701643


def implied_terminal_growth():
    market_equity_value = SHARES_MILLIONS * MARKET_CLOSE
    pv_terminal_value = market_equity_value - PV_EXPLICIT_FCFE
    terminal_value_2030 = pv_terminal_value * (1 + WACC) ** 5
    # TV = FCFE_2030 * (1 + g) / (WACC - g), solved for g.
    g = (terminal_value_2030 * WACC - FCFE_2030) / (terminal_value_2030 + FCFE_2030)
    return market_equity_value, pv_terminal_value, terminal_value_2030, g


if __name__ == "__main__":
    equity, pv_tv, tv_2030, growth = implied_terminal_growth()
    print(f"Market equity value: ${equity:,.1f} million")
    print(f"PV of terminal value required: ${pv_tv:,.1f} million")
    print(f"Terminal value required at 2030: ${tv_2030:,.1f} million")
    print(f"Implied perpetual terminal growth: {growth:.2%}")
    print("This is a mechanical reconciliation, not a forecast probability.")
