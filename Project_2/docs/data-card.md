# Data Card and Point in Time Convention

| Field | Record |
|---|---|
| Decision user and horizon | Meridian reserve-investment committee; next documented data refresh and committee review. |
| Optimizer universe | BIL, IEF, LQD, VTI, XLV only; long-only 5% allocation grid. |
| Portfolio source file | `data/prices_through_2026-10-19.csv`; monthly adjusted closes saved from the Lab 14 course workflow. |
| File integrity | SHA-256 `5CD4BEA99B6340E9969060F2A3F9CB80ACF9C2C5AB114689B44201BFE795F712`. |
| Observation boundary | ETF estimates end 2026-10-19. No later market observation is inserted into that history. |
| Transformation | Adjacent monthly percentage returns; arithmetic mean times 12; sample standard deviation times square root of 12; covariance is correlation times both annualized volatilities. |
| Return convention | Arithmetic annualized mean return, an estimate used for the course mandate rather than a forecast or realized return claim. |
| Cost convention | Base portfolio has 0.00% cost drag; cost stress applies a transparent 0.25% annual implementation proxy. It is not an observed execution-cost claim. |
| LLY context signal | $1,431.67 daily close on 2026-11-16, USD/share, from the saved StockAnalysis source record. |
| LLY timing | Observable only after the 2026-11-16 U.S. market close; no same-day pre-close decision use. |
| LLY exclusion | LLY is research context only, not an optimizer input, allocation sleeve, return estimate, or proxy for the ETF universe. |
| Macro timing rule | DGS10 is admissible only from the ALFRED vintage available on the decision date, with execution no earlier than the next tradable session. |
| Federal Reserve context | `data/DGS10_2026-10-05.csv` and `data/FEDFUNDS_2026-10-05.csv`, copied unchanged from Lab 17 vintage evidence; neither enters the optimizer or current WACC. |
| Typed ticker explorer | A user-entered symbol is display-only. Yahoo chart data can be unavailable or delayed and never changes calculated portfolio weights. |
| Privacy and licensing | The project contains public-market/course data and no personal data. Saved files are used for educational reproducibility; no claim is made to redistribute a market-data vendor's service. |

This card separates source date, observation availability, calculation cutoff, transformation, and exclusion. See `SOURCES.md` for source locations and `docs/reproducibility.md` for the clean-rerun environment.
