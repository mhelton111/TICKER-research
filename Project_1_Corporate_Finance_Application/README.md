# Project 1 — Corporate Finance Application: Eli Lilly (LLY)

Decision for a buy-side committee with no current LLY position: **watch/defer rather than initiate** over the next 12 months, while monitoring a five-year operating forecast. This is a course analysis, not investment advice.

## Run

From this directory, run `python lly_model.py`. No packages, network connection, credentials, or private data are required. It overwrites `output/model-output.md` with the visible model result and validation evidence.

## Scope and conventions

- Valuation decision date: August 31, 2026; comparison-price date preserved from Lab 08: September 9, 2026 regular close.
- Base financial year: December 31, 2025; 2025 Form 10-K filed February 12, 2026.
- Currency and units: USD millions, except per-share values. Per-share bridge uses 899.3m FY2025 diluted weighted-average shares, explicitly a proxy rather than current diluted shares outstanding.
- Exclusions: no transaction value is used because no qualified control/synergy/time-consistent transaction evidence was identified. P/E is an equity-value multiple; it is not bridged with debt or cash.

## Package map

- `lly_model.py` — five-year personalized three-statement/FCFF DCF engine, cases, sensitivity, reverse diagnostic, and checks.
- `output/model-output.md` — generated, visible executed result.
- `MEMO.md` — committee memorandum and method disagreement.
- `SOURCES.md` — source map, dates, definitions, and limitations.
- `VALIDATION_AND_AI_USE.md` — required validation evidence and the still-human-only items.
- `Edition_A_UNCHANGED.md` — preserved original Edition A; do not edit.
- `prior_work/` — copied LLY DCF, sensitivity, comps, and prior Edition B artifacts used as provenance.
- `project_audit.py` and `submission-manifest.csv` — course mechanical audit and working manifest.

## Cold-run protocol

Give a partner only this README and the directory. Have them run the command above in a fresh Python environment without coaching. Record OS, Python version, elapsed time to visible output, raw command/output, and first failure (or `none`) in `cold-run-log.txt` and `VALIDATION_AND_AI_USE.md`. Do not claim a cold run until that occurs.

## Known model limitation

The base-year revenue/cash/debt facts are filing-sourced. Forecast debt is held at the FY2025 level and cash is the residual resulting from operations, capex, and a 25% net-income distribution assumption. That makes the statements articulate, but it is not a management capital-allocation forecast; it is a high-risk assumption that must be challenged before any initiation.
