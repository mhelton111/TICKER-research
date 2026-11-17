# Data Card and Point-in-Time Convention

| Field | Record |
|---|---|
| Portfolio input | Monthly adjusted closes for BIL, IEF, LQD, VTI, and XLV, saved in `data/prices_through_2026-10-19.csv`. |
| Transformation | Adjacent monthly percentage returns; arithmetic mean × 12; sample standard deviation × √12; covariance from the same return series. |
| Date boundary | Portfolio estimates end 2026-10-19. They are not presented as updated through the later LLY close. |
| LLY signal | LLY daily close, $1,431.67 on 2026-11-16, USD/share. |
| LLY timing | Treat as observable only after the 2026-11-16 U.S. market close; no same-day pre-close decision use. |
| LLY role | Comparison/context only; excluded from optimizer and allocation weights. |
| Macro timing rule | Lab 17 admits DGS10 only with the ALFRED vintage available on the decision date and execution no earlier than the next tradable session. |
| Federal Reserve charts | `data/DGS10_2026-10-05.csv` and `data/FEDFUNDS_2026-10-05.csv`, copied unchanged from Lab 17's ALFRED-vintage evidence. |
| Ticker explorer | User-entered symbol; six-month daily close display fetched from Yahoo Finance only when the user requests it. It is informational and never optimizer input. |

This separates observation date, data availability, and calculation cutoff, applying the provenance lessons from Labs 16 and 17.
