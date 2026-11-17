# Decision Memo — Meridian Reserve Decision Desk

**Recommendation: Pilot, not adopt.** The constrained portfolio is a transparent starting process, not an authorization to trade.

The mandate inherited from Labs 13–15 targets CPI + 4% (6.5% estimated annual return), keeps at least 3% in cash or daily-liquid government securities, is long-only, and uses the 60/40 VTI/LQD reference portfolio. The app shows two baselines and their individual rule failures beside the selected allocation. Equal weight fails the return objective; the 60/40 reference clears return but has 0% BIL/IEF and therefore fails the reserve rule. With preserved monthly data through 2026-10-19, the constrained result is BIL 65%, VTI 30%, XLV 5%: 6.56% estimated return, 5.27% estimated volatility, and 65% reserve.

LLY is a context signal rather than an investable sleeve. Its 2026-11-16 closing price was $1,431.67. It is not used before that close, does not enter optimization, and does not convert a historical price into a forecast. The Lab 19 investor panel is also deliberately bounded: it reports stronger profitability/growth indicators but preserves LLY owner-earnings and liabilities gaps as `not known`; it is a follow-up screen, not a purchase recommendation.

The stress raises the return objective from 6.5% to 7.5%. The selected mix becomes BIL 50%, VTI 35%, XLV 15%, with 7.52% estimated return and 7.07% volatility. The expected direction—more equity exposure and higher risk—occurred. This demonstrates sensitivity, not predictive accuracy.

**Allocation range:** pilot at 0% live capital until governance is complete; if the committee authorizes a paper pilot, use the calculated 5%-grid mix as the reference and review rather than a standing trading instruction. **Monitor:** feasibility, data freshness, return estimates, equity/bond correlations, reserve eligibility, LLY's after-close data timestamp, and the unresolved calendar-year-loss definition. **Stop / reject:** if a refresh produces no feasible mix, a checkable rule fails, the point-in-time convention breaks, or the CIO does not define the loss measure, observation date, and breach action.

Educational analysis only; not investment advice. AI tools assisted implementation and documentation; the final judgment remains the student's.
