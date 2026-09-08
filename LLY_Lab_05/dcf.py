"""Lab 05 training FCFF DCF. All amounts are USD millions except per-share value."""

# Editable inputs
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def main() -> None:
    if len(GROWTH_RATES) != 5:
        raise ValueError("Enter exactly five yearly growth rates.")
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return
    if DILUTED_SHARES <= 0:
        raise ValueError("Diluted shares must be greater than zero.")

    fcff = []
    current_fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        current_fcff *= 1 + growth_rate
        fcff.append(current_fcff)

    pv_explicit_fcff = sum(
        cash_flow / (1 + WACC) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value_year_5 = fcff[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value_year_5 / (1 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    pv_terminal_share_of_ev = pv_terminal_value / enterprise_value

    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"PV of explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value, Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_share:.4f}")
    print(f"PV of TV / enterprise value: {pv_terminal_share_of_ev:.4f}")


if __name__ == "__main__":
    main()
