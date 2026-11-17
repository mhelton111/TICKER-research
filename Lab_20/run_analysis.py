"""Produce the readable GitHub output. Run: python run_analysis.py"""

from pathlib import Path
from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "prices_through_2026-10-19.csv"
OUTPUT = ROOT / "output" / "model-output.md"


def table_row(name, result):
    weights = ", ".join(f"{ticker} {weight:.0%}" for ticker, weight in result["weights"].items())
    return f"| {name} | {weights} | {result['return']:.2%} | {result['volatility']:.2%} | {result['reserve']:.0%} | {verdict(result)} |"


def main():
    sleeves, correlations = load_estimates(DATA)
    cases = [("Equal weight", evaluate(equal_weight(sleeves), sleeves, correlations)),
             ("60/40 VTI/LQD benchmark", evaluate(benchmark(sleeves), sleeves, correlations)),
             ("Constrained portfolio", optimize(sleeves, correlations))]
    stressed = optimize(sleeves, correlations, objective=.075)
    lines = ["# Project 2 visible decision output", "",
             "**As of:** 2026-11-16 market close for the LLY reference signal; portfolio estimates use the saved monthly adjusted-close file through 2026-10-19.", "",
             "| Portfolio | Weights | Estimated annual return | Estimated volatility | Reserve | Mandate verdict |",
             "|---|---|---:|---:|---:|---|"]
    lines.extend(table_row(name, result) for name, result in cases)
    lines += ["", "## LLY point-in-time reference signal", "", "LLY closed at **$1,431.67** on 2026-11-16. It is a dated comparison signal only—not an optimizer sleeve or a trade instruction.", "",
              "## Stress run", "", "**Input changed:** return objective 6.5% → 7.5% (annualized; all other saved estimates and 3% reserve minimum unchanged).", "",
              "**Documented directional expectation (not authenticated as an AI-off prediction):** the portfolio will need more equity exposure or no feasible mix; estimated volatility should rise if a feasible mix remains.", "",
              "| Stress case | Weights | Estimated annual return | Estimated volatility | Reserve | Mandate verdict |", "|---|---|---:|---:|---:|---|",
              (table_row("7.5% objective", stressed) if stressed else "| 7.5% objective | — | — | — | — | FAIL — no feasible mix |"), "",
              "**Decision:** PILOT the constrained process, not a live allocation. Use it only after the CIO defines the calendar-year-loss measurement and breach action, and stop the pilot if a data refresh produces no feasible mix, a mandate verdict fails, or a review rejects the point-in-time convention.", "",
              "Educational analysis only; not investment advice. AI (Codex) assisted with code and documentation; the analysis and decision require the student's review and ownership."]
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
