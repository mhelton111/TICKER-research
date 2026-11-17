# Project 2 visible decision output

**As of:** 2026-11-16 market close for the LLY reference signal; portfolio estimates use the saved monthly adjusted-close file through 2026-10-19.

| Portfolio | Weights | Estimated annual return | Estimated volatility | Reserve | Mandate verdict |
|---|---|---:|---:|---:|---|
| Equal weight | BIL 20%, IEF 20%, LQD 20%, VTI 20%, XLV 20% | 4.52% | 8.18% | 40% | FAIL — misses return objective |
| 60/40 VTI/LQD benchmark | BIL 0%, IEF 0%, LQD 40%, VTI 60%, XLV 0% | 7.15% | 12.66% | 0% | FAIL — misses reserve minimum |
| Constrained portfolio | BIL 65%, IEF 0%, LQD 0%, VTI 30%, XLV 5% | 6.56% | 5.27% | 65% | PASS |

## LLY point-in-time reference signal

LLY closed at **$1,431.67** on 2026-11-16. It is a dated comparison signal only—not an optimizer sleeve or a trade instruction.

## Stress run

**Input changed:** return objective 6.5% → 7.5% (annualized; all other saved estimates and 3% reserve minimum unchanged).

**Documented directional expectation (not authenticated as an AI-off prediction):** the portfolio will need more equity exposure or no feasible mix; estimated volatility should rise if a feasible mix remains.

| Stress case | Weights | Estimated annual return | Estimated volatility | Reserve | Mandate verdict |
|---|---|---:|---:|---:|---|
| 7.5% objective | BIL 50%, IEF 0%, LQD 0%, VTI 35%, XLV 15% | 7.52% | 7.07% | 50% | PASS |

**Decision:** PILOT the constrained process, not a live allocation. Use it only after the CIO defines the calendar-year-loss measurement and breach action, and stop the pilot if a data refresh produces no feasible mix, a mandate verdict fails, or a review rejects the point-in-time convention.

Educational analysis only; not investment advice. AI (Codex) assisted with code and documentation; the analysis and decision require the student's review and ownership.
