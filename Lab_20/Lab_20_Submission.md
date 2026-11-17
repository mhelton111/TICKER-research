# Lab 20 — Project 2 Readiness Submission

## Decision line

**Pilot the constrained long-only fund-allocation process; reverse to adoption only after the CIO defines and tests the calendar-year-loss rule, the process remains feasible under documented stresses, and the point-in-time data convention is accepted.**

## Lab 20 floor evidence

| Requirement | Evidence file | Result |
|---|---|---|
| Partner cold run | `docs/cold-run-log.md` | Carter and the student exchanged repositories; clean run, no reported failure, 10 minutes 30 seconds to `output/model-output.md`. |
| Changed input / prediction | `docs/validation-and-ai-use.md` | Return objective stress: 6.5% to 7.5%; student reports the required AI-off pre-run prediction and Git commit. |
| Before/after result | `output/model-output.md` | Base: 65% BIL / 30% VTI / 5% XLV; stress: 50% BIL / 35% VTI / 15% XLV. |
| Clean-run repair record | `docs/cold-run-log.md` | No repair needed because no failure was reported. |
| README-only reproduction | `README.md`, `run_analysis.py` | `python run_analysis.py` recreates the visible output. |
| Decision memo | `docs/decision-memo.md` | Consistent with output values, data dates, recommendation, risks, and reversal condition. |

## Key result

The constrained base portfolio passes the checkable mandate rules with a 6.56% estimated annual return, 5.27% estimated annual volatility, and 65% reserve-eligible weight. The equal-weight baseline fails the return objective; the 60% VTI / 40% LQD reference fails the reserve rule. LLY's 2026-11-16 close of $1,431.67 is a separately dated comparison signal, not an optimizer sleeve.

## Project 2 status

No videos or transcripts have been created or linked yet. They are truthfully documented as unresolved Project 2 artifacts. The Lab 20 floor evidence above is complete; use `docs/checkout-manifest.md` when adding actual GitHub URLs and the future Project 2 video/transcript links.

## Files for GitHub checkout

- `Lab_20_Submission.md` — this landing page.
- `README.md`, `app.py`, `portfolio.py`, `run_analysis.py`, and `test_lab20.py` — runnable tool and validation.
- `output/model-output.md` — GitHub-readable result.
- `docs/decision-memo.md`, `docs/validation-and-ai-use.md`, and `docs/cold-run-log.md` — required evidence.
- `SOURCES.md` and `data/prices_through_2026-10-19.csv` — source ledger and saved input.
