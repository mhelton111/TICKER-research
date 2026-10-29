# Lab 17 — Point-in-Time Audit (course instructions archive)

Source: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md  
Accessed: 2026-10-29

## Required app behavior

Build `asof_app.py`, a Streamlit app that behaves like a FRED page for interest rates. Use public CSV downloads with no API key:

- Current values: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`
- Values known on a date: `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD`

Cache the two downloads. Start with BAA, FEDFUNDS, DGS10, and MORTGAGE30US selected; include a typed additional series-ID field, a 2020-01-01 start date, and an as-known-on date defaulting to today. Chart current values for each series and report the last observation known on the selected date. The table must include a FRED link, last measured/value known then, last measured/value today, number of current values after the last known date, and number of same-date revised values. A bad ID must not prevent other series from working.

## Required checks

Set the as-known-on date to 2026-10-05. Expected values:

| Series | Last date known | Value |
|---|---|---:|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

Add PAYEMS and set date to 2025-01-15. Expected: December 2024 at 159,536 thousand persons in that vintage; today's value is lower and revised count is above zero.

The submission requires a data card for the student's series (source/link, measure, units, publication lag, revisions, download date), a partner attack answered with evidence, and an admit/quarantine/reject call for Project 2.
