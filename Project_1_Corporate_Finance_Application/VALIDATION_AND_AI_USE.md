# Validation and AI-use record

## Validation results produced by the model

Run `python lly_model.py`; the generated output records these executable checks:

| Requirement | Test | Expected result | Evidence |
|---|---|---|---|
| Synthetic / known-answer reconciliation | FY2025 balance sheet: $112,476m assets − $85,941m liabilities − $26,535m equity | Zero difference | `output/model-output.md` |
| Independent definition check | Debt/cash/share basis compared with the 2025 10-K balance sheet, Borrowings note, and EPS statement | Definitions and units disclosed; weighted-average-share limitation retained | `SOURCES.md` |
| Directional test written before execution | Higher WACC lowers per-share value; higher terminal growth raises it | Both pass | Model validation section |
| Three-statement articulation | Every forecast year: assets = liabilities + equity; cash from cash-flow statement = balance-sheet cash | Every test passes | Model validation section |
| Enterprise/equity bridge | (EV + cash − debt) / shares = reported per-share value | Pass | Model validation section |
| Peer policy / definition consistency | AMGN/GILD only; annual FY25 GAAP diluted EPS and date-matched prices; no debt/cash bridge to P/E | Qualified pass | `prior_work/Lab_08_comps.md` |
| Highest-risk failure test | Low case: slower volume, more price pressure, lower margins, higher capex/working capital, higher WACC | Low value is materially below base; action remains defer | `output/model-output.md`, `MEMO.md` |

## Assumption-challenge record

| Load-bearing driver | Base value | Basis | Challenge / challenger | Evidence that would change it |
|---|---|---|---|---|
| Mounjaro/Zepbound volume | 32%, 28%, 22%, 17%, 12% | Decelerating path from FY25 franchise scale, not a straight-line extrapolation | Product concentration makes the terminal FCFF highly sensitive | Quarterly product volume / prescription and supply evidence materially above or below path |
| Realized price | -3%, -3%, -2%, -2%, -2% | Explicit pricing/rebate pressure, rather than assuming volume equals sales growth | Reimbursement/rebate compression can exceed low case | Quarterly net-price commentary, payer decisions, gross-to-net evidence |
| Gross margin | 83.0% to 81.0% | FY25 reported 83.0% then conservative normalization | Mix/manufacturing could help or pricing and capacity costs could hurt | Reported gross margin and manufacturing-cost trends |
| Capex | 13% to 9% of revenue | High early manufacturing investment, then normalization | Capacity expansion may not scale down on schedule | Reported PP&E purchases and capacity announcements |
| WACC / terminal growth | 8.5% / 3.0% | Analyst judgment and sensitivity bounds | Equity risk, capital structure, and terminal durability could invalidate it | Current market inputs and a documented cost-of-capital rebuild |
| Capital-allocation convention | Debt held at FY2025 level; distributions at 25% of NI | Transparent convention needed to articulate statements | Not a forecast of management financing | Updated cash, debt, dividend, buyback, and financing disclosures |

## Locked Changed-Input Record

The prediction below was saved before the documented rerun. No Git client is installed in this workspace, so the timestamp and this frozen written record serve as the pre-run evidence.

| Precommit timestamp | Commit / frozen copy | Input and units | Old → new | Predicted direction | Predicted decision effect |
|---|---|---|---|---|---|
| 2026-10-19 13:55:22 EDT | `VALIDATION_AND_AI_USE.md` saved before rerun; no Git client available | Base WACC; percent | 8.5% → 9.5% | Base per-share value will fall materially because both explicit FCFF and terminal value are discounted more heavily. | No change: Watch/Defer should remain because even the original base value is below the preserved market reference. |

| Actual before/after | Actual decision effect | Prediction reconciliation | Failure diagnosis or no-change reason | Evidence path |
|---|---|---|---|---|
| Base DCF per-share value: $637.42 at 8.5%; $529.24 at 9.5%; change: -$108.18 (-17.0%). Terminal-value share fell from 80.5% to 77.4%. | No change: Watch/Defer. $529.24 remains below the preserved $1,124.21 market reference. | Correct. Value fell materially and the decision did not change. | No failure: the outcome follows the pre-stated DCF discount-rate direction. The case still requires monitoring because the market-price comparison uses later market data than FY2025 bridge inputs. | `output/changed-input-wacc-9_5.md`; restored base output in `output/model-output.md`; original 8.5% input restored in `lly_model.py`. |

## AI output check

| AI output considered | Independent check | Disposition |
|---|---|---|
| Proposed integrated-model architecture and constant-debt equation | Algebraic cash-flow-to-cash and balance-sheet checks in `lly_model.py`; 10-K source map checked against filing locations | Accepted with qualification: constant debt is disclosed as a model convention, not a company forecast. |
| Earlier simple growth-only DCF | Replaced by product-driver forecast and articulated statements | Rejected as final architecture; preserved in `prior_work/` for evolution evidence. |

## Partner cold run

**Operator:** Independent partner, not the project author. AI used during the run was the partner's, not the project author's. This first attempt exposed an environment/package-access failure before the model could execute.

| Run date/time | Operator / AI use | OS | Python version | Elapsed time to visible output | First error or `none` | Outcome |
|---|---|---|---|---|---|---|
| Date not supplied by partner | Independent partner; Codex used only to conduct/document attempt, with no model modification | Windows | `python --version` failed: Python not recognized/on PATH | ~8 seconds to first environment error | `python : The term 'python' is not recognized as the name of a cmdlet, function, script file, or operable program.` Prior file search also found no `lly_model.py` or `README.md` in the active folder. | **Failed before model execution.** `output/model-output.md` was not created. |

**Repair / clean rerun required:** Put `README.md` and `lly_model.py` together in one new folder on the partner's computer, install Python 3 and select **Add Python to PATH**, then have the partner run `python --version` and `python lly_model.py` without coaching. Record that second, clean result separately; it is required before claiming a successful cold run.

| Clean-rerun date/time | Operator / AI use | OS | Python version | Elapsed time to visible output | First error or `none` | Outcome |
|---|---|---|---|---|---|---|
| Date/time not supplied by partner | Independent partner; Codex used by the partner during the rerun | Windows (reported in first attempt) | Python 3 (major version reported) | 2 minutes 34 seconds | none | **Passed.** `output/model-output.md` was created. |

The three recordings, corrected transcripts, repository access check, and final receipt still require student action.
