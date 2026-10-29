# Lab 17 — Point-in-Time Audit

> **Disclaimer:** This is an educational analysis using public FRED/ALFRED data. It is not investment research, investment advice, or a recommendation to buy, sell, or hold any security. Historical data and revisions do not predict future performance.

## Decision question

**Was each number in the selected series knowable on the day it would have informed a decision, and may Project 2 use it?**

## Deliverable and reproducibility

`asof_app.py` is a Streamlit rate viewer and point-in-time audit. It makes exactly one cached public CSV request per selected series to FRED for today's values and one cached request to ALFRED for a selected vintage date. It uses no API key. A period (`.`) is treated as missing, not as zero. Each chart presents current FRED history in blue against the selected ALFRED vintage in gold, with an information-cutoff line and interactive tooltips; the underlying audit still uses the original source data.

Run from this folder:

```powershell
streamlit run asof_app.py
python -m unittest -v test_lab17.py
```

The app starts with BAA, FEDFUNDS, DGS10, and MORTGAGE30US; allows a typed series ID such as PAYEMS; charts each current series from 1 January 2020; and shows its last observation available by the chosen date. It continues after an individual bad-series error rather than failing the whole page.

The audit table distinguishes two risks:

- **Release lag:** count of current observations dated after the last observation in the selected historical vintage.
- **Revision risk:** count of shared observation dates whose selected ALFRED-vintage value differs from today's FRED value.

## Required known-answer check

With **As known on = 5 October 2026**, the app's “Value known then” fields should be:

| Series | Last date known | Value |
|---|---|---:|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

These are not typed into the application. They are the course's required validation targets for the public FRED/ALFRED downloads. The computation layer has focused offline tests for missing values, release-lag and revision counts, and invalid ID rejection.

### PAYEMS revision probe

Add `PAYEMS` and set **As known on = 15 January 2025**. The required point-in-time check is December 2024 at **159,536 thousand persons**. Compare that vintage against the current FRED series: the current December 2024 value is lower and the app should report revisions above zero. This probe verifies that the app reads ALFRED for the historical vintage rather than downloading today's FRED data twice.

### Completed verification record — 29 October 2026

The app entry point was launched locally with `streamlit run asof_app.py` and its local page returned HTTP 200. The public ALFRED and FRED CSV downloads used for the required point-in-time checks are retained unchanged in `raw_data/`; `verify_lab17.py` re-runs these checks from those raw files.

| Check | Verified result |
|---|---|
| BAA, ALFRED vintage 2026-10-05 | Latest available observation: 2026-09-01, **6.47**. |
| FEDFUNDS, ALFRED vintage 2026-10-05 | Latest available observation: 2026-09-01, **3.75**. |
| DGS10, ALFRED vintage 2026-10-05 | Latest available observation: 2026-10-02, **5.28**. |
| MORTGAGE30US, ALFRED vintage 2026-10-05 | Latest available observation: 2026-10-01, **7.28**. |
| PAYEMS, ALFRED vintage 2025-01-15 | December 2024: **159,536** thousand persons. |
| PAYEMS, current FRED download | December 2024: **158,316** thousand persons—lower than the historical vintage. |
| PAYEMS same-date revisions | **381** overlapping observations differ between the selected historical vintage and the current download. |

The four rate values reproduce the course known answer exactly. The PAYEMS result demonstrates the point-in-time issue directly: a present-day series cannot be substituted for the January 2025 information set.

## My data card — DGS10 (10-Year Treasury Constant Maturity Rate)

| Field | Evidence |
|---|---|
| Source and link | FRED, Federal Reserve Bank of St. Louis: [DGS10](https://fred.stlouisfed.org/series/DGS10); the point-in-time comparison uses the corresponding [ALFRED vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05). |
| What it measures | The market yield on U.S. Treasury securities at a constant 10-year maturity. |
| Units / frequency | Percent; not seasonally adjusted; daily business-day observations. |
| Publication lag | Near-daily market rate; the selected 5 October vintage demonstrates that 2 October was the last available observation on 5 October (weekend/non-business-day timing). |
| Revisions | A market-rate series generally has much less revision risk than survey or benchmark-revised macro series, but the app audits the actual selected vintage instead of assuming zero revisions. |
| Download date | 29 October 2026; data are fetched live by the app from the cited FRED and ALFRED endpoints. |

### Three manual-value checks

The in-app 5 October 2026 ALFRED check should show DGS10 at **5.28** on **2 October 2026**. The other rate-series cross-checks are BAA **6.47** (September 2026) and FEDFUNDS **3.75** (September 2026). These values are also the course's known answer and verify that the viewer applies the selected vintage rather than present-day values.

## Partner discussion and fresh-eyes attack

**Discussion:** DGS10 was selected because the 10-year Treasury yield is a benchmark long-term rate that can affect discount rates, borrowing conditions, and equity valuation. We distinguished the observation date from the date that a decision-maker could access the observation. For a daily market rate, the release lag is typically minimal, but non-trading days still matter; the app shows the last actual observation available by a selected historical date.

**Attack — field trusted least: publication timing.** The publication-timing field deserves the most scrutiny because a historical backtest can accidentally use a day’s value before it was observable or tradable. Evidence: with the 5 October 2026 vintage, the app identifies 2 October—not 5 October—as DGS10's last available observation; the series should therefore be aligned with an explicit end-of-day/next-trading-session trading convention.

## Project 2 call

**Admit with an as-of rule.** DGS10 may be used as a macro/discount-rate context series only if every decision date uses the ALFRED vintage available on that date and any trade is assumed no earlier than the next tradable session after the observation becomes available. I would quarantine it if the analysis cannot document a consistent observation-time and execution-time convention. A backtest using today's DGS10 history is less vulnerable to revisions than PAYEMS, but it could still overstate timeliness by ignoring the daily observation and market-close timing.

## Reflection

“Cleaning” a series does not make it point-in-time valid. A data card records source, definition, units, frequency, publication lag, revision behavior, vintage/retrieval date, and transformations; these fields let a reader reproduce what was available then. For PAYEMS, a backtest on current revised data could overstate what was knowable because employment data are released with a lag and revised later. For DGS10, the dominant risk is timing rather than broad benchmark revisions.

## Submission contents

- `asof_app.py` — Streamlit FRED/ALFRED point-in-time app.
- `asof_core.py` — independently testable CSV parsing and point-in-time audit calculations.
- `test_lab17.py` — focused calculation-layer tests.
- `verify_lab17.py` — replayable known-answer and PAYEMS verification from the preserved raw downloads.
- `raw_data/` — exact public FRED/ALFRED CSV files used for the recorded verification.
- `Lab_17_Submission.md` — analysis, validation targets, data card, partner discussion, and Project 2 call.
- `lab-17-point-in-time.md` — archived course instructions.
- `SOURCES.md` — source and provenance ledger.
