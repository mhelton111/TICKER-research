# Meridian Portfolio Process — Decision Memo

**Decision:** Pilot, not adopt, the constrained long-only portfolio process.

This is educational analysis, not investment advice. Codex assisted with code and documentation; the analysis and decision are the student's and require the student's review.

## Mandate and process

The process uses five diversified ETFs: BIL (cash/reserve), IEF (Treasury), LQD (investment-grade bonds), VTI (U.S. equity), and XLV (health-care equity). It searches long-only weights in 5% increments for the lowest estimated volatility that reaches a 6.5% annual expected-return objective and holds at least 3% in BIL or IEF. The saved monthly adjusted-close input ends 2026-10-19; the LLY comparison signal is separately dated to the 2026-11-16 market close.

The CIO's calendar-year-loss limit is intentionally not treated as a passing constraint because its return definition, observation date, and breach action have not been supplied. Calling it a pass without those details would be misleading.

## Results and comparison

`output/model-output.md` is the controlling calculation output. On the saved data, equal weight fails the return objective; the transparent 60% VTI / 40% LQD reference fails the reserve rule; and the constrained portfolio passes both checkable rules at 65% BIL, 30% VTI, and 5% XLV, with 6.56% estimated annual return and 5.27% estimated annual volatility.

The 7.5% objective stress shifts the feasible allocation to 50% BIL, 35% VTI, and 15% XLV, with 7.52% estimated return and 7.07% volatility. This is directionally consistent with the prediction: a higher return hurdle required more equity exposure and raised estimated volatility.

## Point-in-time signal and monitoring

LLY closed at $1,431.67 on 2026-11-16. It is a dated comparison signal only; it does not enter the optimizer and is not a buy/sell signal. Its inclusion demonstrates that the project identifies the date and source of a public-company reference rather than silently using a current quote.

Monitor data freshness, the feasibility of the 5%-grid search, expected-return estimates, equity/bond correlations, reserve eligibility, and the future CIO definition of the calendar-year-loss limit. Stop the process if a refresh yields no feasible portfolio, any checkable mandate rule fails, the point-in-time convention cannot be defended, or the CIO rejects the loss-limit implementation.

## Reversal condition

Change from **pilot** to **adopt** only when the CIO documents the loss metric and breach response, the implementation is tested against it, a partner completes a clean README-only cold run, and the process still passes under documented return/correlation/window stresses. Reject the process if those conditions cannot be met.
