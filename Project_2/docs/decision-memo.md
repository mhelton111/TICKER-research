# Decision Memo - Meridian Reserve Decision Desk

**Recommendation: Pilot, not adopt.** The committee should authorize no live capital. If it authorizes a paper pilot, the calculated 5% grid mix is a documented reference for review, not a standing trading instruction. This is educational analysis, not investment advice. OpenAI Codex, a GPT-5-based coding assistant, assisted implementation and documentation; the analysis and decision remain the student's responsibility.

## Committee decision and mandate

The intended user is the Meridian reserve-investment committee. Its decision is whether the process is sufficiently specified to adopt, allocate to, rebalance, pilot, or reject. The current horizon is the next controlled data refresh and committee review. The inherited mandate seeks CPI plus 4% (a 6.5% estimated annual return), at least 3% in cash or daily-liquid government securities, long-only exposure, and the 60% VTI / 40% LQD reference portfolio. The modeled universe is BIL, IEF, LQD, VTI, and XLV in 5% increments; it prohibits shorting, borrowing, and derivatives.

The app keeps two baselines beside the selected mix. Equal weight holds 40% BIL/IEF reserve but earns only 4.52% estimated annual return, so it fails the return objective. The 60/40 VTI/LQD reference earns 7.15% but holds 0% BIL/IEF, so it fails the reserve requirement. The lowest-volatility mix that satisfies the modeled return and reserve rules is BIL 65%, IEF 0%, LQD 0%, VTI 30%, XLV 5%: 6.56% estimated return, 5.27% estimated volatility, and 65% reserve.

This is not an all-mandate PASS. The app can test the objective, reserve, long-only condition, and 5% grid. It displays volatility but does not invent a volatility cap. The 90% five-day-liquidity test, 8% issuer-limit look-through, and 10% calendar-year-loss rule require a CIO-approved measurement convention, holdings/liquidity evidence, observation date, and breach action. Treating an undefined rule as passed would make the decision less useful, not more complete.

## Student judgment behind the recommendation

My priority is to meet a credible return objective while preserving enough liquidity to protect future obligations. Missing a stated return objective can damage investor confidence and the committee's credibility, but avoiding every loss is neither realistic nor the goal: markets have down years and the process should be designed for them rather than promise that they will not happen. That is why the reserve sleeve matters. It supplies liquidity and a buffer for obligations while the VTI and XLV sleeves provide the return exposure needed to clear the modeled objective.

I view the base mix as appropriate for a pilot, not as a claim that 65% BIL is permanently optimal. Its roughly 6.5% modeled return is deliberately below a generic long-run equity-market expectation because this is a reserve mandate with a liquidity requirement, not an all-equity personal account. If the committee raises the required return, more VTI and XLV exposure can be reasonable, but it also accepts higher volatility. A younger individual investor might have time to recover from volatility; this committee must instead respect its stated cash-flow needs, retirement-adjacent clients, and crisis conditions. Those are situations in which the higher-risk tradeoff becomes unacceptable.

## Data boundary and LLY role

The optimizer uses saved monthly adjusted closes through 2026-10-19. It converts adjacent monthly prices to returns, annualizes arithmetic average return by 12, annualizes sample volatility by the square root of 12, and applies the full correlation-based covariance matrix. `docs/data-card.md` and `docs/reproducibility.md` record the input boundary, transformation, checksum, source role, and exclusions.

LLY is a dated research-context signal, not an investable sleeve. Its $1,431.67 close is observable only after the 2026-11-16 U.S. market close; it is not blended into the earlier ETF history, and it does not affect optimizer weights. Adding one stock would silently change the diversified ETF mandate and introduce concentration risk. The Labs 18-19 investor screens therefore remain bounded follow-up context, not a purchase recommendation.

## Stress suite and judgment

The process changes one input family at a time. A 1.00% annual return haircut selects BIL 50%, VTI 35%, XLV 15% (6.52% estimated return; 7.07% volatility). A trailing 36-month window selects BIL 85%, VTI 10%, XLV 5% (6.57%; 1.69%). A 0.25% annual implementation-cost drag selects BIL 60%, VTI 30%, XLV 10% (6.57%; 5.77%). Tighter constraints of a 7.5% objective and 10% reserve select BIL 50%, VTI 35%, XLV 15% (7.52%; 7.07%). These are sensitivity results, not forecasts.

The economic lesson is not that any single mix is permanent. Lower return estimates, explicit cost drag, and a higher return requirement shift the solution toward higher-return equity sleeves and raise estimated risk when a feasible mix exists. The shorter-window result demonstrates estimation-window dependence. A deliberately impossible 50% estimated-return / 90% reserve request returns no feasible portfolio; the process must stop rather than force an answer.

For the unresolved loss rule, my proposed committee convention is calendar-year total return measured from January 1 through December 31, with a fiscal-year convention used only if the entity's governing documents require it. A 10% breach should trigger containment: pause new allocations and discretionary rebalancing, verify the return calculation and data, notify the committee, and decide whether to reduce risk or continue under a documented exception. This is a proposed governance choice, not a result the current app has silently assumed.

## LLY valuation context and boundary

The LLY driver panel is deliberately bounded to sensitivity context. It exposes WACC, cardiometabolic volume, gross-margin, and capex controls with reset; it never changes the ETF allocation. The most distrusted input is WACC because the prior 8.5% rate is analyst judgment rather than a fully sourced, date-matched build. `docs/wacc-rebuild.md` lists the risk-free rate, beta source/lookback, equity-risk-premium method, pre-tax debt cost, marginal tax rate, and capital weights required before a new WACC may support adoption.

The preserved Project 1 DCF range was $271.87 low, $637.42 base, and $946.03 high per share against a separately dated $1,124.21 reference market close. Its reverse-DCF diagnostic required 5.52% terminal growth versus the 3.0% base assumption. That comparison is not mechanically merged with the newer $1,431.67 LLY context close: the older DCF cash/debt bridge and market reference use a different date boundary. Its decision lesson remains relevant: even the high case required more durable cash-flow support than the then-modeled path, and the high terminal-value share makes WACC/growth assumptions material. The portfolio process therefore treats the panel as research context, not as a trading signal.

## Allocation range monitoring and reversal triggers

**Allocation range:** 0% live capital until governance is complete. A paper pilot may use the 5% grid allocation as a documented comparison reference only. It is a validation process for decision rules and governance, not a promise that the model can time the best market entry. **Monitor:** data freshness; input checksum; return estimates; correlation changes; reserve eligibility; cost assumptions; point-in-time availability; LLY after-close timestamp; and the committee's liquidity, issuer, and loss-rule definitions. **Stop / reject:** stop if no feasible mix exists, a modeled rule fails, a data boundary cannot be defended, correlations fail validation, or credible public governance, legal, or insider-trading disclosures raise a concern requiring committee review. **Move from pilot to adopt only if:** the outstanding mandate rules become testable, the process remains feasible under the documented estimate/window/cost/constraint stresses, and the committee approves the evidence and breach governance.
