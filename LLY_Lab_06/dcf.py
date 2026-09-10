"""Lab 06 FCFF DCF for Eli Lilly. Amounts are USD millions except per-share value."""

# Editable inputs
STARTING_FCFF = 9479.666
GROWTH_RATES = [0.25, 0.20, 0.15, 0.10, 0.05]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 7268.0
DEBT = 42503.0
DILUTED_SHARES = 899.3

# Lab 06 sensitivity and reverse-DCF inputs
WACC_VALUES = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 1124.21
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.10
REVERSE_TOLERANCE = 0.000001


def value_per_share(starting_fcff: float, growth_rates: list[float], wacc: float, terminal_growth: float) -> float:
    """Return equity value per diluted share for one set of operating assumptions."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")
    fcff = []
    current_fcff = starting_fcff
    for growth_rate in growth_rates:
        current_fcff *= 1 + growth_rate
        fcff.append(current_fcff)
    pv_explicit_fcff = sum(cash_flow / (1 + wacc) ** year for year, cash_flow in enumerate(fcff, start=1))
    terminal_value_year_5 = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value_year_5 / (1 + wacc) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return equity_value / DILUTED_SHARES


def print_sensitivity_grid() -> None:
    print("\nSensitivity grid: value per diluted share ($)")
    header = "WACC \\ terminal growth | " + " | ".join(f"{growth:.0%}" for growth in TERMINAL_GROWTH_VALUES)
    print(header)
    print("-" * len(header))
    for wacc in WACC_VALUES:
        cells = ["invalid" if terminal_growth >= wacc else f"{value_per_share(STARTING_FCFF, GROWTH_RATES, wacc, terminal_growth):.2f}" for terminal_growth in TERMINAL_GROWTH_VALUES]
        print(f"{wacc:.0%}".ljust(23) + " | " + " | ".join(cells))


def reverse_dcf_shift() -> float | None:
    """Use bisection to solve a uniform shift to every explicit growth rate."""
    if any(rate + REVERSE_SHIFT_LOWER <= -1 for rate in GROWTH_RATES):
        return None

    def difference(shift: float) -> float:
        shifted_growth = [rate + shift for rate in GROWTH_RATES]
        return value_per_share(STARTING_FCFF, shifted_growth, WACC, TERMINAL_GROWTH) - TARGET_SHARE_PRICE

    lower, upper = REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER
    lower_difference, upper_difference = difference(lower), difference(upper)
    if lower_difference == 0:
        return lower
    if upper_difference == 0:
        return upper
    if lower_difference * upper_difference > 0:
        return None
    while upper - lower > REVERSE_TOLERANCE:
        midpoint = (lower + upper) / 2
        midpoint_difference = difference(midpoint)
        if midpoint_difference == 0:
            return midpoint
        if lower_difference * midpoint_difference < 0:
            upper = midpoint
        else:
            lower, lower_difference = midpoint, midpoint_difference
    return (lower + upper) / 2


def print_reverse_dcf() -> None:
    print("\nReverse DCF: uniform shift to Years 1-5 growth rates")
    print(f"Target share price: ${TARGET_SHARE_PRICE:.2f}")
    print(f"Held fixed: starting FCFF {STARTING_FCFF:.3f}; WACC {WACC:.1%}; terminal growth {TERMINAL_GROWTH:.1%}; cash {NON_OPERATING_CASH:.1f}; debt {DEBT:.1f}; diluted shares {DILUTED_SHARES:.1f}.")
    shift = reverse_dcf_shift()
    if shift is None:
        print(f"No solution in the configured bracket [{REVERSE_SHIFT_LOWER:.1%}, {REVERSE_SHIFT_UPPER:.1%}].")
    else:
        shifted_growth = [rate + shift for rate in GROWTH_RATES]
        print(f"Solved uniform growth shift: {shift:+.4%}")
        print("Implied Years 1-5 growth rates: " + ", ".join(f"{rate:.2%}" for rate in shifted_growth))


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
    pv_explicit_fcff = sum(cash_flow / (1 + WACC) ** year for year, cash_flow in enumerate(fcff, start=1))
    terminal_value_year_5 = fcff[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value_year_5 / (1 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_share_result = equity_value / DILUTED_SHARES
    pv_terminal_share_of_ev = pv_terminal_value / enterprise_value
    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"PV of explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value, Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_share_result:.4f}")
    print(f"PV of TV / enterprise value: {pv_terminal_share_of_ev:.4f}")
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
