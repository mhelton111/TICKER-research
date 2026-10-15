# Lab 13 — Portfolio Mandate Defense

**Course case:** Meridian Foundation Reserve (fictional)  
**Workspace folder:** `Meridian_Lab_13`  
**Completed:** October 15, 2026

## Scope correction

Lab 13 requires the common Meridian case and supplied holdings/candidates A–C. It does not use a company target, SEC filings, 10-K/10-Q data, or market-close data. This folder follows the required common case so its output can be checked against the published known answers.

## Checker

Run from this folder:

```powershell
python mandate.py
python mandate.py --probe
```

`mandate.py` uses only the Python standard library. It computes every reported value from editable inputs at the top of the file. The default run tests candidates A–D. The `--probe` run replaces candidate A's Cash weight with -2% and its global-equity-fund weight with 64%, as required by the lab.

## Known-answer validation

The reserve minimum is **3.0%** (= 4 quarters × $0.75M ÷ $100M × 100). The default checker output matches the published A/B/C result:

| Rule | A | B | C |
|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

The full executed default and probe output is preserved in `run-output.txt`.

## Probe validation

With `python mandate.py --probe`, candidate A has a lowest weight of **-2.0%** and fails only long-only. Its reserve-eligible weight remains **10.0%**, so the reserve rule still passes. This confirms that the checker is calculating rules separately rather than typing a verdict.

## Candidate D — AI-proposed attack on the checker

Candidate D is 3% Cash and 97% Global equity index fund, with all other holdings at 0%. It passes every checkable rule: total weight 100.0%, lowest weight 0.0%, reserve 3.0%, five-day liquidity 100.0%, and largest single company 0.0%.

Candidate D is designed to surface **S9**, because the stated calendar-year-loss limit has no defined measure or breach rule and therefore cannot be mechanically tested. The completed judgment appears below.

## Mandate-statement classification

| Statement | Type | My reason |
|---|---|---|
| S1 — Seven-year horizon; annual rebalancing | Hard constraint | The stated annual rebalance frequency is an operational rule the portfolio process can follow; the seven-year horizon is a planning input for the asset mix. |
| S2 — CPI + 4% net of costs over rolling five-year periods | Objective | This states the desired return outcome, measurement period, and net-of-costs convention. |
| S3 — $0.75M quarterly payout; one year in cash/daily-liquid government securities | Hard constraint | The payout amount, timing, reserve amount, and eligible assets are specific and mechanically testable. |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | It provides a comparison standard, but it does not say the portfolio must track it or set an active-risk limit. |
| S5 — Long-only; no borrowing, short sales, or derivatives | Hard constraint | These are explicit prohibited actions. |
| S6 — No single issuer above 8% | Hard constraint | The maximum issuer exposure is a numerical limit; the stated exemptions can be coded. |
| S7 — Annual turnover at most 25% without committee approval | Hard constraint | This is a numerical trading limit with a stated approval exception. |
| S8 — At least 90% redeemable within five business days | Hard constraint | The liquidity threshold and redemption window are measurable. |
| S9 — No calendar-year loss greater than 10% | Unverifiable promise | It gives no return measure, observation point, valuation convention, or breach response, so it cannot be tested reliably. |
| S10 — No sector, ESG, tax, or home-bias preference; no stated pilot objective | Missing | The mandate still does not say what the pilot should optimize or how trade-offs should be chosen. |

## Candidate D judgment

I think the CIO's objection holds because candidate D puts 97% in global equities even though it passes every rule the checker can measure. S9 decides the issue: a portfolio with that much equity risk could conflict with the stated 10% calendar-year-loss limit, but the CIO must define the rule before I can test or optimize for it.

## My question for the CIO

**Question:** Is S9 a binding hard risk limit, and if so, what exact calendar-year return measure, observation date, and breach response should govern it?

**Answer that changes my portfolio:** If S9 is a binding 10% limit based on year-end portfolio NAV with a required de-risking response, I would need a materially more defensive allocation and a formal downside-risk constraint rather than optimize mainly for return. If it is only a risk-tolerance preference with no mandatory action, I could accept a larger equity allocation while using the 60/40 benchmark as the main reference point.

## Simulated skeptical-colleague discussion

The lab permits me to play both roles when a partner is unavailable.

| Q&A | Discussion |
|---|---|
| **Skeptical colleague:** Candidate D passes everything. Why reject it? | **Me:** Passing the checker only proves that it meets the rules that are presently measurable. D exposes the missing operational definition in S9 and may not fit the Foundation's intended loss tolerance. |
| **Skeptical colleague:** Isn't the 60/40 benchmark enough to rule out 97% global equities? | **Me:** Not by itself. S4 identifies a benchmark but does not specify a tracking-error, allocation-band, or active-risk constraint, so I treat it as a preference/reference rather than a prohibition. |
| **Skeptical colleague:** Why is S9 not simply a hard 10% limit in the code? | **Me:** The number alone is incomplete: I need to know the return convention, measurement date, treatment of distributions, and what happens after a breach. Coding an unstated convention would hide a CIO decision inside the model. |
| **Skeptical colleague:** What decision must happen before optimization? | **Me:** The CIO must operationalize S9 and state what the pilot is intended to optimize. That decision determines whether the portfolio needs a binding downside-risk constraint or can prioritize the stated long-run return objective. |

## Reflection and investment-policy statement

An investment policy statement translates a client's objectives, constraints, governance, and measurement standards into instructions that can guide portfolio construction and monitoring. A portfolio can pass every checkable rule but still be unsuitable because the code cannot resolve an undefined loss rule, an unstated optimization objective, or an implicit risk preference; candidate D demonstrates that gap.

The type I was least sure about was S4. I classified it as a preference because it is a benchmark, not an explicit allocation requirement or tracking-error limit; the CIO could change that classification by stating a permitted deviation from the benchmark.

| Statement(s) | IPS role |
|---|---|
| S1 | Time horizon and rebalancing governance |
| S2 | Return objective and performance measurement |
| S3 | Spending obligation and liquidity/reserve constraint |
| S4 | Benchmark and preferred reference allocation |
| S5–S8 | Investment, concentration, trading, and liquidity constraints |
| S9 | Intended risk limit that requires an operational definition before it becomes a testable constraint |
| S10 | Missing optimization and preference information that the CIO must supply |

## AI quiz log

- **Line/concept selected:** `issuer_exposures()` and the `EXEMPT_ISSUERS` check.
- **My answer before explanation:** I thought every holding was compared separately with the 8% issuer limit.
- **What I corrected or learned:** The checker first adds all non-exempt securities belonging to the same company. That is why candidate B's 5% Acme bonds plus 4% Acme stock equals a 9% single-company exposure and fails the rule.

## Source and AI-use note

The only source for the case inputs, known answer, and requirements is the Lab 13 instruction page listed in `SOURCES.md`. Code assistance was used to construct the permitted standard-library checker and candidate-D test. The written discussion reflects my own thoughts and wording, not using AI. 
