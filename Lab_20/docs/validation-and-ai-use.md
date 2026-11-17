# Validation and AI Use

This is educational analysis, not investment advice. Codex assisted with code and documentation; the analysis and decision are the student's and require the student's review.

## Reproducible checks completed locally

On 2026-11-17, `python run_analysis.py` regenerated `output/model-output.md`. `python -m unittest -v test_lab20.py` checks that both baselines disclose their rule-specific failures, the constrained portfolio passes the checkable return and reserve rules, weights sum to 100%, and the 7.5% stress is riskier than the base case.

## Stress record

| Item | Record |
|---|---|
| Changed input | Estimated annual return objective: 6.5% → 7.5%; all saved monthly estimates and the 3% reserve minimum unchanged. |
| Predicted direction | More equity exposure or no feasible mix; higher volatility if feasible. |
| Actual | Feasible: BIL 50%, VTI 35%, XLV 15%; 7.52% expected return; 7.07% volatility. The base case is BIL 65%, VTI 30%, XLV 5%; 6.56% expected return; 5.27% volatility. |
| Interpretation | The higher hurdle required more equity exposure and raised model-estimated volatility. This does not validate the estimate as a forecast. |
| Stop condition | Stop if no feasible mix exists, a mandate verdict fails, point-in-time data cannot be defended, or the CIO rejects the loss-limit implementation. |

## Locked Changed-Input Record

The student reports that they and their partner completed the required AI-off pre-run prediction and Git commit before execution. This file records the prediction and result. The actual commit identifier and repository URLs were not supplied to this workspace, so they are not invented below.

| Required evidence | Student must add |
|---|---|
| Prediction commit URL/hash | Completed per student report; identifier not supplied here |
| Baseline output GitHub link | Local artifact: `output/model-output.md`; repository URL not supplied |
| Changed-input output GitHub link | Local artifact: `output/model-output.md`; repository URL not supplied |
| Student's explanation of match/mismatch | The direction matched: the higher return hurdle required more equity exposure and increased estimated volatility. |

## AI use disclosure

Codex was used to inspect course instructions, organize the readiness package, create the Python/Streamlit implementation, calculate and test the saved-data outputs, and draft documentation. The student must inspect the code, verify every statement and source, personally make the AI-off prediction, explain the decision-number code line by line, and own the final decision.
