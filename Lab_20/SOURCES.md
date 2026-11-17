# Sources and Data Boundaries

| Item | Source | What was used | Accessed / as-of |
|---|---|---|---|
| Lab 20 requirements | https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-13/lab-20-project2-readiness.md | Cold-run, changed-input, decision-line, and checkout requirements. | 2026-11-17 |
| Project 2 requirements | https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md | App, mandate, two baselines, point-in-time signal, stress, memo, validation, and AI disclosure requirements. | 2026-11-17 |
| Saved ETF prices | `data/prices_through_2026-10-19.csv` | Monthly adjusted closes for BIL, IEF, LQD, VTI, XLV; copied unchanged from the prior Lab 15 evidence set. The optimizer uses this file only. | Through 2026-10-19 |
| LLY market-close reference | https://stockanalysis.com/stocks/lly/history/ | 2026-11-16 close: $1,431.67. Cross-checked against the historical-data page at https://bullzeno.com/stock/LLY/historical. | 2026-11-16 close; retrieved 2026-11-17 |

## Data card — LLY

- **Series:** Eli Lilly and Company (`LLY`) daily closing price, USD per share.
- **Role:** dated public-company comparison signal only; excluded from the fund optimizer.
- **Observation date:** 2026-11-16 market close.
- **Value:** $1,431.67.
- **Timing convention:** the value is available only after the 2026-11-16 U.S. market close; it must not be used for a decision assumed to trade before that close.
- **Revision note:** the stored reference is a close-price record rather than a forecast; source corrections or vendor discrepancies must be documented if they arise.

The data boundary matters: LLY's 2026-11-16 close does not update the monthly ETF return estimates, which end 2026-10-19. The app and memo disclose this rather than implying a single synchronized dataset.
