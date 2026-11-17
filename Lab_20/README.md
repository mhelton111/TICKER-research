# Lab 20 — Project 2 Readiness

This folder is a self-contained Project 2 readiness package for the Meridian fund-portfolio process. It is educational analysis, not investment advice. Codex assisted with code and documentation; the analysis and decision are the student's and require the student's review.

## Run one command

From this folder, run:

```powershell
python run_analysis.py
```

That creates `output/model-output.md`, the GitHub-readable decision output. For the interactive web app, run `streamlit run app.py`. For validation, run `python -m unittest -v test_lab20.py`.

## Decision

**Pilot, not adopt.** The constrained 5%-grid portfolio meets the 6.5% estimated-return objective and 3% BIL/IEF reserve minimum using the saved monthly adjusted-close data. Do not move to adoption until the CIO defines the calendar-year-loss measurement and breach action, and the process remains feasible under the recorded stress and point-in-time review.

For the Lab 20 checkout landing page, use `Lab_20_Submission.md`.

## What the tool does

- Displays two transparent baselines—equal weight and a 60% VTI / 40% LQD reference—and their rule-specific mandate verdicts.
- Searches long-only, 5%-increment portfolios for the lowest estimated volatility that clears the checkable return and reserve rules.
- Keeps LLY as a dated comparison signal, not a portfolio sleeve. Its 2026-11-16 market close was $1,431.67.
- Preserves a 7.5% objective stress run, the stop condition, source ledger, and validation record.

## Important Lab 20 authenticity items

The student reports completing the AI-off pre-run prediction/Git commit and peer README-only cold run with Carter. `docs/validation-and-ai-use.md` and `docs/cold-run-log.md` record those results, including the 10-minute-30-second clean run. The repository URL and commit identifier were not supplied in this workspace, so those fields are accurately labeled rather than fabricated. Videos and transcripts remain Project 2 artifacts.

## Project 2 status

No Project 2 videos or transcripts have been created or linked yet. The app, decision output, memo, validation record, data card, stress record, and partner cold-run evidence are in place. Project 2 will be complete when the three required recordings and transcripts are created and linked, and the repository/commit URLs are added to the checkout manifest.

## Files

- `app.py` — Streamlit web app.
- `portfolio.py` — calculation layer.
- `run_analysis.py` — reproducible visible-output generator.
- `output/model-output.md` — current readable decision results.
- `docs/decision-memo.md` — committee memo.
- `docs/validation-and-ai-use.md` — checks, stress result, and honest completion record.
- `docs/checkout-manifest.md` — GitHub checkout template.
- `data/prices_through_2026-10-19.csv` — saved monthly adjusted-close input used by the optimizer.
- `SOURCES.md` — provenance and date boundaries.
