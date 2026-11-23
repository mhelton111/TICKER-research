# Labs 13 through 19 Integration Record

This project keeps the Meridian Foundation Reserve mandate as its governing framework. Earlier labs provide evidence and design rules; none silently replaces the mandate or turns an informational signal into an optimizer input.

| Lab | Incorporated evidence | Project control or output |
|---|---|---|
| 13 Mandate | 6.5% objective, 3% reserve, long-only, 60/40 benchmark, 90% five-day liquidity, 8% issuer rule, and undefined calendar-year-loss rule. | The app checks the return/reserve rules, labels the 60/40 baseline failure, and keeps the loss rule as CIO clarification rather than a fabricated pass. |
| 14 Baselines | Equal-weight and 60/40 reference portfolios; covariance uses correlation times both volatilities. | The app reports both baseline verdicts beside the constrained mix and charts return versus volatility. |
| 15 Stability | Five-year monthly adjusted-close estimation, 5% long-only search, and changed-objective stress. | `portfolio.py` performs the reusable search; 6.5% to 7.5% stress is preserved in output and validation. |
| 16 Provenance | Knowability requires a stated source, observation date, publication timing, and row/data boundary. | The data card distinguishes the 2026-10-19 ETF cutoff from the 2026-11-16 LLY close; no later price is inserted into historical estimates. |
| 17 Point in time | FRED/ALFRED current-versus-vintage distinction and next-tradable-session convention. | Saved DGS10 and FEDFUNDS 2026-10-05 ALFRED-vintage files power context charts; they are not optimizer inputs or current WACC components. |
| 18 Skill discipline | Deterministic transformations, explicit source selection, and `not known` rather than invented values. | Portfolio calculations are code-derived; the LLY WACC panel labels its unsourced prior rate as the most distrusted input. |
| 19 LLY panel | Buffett/Graham/Burry results are a bounded first-pass screen, with missing facts retained. | LLY is context only. The app and memo do not convert a screen result into a trade recommendation or allocation sleeve. |

## Validation retained

`test_project2.py` verifies baseline rule failures, constrained-portfolio feasibility, stress direction, and LLY DCF base reconciliation. The local Streamlit app is tested separately for HTTP 200. The public dashboard exposes the same portfolio mandate controls but preserves an explicit evidence boundary for its informational charts.

## Course-source links

- Lab 13: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md
- Lab 14: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md
- Lab 15: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-15-portfolio-stability.md
- Lab 16: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md
- Lab 17: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md
- Lab 18: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md
- Lab 19: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/slides-session-19.md
