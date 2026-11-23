# Locked Changed Input Record

## Prediction to lock before the official run

**Student AI-off prediction:** I personally believe that raising the required return will push the portfolio toward higher-return, higher-volatility tickers and reduce its reserve allocation if a feasible mix remains. The same tradeoff can appear when estimated returns are reduced or implementation costs are added. I made this prediction before the official validation run.

| Input family | Old value | New value | Pre-run prediction |
|---|---|---|---|
| Estimates | Saved annualized return estimates | Each asset return reduced by 1.00 percentage point | Lower expected returns should require heavier weights in higher-return, higher-volatility tickers, or make the mandate infeasible. |
| Window | Full preserved monthly series through 2026-10-19 | Trailing 36 monthly returns from the same file | The selected weights and volatility may change materially because the sample is shorter; I expect the result to remain sensitive to the return estimates. |
| Costs | 0.00% annual implementation drag | 0.25% annual implementation drag | Lower net return should require heavier weights in higher-return, higher-volatility tickers, or make the mandate infeasible. |
| Constraints | 6.5% objective and 3% reserve | 7.5% objective and 10% reserve | A higher required return should shift weight toward higher-return, higher-volatility tickers; the tighter reserve requirement may partially limit that shift. |

## Commit evidence

- Pre-run commit hash: `f2ff122bbb0961252e0c59adebc14d499bd8e5fb`
- Pre-run GitHub URL: https://github.com/mhelton111/TICKER-research/commit/f2ff122bbb0961252e0c59adebc14d499bd8e5fb
- Official run command: `python -m unittest -v test_project2.py; python run_analysis.py`
- Actual results: recorded in `docs/validation-and-ai-use.md` and `output/model-output.md` after the official run.
