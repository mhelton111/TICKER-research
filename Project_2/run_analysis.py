from pathlib import Path
from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict
ROOT=Path(__file__).resolve().parent
sleeves,corr=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv')
def row(name,r,objective=.065,reserve=.03): return f"| {name} | {', '.join(f'{k} {v:.0%}' for k,v in r['weights'].items())} | {r['return']:.2%} | {r['volatility']:.2%} | {r['reserve']:.0%} | {verdict(r,objective,reserve)} |"
base=evaluate(equal_weight(sleeves),sleeves,corr); ref=evaluate(benchmark(sleeves),sleeves,corr); choice=optimize(sleeves,corr); stress=optimize(sleeves,corr,.075)
haircut_s,haircut_c=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv',return_haircut=.01)
estimate_stress=optimize(haircut_s,haircut_c)
short_s,short_c=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv',lookback_months=36)
window_stress=optimize(short_s,short_c)
cost_stress=optimize(sleeves,corr,annual_cost=.0025)
tight_constraint_stress=optimize(sleeves,corr,.075,.10)
text="""# Meridian Reserve Decision Output

**Decision date / LLY reference:** 2026-11-16 market close. LLY closed at **$1,431.67**. The ETF optimizer uses the preserved monthly adjusted-close input through 2026-10-19.

| Portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
"""+"\n".join([row("Equal-weight baseline",base),row("60/40 VTI/LQD baseline",ref),row("Constrained portfolio",choice)])+"""

## Stress suite
Each row is a reproducible one-at-a-time sensitivity. These are estimated outcomes, not forecasts. The process stops if any stress produces no feasible mix or if the CIO does not operationalize the calendar-year-loss rule.

| Stress portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
"""+"\n".join([
row("Estimate stress: 1.00% annual return haircut",estimate_stress),
row("Window stress: trailing 36 monthly returns",window_stress),
row("Cost stress: 0.25% annual implementation drag",cost_stress),
row("Constraint stress: 7.5% objective / 10% reserve",tight_constraint_stress,.075,.10),
row("Prior objective-only stress: 7.5% objective",stress,.075,.03),
])+"""

## Mandate coverage
The model checks the objective, BIL/IEF reserve, long-only weights, and 5% allocation grid. It reports volatility but does not impose an invented volatility cap. The 90% five-day-liquidity test, 8% issuer limit look-through, and 10% calendar-year-loss rule require a CIO-approved measurement convention and saved holdings/liquidity evidence before they can be marked as passed. Therefore, the portfolio **passes modeled rules only**; it is not an all-mandate approval.

## Committee call
**Pilot, not adopt.** Reverse only when the CIO operationalizes the calendar-year-loss rule, approves liquidity and issuer-look-through tests, and the process remains feasible under documented estimate, window, cost, and constraint stresses. Educational analysis only; not investment advice.
"""
(ROOT/'output'/'model-output.md').write_text(text,encoding='utf-8')
print(ROOT/'output'/'model-output.md')
