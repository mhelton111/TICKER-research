# Validation and AI Use

Run `python -m unittest -v test_project2.py` and `python run_analysis.py`. Tests verify both baselines expose their distinct mandate failures, the constrained portfolio passes the checkable return/reserve rules, and the 7.5% objective stress has higher estimated volatility than base.

## Locked changed-input record

| Field | Record |
|---|---|
| Input | Objective 6.5% → 7.5%; 3% reserve and saved estimates unchanged. |
| Pre-run prediction | More equity exposure or no feasible mix; higher estimated volatility if feasible. |
| Actual | BIL 65% / VTI 30% / XLV 5% becomes BIL 50% / VTI 35% / XLV 15%; volatility rises from 5.27% to 7.07%. |
| Decision effect | Remains Pilot, because the loss-limit governance condition is still unresolved. |
| Student commit evidence | Student reports this prediction and pre-run commit were completed; add the actual commit URL/hash before final submission. |

AI tools assisted source organization, Python/Streamlit/static-web implementation, testing, and drafting. The student must verify sources, own the prediction and decision, and explain the calculation code.
