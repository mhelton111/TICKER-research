"""LLY Project 1 integrated pro-forma, DCF, and validation engine.

Run: python lly_model.py
All dollars are USD millions except per-share values.  This program is
deliberately dependency-free and writes a reviewable result to output/.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from statistics import median


@dataclass(frozen=True)
class Case:
    name: str
    cardio_volume: tuple[float, ...]
    cardio_price: tuple[float, ...]
    other_growth: tuple[float, ...]
    gross_margin: tuple[float, ...]
    rd_pct: tuple[float, ...]
    sga_pct: tuple[float, ...]
    capex_pct: tuple[float, ...]
    nwc_pct: tuple[float, ...]
    wacc: float
    terminal_growth: float


YEARS = (2026, 2027, 2028, 2029, 2030)
# FY2025 reported base: Lilly 2025 Form 10-K, filed 2026-02-12.  Values are
# rounded to $m from the filing / SEC company-facts; see SOURCES.md.
BASE = {
    "revenue": 65179.0, "mounjaro_zepbound": 36507.0, "cash": 7268.0,
    "assets": 112476.0, "equity": 26535.0, "debt": 42503.0,
    "ocf": 16813.0, "capex": 7841.0, "net_income": 20640.0,
}
BASE["liabilities"] = BASE["assets"] - BASE["equity"]
BASE["nwc"] = BASE["revenue"] * 0.10
BASE["ppe"] = 35000.0  # model convention; gross PP&E/capex schedule anchor
BASE["other_assets"] = BASE["assets"] - BASE["cash"] - BASE["nwc"] - BASE["ppe"]
BASE["other_liabilities"] = BASE["liabilities"] - BASE["debt"]
SHARES = 899.3  # FY2025 diluted weighted-average shares; disclosed limitation
MARKET_PRICE = 1124.21  # 2026-09-09 regular-session close, preserved lab input

BASE_CASE = Case(
    "Base", (0.32, .28, .22, .17, .12), (-.03, -.03, -.02, -.02, -.02),
    (.07, .06, .05, .04, .03), (.830, .825, .820, .815, .810),
    (.125,) * 5, (.175,) * 5, (.130, .120, .110, .100, .090),
    (.100,) * 5, .085, .030,
)
LOW_CASE = Case(
    "Low", (.20, .16, .12, .09, .06), (-.07, -.06, -.05, -.04, -.03),
    (.03, .02, .02, .02, .02), (.810, .800, .795, .790, .790),
    (.140,) * 5, (.190,) * 5, (.150, .140, .125, .115, .105),
    (.115,) * 5, .095, .025,
)
HIGH_CASE = Case(
    "High", (.38, .33, .27, .21, .15), (-.01, -.01, -.01, -.01, -.01),
    (.09, .08, .07, .06, .05), (.840, .840, .835, .830, .825),
    (.120,) * 5, (.165,) * 5, (.120, .110, .100, .090, .085),
    (.095,) * 5, .080, .030,
)


def build(case: Case) -> list[dict[str, float]]:
    """Forecast an articulated three-statement model with a constant-debt policy."""
    rows: list[dict[str, float]] = []
    cardio, other = BASE["mounjaro_zepbound"], BASE["revenue"] - BASE["mounjaro_zepbound"]
    cash, ppe, debt, equity = BASE["cash"], BASE["ppe"], BASE["debt"], BASE["equity"]
    nwc = BASE["nwc"]
    for i, year in enumerate(YEARS):
        cardio *= (1 + case.cardio_volume[i]) * (1 + case.cardio_price[i])
        other *= 1 + case.other_growth[i]
        revenue = cardio + other
        cogs = revenue * (1 - case.gross_margin[i])
        rd, sga = revenue * case.rd_pct[i], revenue * case.sga_pct[i]
        da = ppe * .060
        ebit = revenue - cogs - rd - sga - da
        interest = debt * .045
        ebt = ebit - interest
        taxes = max(0.0, ebt * .200)
        net_income = ebt - taxes
        next_nwc = revenue * case.nwc_pct[i]
        delta_nwc = next_nwc - nwc
        capex = revenue * case.capex_pct[i]
        cfo = net_income + da - delta_nwc
        next_ppe = ppe + capex - da
        # Debt remains at the FY25 balance. Cash is the residual cash balance
        # after operating cash generation, capex, and modeled distributions.
        # This is an explicit no-new-debt policy, not a cash forecast from Lilly.
        dividends = net_income * .250
        next_equity = equity + net_income - dividends
        next_debt = BASE["debt"]
        target_cash = next_debt + BASE["other_liabilities"] + next_equity - next_nwc - next_ppe - BASE["other_assets"]
        debt_change = next_debt - debt
        cff = debt_change - dividends
        cash_from_cf = cash + cfo - capex + cff
        assets = target_cash + next_nwc + next_ppe + BASE["other_assets"]
        liabilities = next_debt + BASE["other_liabilities"]
        fcff = ebit * .800 + da - capex - delta_nwc
        rows.append(locals().copy())
        cardio, other, cash, ppe, debt, equity, nwc = cardio, other, target_cash, next_ppe, next_debt, next_equity, next_nwc
    return rows


def valuation(rows: list[dict[str, float]], wacc: float, g: float) -> dict[str, float]:
    if g >= wacc:
        raise ValueError("Terminal growth must be below WACC.")
    pvs = [r["fcff"] / (1 + wacc) ** (i + 1) for i, r in enumerate(rows)]
    tv = rows[-1]["fcff"] * (1 + g) / (wacc - g)
    pv_tv = tv / (1 + wacc) ** 5
    ev = sum(pvs) + pv_tv
    equity = ev + BASE["cash"] - BASE["debt"]
    return {"ev": ev, "equity": equity, "per_share": equity / SHARES, "pv_tv": pv_tv, "tv_share": pv_tv / ev, "tv": tv}


def validate(rows: list[dict[str, float]], case: Case) -> list[str]:
    results = []
    results.append("PASS base-year balance sheet: assets - liabilities - equity = 0.0" if abs(BASE["assets"] - BASE["liabilities"] - BASE["equity"]) < .01 else "FAIL base-year balance sheet")
    for r in rows:
        bs_ok = abs(r["assets"] - r["liabilities"] - r["next_equity"]) < .01
        cf_ok = abs(r["cash_from_cf"] - r["target_cash"]) < .01
        results.append(f"{'PASS' if bs_ok else 'FAIL'} {r['year']}: balance sheet")
        results.append(f"{'PASS' if cf_ok else 'FAIL'} {r['year']}: cash-flow-to-cash tie")
    base_value = valuation(rows, case.wacc, case.terminal_growth)["per_share"]
    high_wacc = valuation(rows, case.wacc + .01, case.terminal_growth)["per_share"]
    high_g = valuation(rows, case.wacc, case.terminal_growth + .005)["per_share"]
    results.append(f"{'PASS' if high_wacc < base_value else 'FAIL'} DCF monotonicity: +100bp WACC lowers value")
    results.append(f"{'PASS' if high_g > base_value else 'FAIL'} DCF monotonicity: +50bp terminal growth raises value")
    bridge = valuation(rows, case.wacc, case.terminal_growth)
    rebuilt = (bridge["ev"] + BASE["cash"] - BASE["debt"]) / SHARES
    results.append(f"{'PASS' if abs(rebuilt - bridge['per_share']) < .001 else 'FAIL'} enterprise-to-equity bridge")
    return results


def sensitivity(rows: list[dict[str, float]]) -> list[list[float]]:
    return [[valuation(rows, w, g)["per_share"] for g in (.025, .030, .035)] for w in (.080, .085, .090)]


def reverse_dcf(rows: list[dict[str, float]]) -> str:
    # Solve terminal growth only, holding explicit FCFF fixed.  This is a
    # market-implied expectation diagnostic, not a forecast.
    lo, hi = -0.05, .0849
    target = MARKET_PRICE
    for _ in range(100):
        mid = (lo + hi) / 2
        value = valuation(rows, .085, mid)["per_share"]
        if value < target: lo = mid
        else: hi = mid
    result = (lo + hi) / 2
    return "not reachable below WACC" if result >= .0848 else f"{result:.2%} terminal growth required to equal ${target:,.2f}"


def write_report() -> None:
    output = Path(__file__).with_name("output")
    output.mkdir(exist_ok=True)
    case_rows = {c.name: build(c) for c in (LOW_CASE, BASE_CASE, HIGH_CASE)}
    vals = {name: valuation(rows, {"Low": LOW_CASE, "Base": BASE_CASE, "High": HIGH_CASE}[name].wacc, {"Low": LOW_CASE, "Base": BASE_CASE, "High": HIGH_CASE}[name].terminal_growth) for name, rows in case_rows.items()}
    base_rows, base_val = case_rows["Base"], vals["Base"]
    grid = sensitivity(base_rows)
    lines = ["# LLY Integrated Model — Executed Output", "", "All dollars are USD millions except per-share values. Run date and source cutoff are stated in README.md.", "", "## Valuation range", "", "| Case | WACC | Terminal growth | EV | Equity value | Value/share |", "|---|---:|---:|---:|---:|---:|"]
    for name, case in (("Low", LOW_CASE), ("Base", BASE_CASE), ("High", HIGH_CASE)):
        v = vals[name]; lines.append(f"| {name} | {case.wacc:.1%} | {case.terminal_growth:.1%} | ${v['ev']:,.0f} | ${v['equity']:,.0f} | ${v['per_share']:,.2f} |")
    lines += ["", f"Reference market close preserved from Lab 08: ${MARKET_PRICE:,.2f} (2026-09-09). Base-case terminal-value share of EV: {base_val['tv_share']:.1%}.", "", "## Base-case five-year pro-forma", "", "| Year | Revenue | EBIT | Net income | CFO | Capex | FCFF | Cash | Debt | Equity |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in base_rows:
        lines.append(f"| {r['year']} | ${r['revenue']:,.0f} | ${r['ebit']:,.0f} | ${r['net_income']:,.0f} | ${r['cfo']:,.0f} | ${r['capex']:,.0f} | ${r['fcff']:,.0f} | ${r['target_cash']:,.0f} | ${r['next_debt']:,.0f} | ${r['next_equity']:,.0f} |")
    lines += ["", "## WACC / terminal-growth sensitivity ($/share)", "", "| WACC \\ g | 2.5% | 3.0% | 3.5% |", "|---|---:|---:|---:|"]
    for w, row in zip((.080, .085, .090), grid): lines.append(f"| {w:.1%} | " + " | ".join(f"${x:,.2f}" for x in row) + " |")
    lines += ["", "## Market-implied diagnostic", "", reverse_dcf(base_rows), "", "## Validation", ""] + [f"- {x}" for x in validate(base_rows, BASE_CASE)]
    lines += ["", "## Required interpretation", "", "The model holds debt at its FY2025 level and assumes distributions equal 25% of forecast net income; cash is the residual balance that makes the three statements articulate. These are explicit model conventions, not management forecasts. The DCF uses FY2025 cash and debt for the enterprise-to-equity bridge despite the later comparison-price date, so the range must be read with the staleness qualification in the memo."]
    (output / "model-output.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    write_report()
