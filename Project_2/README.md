# Meridian Reserve Decision Desk - Project 2

**Recommendation: Pilot, not adopt.** This educational portfolio process searches long-only 5% ETF allocations to meet Meridian's 6.5% estimated-return objective and 3% BIL/IEF reserve rule. It is not investment advice. OpenAI Codex, a GPT-5-based coding assistant, assisted implementation and documentation; the analysis and decision are the student's and require student review and ownership.

## Start the app and reproduce the output

```powershell
python -m pip install -r requirements.txt
python run_analysis.py
streamlit run app.py
```

`run_analysis.py` writes `output/model-output.md`, a visible decision record. Run `python -m unittest -v test_project2.py` to validate the calculations. Python 3.11+ is recommended.

## Mandate and decision design

- **Universe:** BIL, IEF, LQD, VTI, and XLV; long-only 5% steps. LLY is a separately dated public-company comparison signal, not a portfolio sleeve.
- **Objective:** 6.5% estimated annual return (CPI + 4% course mandate).
- **Modeled constraints:** at least 3% BIL/IEF reserve; no shorting, borrowing, or derivatives.
- **Benchmark:** 60% VTI / 40% LQD; transparent equal-weight baseline also shown.
- **Modeled checks:** return objective, BIL/IEF reserve, long-only weights, and 5% grid.
- **Governance checks pending a CIO measurement method:** 90% five-day liquidity classification, 8% issuer look-through, and the 10% calendar-year-loss limit. The portfolio passes modeled rules only, which supports a pilot rather than adoption.
- **Student governance proposal for committee review:** define calendar-year total return as January 1 through December 31; following a 10% breach, pause new allocations and discretionary rebalancing, verify the calculation, notify the committee, and document a reduce-risk or exception decision. This remains a proposal until the CIO approves it.

## Current evidence and stress suite

- LLY close: **$1,431.67 on 2026-11-16**, usable only after that market close.
- Saved monthly ETF adjusted-close data: through 2026-10-19 in `data/`.
- Point-in-time convention and LLY context: `docs/data-card.md` and `docs/decision-memo.md`.
- Reproducible one-at-a-time stresses: 1.00% return haircut, trailing 36-month window, 0.25% annual implementation-cost drag, and 7.5% objective / 10% reserve. Results appear in `output/model-output.md`.

## Submission documents

- `docs/decision-memo.md`
- `docs/validation-and-ai-use.md`
- `docs/locked-changed-input-record.md`
- `docs/partner-discussion.md`
- `docs/labs-13-19-integration.md`
- `docs/rubric-evidence-map.md`
- `docs/project-evolution.md`
- `docs/reproducibility.md`
- `docs/manifest.md`
- `SOURCES.md`

The three video speaking scripts and editable transcript files are in `videos/`. Record and publish them as unlisted YouTube videos, then add the links, duration, and access confirmation to `docs/manifest.md`.

## Public dashboard

The public dashboard is available at https://meridian-reserve-decision-desk.caringdace16.chatgpt.site. It is a static companion that mirrors the decision and evidence boundary. The canonical Python app remains `app.py`.
