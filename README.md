# Meridian Reserve Decision Desk — Project 2

**Recommendation: Pilot, not adopt.** This educational portfolio process searches long-only 5% ETF allocations to meet Meridian's 6.5% estimated-return objective and 3% BIL/IEF reserve rule. It is not investment advice. AI tools assisted implementation and documentation; the analysis and decision require student review and ownership.

## One-command visible result

```powershell
python run_analysis.py
```

This writes `output/model-output.md`. Run the app with `streamlit run app.py`; validate with `python -m unittest -v test_project2.py`.

## Mandate / decision design

- **Universe:** BIL, IEF, LQD, VTI, XLV; long-only 5% steps. LLY is a separately dated public-company comparison signal—not a portfolio sleeve.
- **Objective:** 6.5% estimated annual return (CPI + 4% course mandate).
- **Hard constraints:** at least 3% BIL/IEF reserve; no shorting, borrowing, or derivatives.
- **Benchmark:** 60% VTI / 40% LQD; transparent equal-weight baseline also shown.
- **Unresolved rule:** the CIO has not operationalized the 10% calendar-year-loss limit, so it is disclosed rather than silently coded.

## Current evidence

- LLY close: **$1,431.67 on 2026-11-16**. It is only usable after that market close.
- Saved monthly ETF adjusted-close data: through 2026-10-19 in `data/`.
- Point-in-time convention and LLY fundamentals screen: `docs/data-card.md` and `docs/decision-memo.md`.
- Baseline, constrained, and stress results: `output/model-output.md`.

## Project documents

- `docs/decision-memo.md`
- `docs/validation-and-ai-use.md`
- `docs/partner-discussion.md`
- `docs/labs-13-19-integration.md`
- `SOURCES.md`

Three recordings/transcripts must be added by the student for final Project 2 submission. The `docs/manifest.md` lists every required artifact and records that status truthfully.

## Public dashboard

The public dashboard is available at https://meridian-reserve-decision-desk.caringdace16.chatgpt.site. It is a static public companion that mirrors the decision, comparisons, and documented stress. The canonical Python app remains `app.py`.
