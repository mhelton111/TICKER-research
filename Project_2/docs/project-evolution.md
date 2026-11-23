# Project 2 Evolution and Decision Boundary

## Purpose

This record gives a reviewer a concise before-and-after trail for the current Project 2 repository. It does not replace a course-required immutable Edition A submission or claim one where none exists. Its purpose is to make the material evolution of the decision package reviewable.

## Baseline to current package

| Evidence surface | Repository baseline | Current package | Decision effect |
|---|---|---|---|
| Decision output | One constrained ETF result, two baselines, and an objective stress | Four one-at-a-time stresses: estimate haircut, 36-month window, cost drag, and tighter constraints | Moves the conclusion from a single feasible answer to a process that must survive documented assumption changes. |
| Mandate verdict | Return and reserve pass/fail were visible | Modeled checks are separated from liquidity, issuer-look-through, and loss-rule governance checks | Prevents a false all-mandate PASS; supports Pilot rather than Adopt. |
| Data lineage | Saved ETF data and a separately dated LLY reference | Data-card definitions, checksum, transformation, exclusions, and point-in-time boundary are explicit | Makes the result reproducible and prevents mixing the later LLY close into ETF estimates. |
| Validation | Baseline and direction checks | Course-known-answer, invalid-correlation, no-feasible-mix, cost, window, and base-DCF reconciliations | Tests both normal answers and high-risk failure modes. |
| Communication | App and memo explained the allocation | Rubric map, reproducibility record, revised memo, public companion, and video screen cues | Reduces reviewer effort and makes the committee ask inspectable. |

## What did not change

The governing decision remains the Meridian reserve mandate: diversified ETF sleeves, no shorting or borrowing, 5% grid, 6.5% estimated-return objective, 3% BIL/IEF reserve, and a 60/40 VTI/LQD reference. LLY remains a point-in-time research-context signal, not an allocation sleeve. The recommendation remains **Pilot, not adopt**.

## Why the decision is not adoption

The current process can show feasibility under stated inputs, but it cannot honestly certify the 90% five-day-liquidity rule, 8% issuer look-through, or 10% calendar-year-loss limit without a committee-approved measurement convention, holdings evidence, observation date, and breach response. The absence of that governance definition is decision-relevant evidence, not a coding defect to hide.
