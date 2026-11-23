# Meridian Reserve Decision Output

**Decision date / LLY reference:** 2026-11-16 market close. LLY closed at **$1,431.67**. The ETF optimizer uses the preserved monthly adjusted-close input through 2026-10-19.

| Portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
| Equal-weight baseline | BIL 20%, IEF 20%, LQD 20%, VTI 20%, XLV 20% | 4.52% | 8.18% | 40% | FAIL — misses return objective |
| 60/40 VTI/LQD baseline | BIL 0%, IEF 0%, LQD 40%, VTI 60%, XLV 0% | 7.15% | 12.66% | 0% | FAIL — misses reserve minimum |
| Constrained portfolio | BIL 65%, IEF 0%, LQD 0%, VTI 30%, XLV 5% | 6.56% | 5.27% | 65% | PASS |

## Stress suite
Each row is a reproducible one-at-a-time sensitivity. These are estimated outcomes, not forecasts. The process stops if any stress produces no feasible mix or if the CIO does not operationalize the calendar-year-loss rule.

| Stress portfolio | Weights | Est. annual return | Est. volatility | Reserve | Verdict |
|---|---|---:|---:|---:|---|
| Estimate stress: 1.00% annual return haircut | BIL 50%, IEF 0%, LQD 0%, VTI 35%, XLV 15% | 6.52% | 7.07% | 50% | PASS |
| Window stress: trailing 36 monthly returns | BIL 85%, IEF 0%, LQD 0%, VTI 10%, XLV 5% | 6.57% | 1.69% | 85% | PASS |
| Cost stress: 0.25% annual implementation drag | BIL 60%, IEF 0%, LQD 0%, VTI 30%, XLV 10% | 6.57% | 5.77% | 60% | PASS |
| Constraint stress: 7.5% objective / 10% reserve | BIL 50%, IEF 0%, LQD 0%, VTI 35%, XLV 15% | 7.52% | 7.07% | 50% | PASS |
| Prior objective-only stress: 7.5% objective | BIL 50%, IEF 0%, LQD 0%, VTI 35%, XLV 15% | 7.52% | 7.07% | 50% | PASS |

## Mandate coverage
The model checks the objective, BIL/IEF reserve, long-only weights, and 5% allocation grid. It reports volatility but does not impose an invented volatility cap. The 90% five-day-liquidity test, 8% issuer limit look-through, and 10% calendar-year-loss rule require a CIO-approved measurement convention and saved holdings/liquidity evidence before they can be marked as passed. Therefore, the portfolio **passes modeled rules only**; it is not an all-mandate approval.

## Committee call
**Pilot, not adopt.** Reverse only when the CIO operationalizes the calendar-year-loss rule, approves liquidity and issuer-look-through tests, and the process remains feasible under documented estimate, window, cost, and constraint stresses. Educational analysis only; not investment advice.
