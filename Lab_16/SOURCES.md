# Lab 16 sources and provenance

## Data used in calculations

| Source | Used for | Accessed | Local preservation |
|---|---|---|---|
| Course-authored fictional card-spend-index table in Lab 16 | Every input row and all calculated results | 2026-10-27 | `lab-16-provenance-gate.md`; copied verbatim into `asof.py` as editable `ROWS` |

No live FRED, ALFRED, market-price, 10-K, or 10-Q data are inputs to this training-table calculation. This is intentional: the course specifies a fictional known-answer table.

## Conceptual / implementation references

| Source | Relevant point | URL | Accessed |
|---|---|---|---|
| ALFRED, Federal Reserve Bank of St. Louis | Retrieves the data-release vintage available on a specified date in history. | https://alfred.stlouisfed.org/ | 2026-10-27 |
| FRED API documentation: `series/observations` | Documents observation retrieval and the `realtime_start`, `realtime_end`, and `vintage_dates` parameters used for point-in-time work. | https://fred.stlouisfed.org/docs/api/fred/series_observations.html | 2026-10-27 |

## Reproducibility note

The source table, filter code, tests, and completed analysis are all stored in this folder. A future real-data extension should add the downloaded raw vintage extract to this folder before transforming it, retain the query URL/parameters, and never overwrite the raw file.
