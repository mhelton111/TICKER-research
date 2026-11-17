from pathlib import Path
from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict
ROOT=Path(__file__).resolve().parent
sleeves,corr=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv')
def row(name,r): return f"| {name} | {', '.join(f'{k} {v:.0%}' for k,v in r['weights'].items())} | {r['return']:.2%} | {r['volatility']:.2%} | {r['reserve']:.0%} | {verdict(r)} |"
base=evaluate(equal_weight(sleeves),sleeves,corr); ref=evaluate(benchmark(sleeves),sleeves,corr); choice=optimize(sleeves,corr); stress=optimize(sleeves,corr,.075)
text="""# Meridian Reserve Decision Output

**Decision date / LLY reference:** 2026-11-16 market close. LLY closed at **$1,431.67**. The ETF optimizer uses the preserved monthly adjusted-close input through 2026-10-19.

| Portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
"""+"\n".join([row("Equal-weight baseline",base),row("60/40 VTI/LQD baseline",ref),row("Constrained portfolio",choice)])+"""

## Stress
The annual return objective changed from 6.5% to 7.5%, with the 3% reserve rule and saved estimates unchanged. The documented pre-run direction was more equity exposure or no feasible portfolio, with higher estimated volatility if feasible.

| Stress portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
"""+row("7.5% objective",stress)+"""

## Committee call
**Pilot, not adopt.** Reverse only when the CIO operationalizes the calendar-year-loss rule and the process remains feasible under documented data, timing, and estimate stresses. Educational analysis only; not investment advice.
"""
(ROOT/'output'/'model-output.md').write_text(text,encoding='utf-8')
print(ROOT/'output'/'model-output.md')
