# Project 2 Rubric Evidence Map

This map identifies the evidence a reviewer can inspect for each analytic-rubric category. It distinguishes completed evidence from governance conditions that intentionally remain unresolved; an unresolved condition is never relabeled as a pass.

## Problem definition and decision usefulness

**User and decision:** The intended user is the Meridian reserve-investment committee. The decision is whether to adopt, allocate to, rebalance, pilot, or reject a transparent ETF allocation process. The recommendation is **Pilot, not adopt**: 0% live capital until the committee operationalizes the outstanding mandate checks. The horizon is the next documented data refresh and committee review, not a price target.

**Decision rules:** The modeled portfolio must be long-only, use 5% increments, reach a 6.5% estimated annual return, and keep at least 3% in BIL/IEF reserve assets. The process compares equal weight, the 60/40 VTI/LQD reference, and the lowest-volatility feasible allocation. See `README.md`, `app.py`, `portfolio.py`, `output/model-output.md`, and `docs/decision-memo.md`.

**Boundary and evolution:** The repository baseline is commit `5047aa3`; the current package adds the four-part stress suite, explicit governance boundary, course-known-answer reconciliation, expanded failure tests, reproducibility record, and revised decision memo. This is a repository-evolution boundary, not a claim that Project 2 had a separate Brightspace Edition A requirement. `docs/project-evolution.md` records the changes and their decision effect.

## Data integrity and traceability

The primary optimizer input is the saved monthly adjusted-close file `data/prices_through_2026-10-19.csv`. Its transformation is adjacent monthly returns, arithmetic mean times 12, sample volatility times square root of 12, and a correlation-derived covariance calculation. The checksum, date boundary, input exclusions, source roles, and availability convention are in `docs/data-card.md` and `docs/reproducibility.md`. LLY's 2026-11-16 close is a separately dated context signal and is excluded from the optimizer.

The project does not silently insert live Yahoo data, Federal Reserve rates, LLY financial-statement screens, or the analyst-judgment WACC into the portfolio optimizer. Their limited roles are stated in `SOURCES.md`, `docs/data-card.md`, `docs/wacc-rebuild.md`, and `docs/labs-13-19-integration.md`.

## Financial soundness and judgment

The engine uses full covariance cross terms: weight(i) times weight(j) times correlation(i,j) times volatility(i) times volatility(j). It reports expected annual return, annualized volatility, and BIL/IEF reserve weight for every portfolio. The Lab 14 course-known-answer reconciliation verifies a 60/40 IG-bond/equity benchmark at 6.80% return, 10.46% volatility, and 0% reserve in `test_project2.py`.

The recommendation is conditional rather than a trade instruction. The 60/40 reference earns 7.15% but fails the reserve requirement; equal weight holds 40% reserve but misses the return objective; the selected mix passes the modeled checks. The decision memo specifies a 0% live-capital allocation range, monitoring items, and reversal triggers.

## Technical execution and usability

`README.md` provides the install, analysis, app, and test commands. `requirements.txt` names runtime dependencies. `run_analysis.py` creates a reviewable `output/model-output.md` without opening the UI. `app.py` exposes mandate controls, baseline comparisons, stress results, point-in-time disclosure, LLY sensitivity context, and explicit error handling for unavailable ticker data.

## Validation sensitivity and reproducibility

`test_project2.py` covers baseline failures, constrained feasibility, the documented higher-objective direction, estimate and cost effects, a 36-month window, a no-feasible-mix condition, invalid correlations, the Lab 14 known answer, and the preserved LLY base-case reconciliation. The changed-input record keeps the student prediction, old/new values, and actual decision effect. The cold-run result and reproducibility instructions are retained in `docs/partner-discussion.md` and `docs/reproducibility.md`.

## Professional communication

The README, decision memo, data card, validation record, rubric map, manifest, source list, public dashboard, and video scripts use the same Pilot conclusion and point-in-time boundary. The three transcript files contain explicit on-screen cues, the AI-use statement, educational-not-investment-advice statement, and the LLY context-only explanation. The student must add the final YouTube URLs, durations, timestamps, and access confirmation after recording.
