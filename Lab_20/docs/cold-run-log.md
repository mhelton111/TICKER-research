# Partner Cold-Run Log

This log records the peer cold run reported by the student on 2026-11-17: the student and Carter exchanged their repositories and each ran the other's package using the README. Carter reported a clean run to visible output in 10 minutes 30 seconds.

## Instructions for the partner

1. Use a new folder and the repository link only; do not ask for help while running it.
2. From `Lab_20`, run `python run_analysis.py`.
3. Record the exact command, the first failure (or `none`), elapsed time to `output/model-output.md`, and where you found the decision.
4. If a failure occurs, the author fixes it, pushes the fix, and you rerun it. Record both attempts.

| Field | Partner entry |
|---|---|
| Partner name | Carter |
| Date | 2026-11-17 (reported by student) |
| Scope | README-only exchange: each partner ran the other's Lab 20 package without coaching. |
| Exact command | `python run_analysis.py` from the `Lab_20` folder. |
| First failure | None reported. |
| Elapsed time to visible output | 10 minutes 30 seconds |
| Result location | `output/model-output.md` |
| Fix needed / GitHub commit URL | No repair was reported; add the actual GitHub commit URL if one exists. |
| Clean rerun result | Both partners reported that the command generated the visible decision output. |

## Partner Q&A

**Question:** How does the program turn the saved monthly adjusted-close prices into the portfolio decision instead of simply choosing the ETF with the highest historical return?

**Answer:** `load_estimates()` first converts each adjacent pair of monthly adjusted closes into a monthly return. It annualizes each asset's average monthly return and sample volatility, then calculates the correlation table from the same monthly-return series. `evaluate()` uses the portfolio weights, volatilities, and correlations to compute expected return, volatility, and BIL/IEF reserve weight. `optimize()` enumerates every long-only 5%-increment mix, rejects any that miss the 6.5% return or 3% reserve rule, and retains the feasible mix with the lowest estimated volatility. The decision is therefore based on the stated constraints and the whole covariance relationship, not on a single asset's return.

**Follow-up / answer from the code:** Why can the 60% VTI / 40% LQD baseline have a higher estimated return yet fail the mandate? `verdict()` checks both the return objective and the BIL/IEF reserve minimum. That baseline has 0% reserve assets, so it fails the reserve rule even though its estimated return exceeds 6.5%.

**Carter's improvement question:** What would improve the tool before it is used beyond this course exercise?

**Answer:** First, formalize the calendar-year-loss limit that is currently disclosed but not coded: the CIO must specify the return measure, observation date, limit, and breach response. Then add transaction costs and rebalancing rules so an allocation change is not treated as free. A next improvement is a versioned data-refresh process that stores the downloaded prices, source timestamp, and resulting output together. These changes would make the process more auditable without pretending that historical estimates are forecasts.

**Carter's bottleneck question:** What is the main computational or decision bottleneck?

**Answer:** With five assets and 5% increments, enumeration is small and transparent, so computation is not the practical bottleneck. The real bottleneck is estimate quality: monthly historical returns, volatilities, and correlations can change with the selected window and do not guarantee future outcomes. The 7.5% objective stress shows this directly—raising the hurdle changes the selected allocation and increases estimated volatility. As the asset universe or grid becomes much larger, exhaustive enumeration would also become slower; then the process would need a documented optimization method while preserving the same mandate checks and audit trail.
