# Reproducibility and Clean Rerun Record

## Environment observed for the documented rerun

| Item | Version / value |
|---|---|
| Python | 3.13.15 |
| Streamlit | 1.66.0 |
| pandas | 3.0.6 |
| requests | 2.34.2 |
| Altair | 6.3.0 |
| ETF input SHA-256 | `5CD4BEA99B6340E9969060F2A3F9CB80ACF9C2C5AB114689B44201BFE795F712` |
| ETF input boundary | Monthly adjusted closes through 2026-10-19 |
| LLY context boundary | $1,431.67 close on 2026-11-16, usable after close only |

## Reproduction commands

```powershell
python -m pip install -r requirements.txt
python -m unittest -v test_project2.py
python run_analysis.py
streamlit run app.py
```

The test command verifies nine checks. `run_analysis.py` rewrites `output/model-output.md`; compare its date boundary, baseline verdicts, stress rows, and Pilot conclusion with the memo before submission.

## Inputs and exclusions

- Optimizer inputs: only the saved BIL, IEF, LQD, VTI, and XLV monthly adjusted-close series.
- Context-only inputs: LLY close, LLY DCF, Federal Reserve charts, typed ticker display, and Labs 18-19 screens.
- Cost stress: 0.25% annual implementation drag. It is a transparent proxy, not a claim about an observed future trading cost because no starting holdings, trade list, or execution venue is supplied.
- Window stress: last 36 monthly return observations from the same saved ETF file; it does not add newer data.

## Expected clean-run behavior

- All tests pass.
- The output marks equal weight as failing the return objective and the 60/40 benchmark as failing the reserve minimum.
- The base constrained mix is BIL 65%, VTI 30%, XLV 5% and passes the modeled return/reserve rules.
- A deliberately impossible 50% estimated-return / 90% reserve request returns no feasible mix; this is a tested stop condition.

## Safe failure behavior

The calculation code rejects missing sleeve fields, non-finite returns or volatilities, out-of-range or asymmetric correlations, non-long-only weights, weights that do not sum to 100%, and negative/non-finite costs. The Streamlit typed-ticker display catches unavailable remote data and labels it as display-only; it never changes portfolio weights.
