# Lab 17 sources and provenance

| Source | Used for | URL | Accessed |
|---|---|---|---|
| Course Lab 17 instructions | Requirements, required IDs, known-answer and PAYEMS validation targets | https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md | 2026-10-29 |
| FRED graph CSV endpoint | Latest/current series values | https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES | 2026-10-29; fetched live by app |
| ALFRED graph CSV endpoint | Historical vintage values as known on selected date | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD | 2026-10-29; fetched live by app |
| FRED DGS10 series page | DGS10 definition, units, frequency, source metadata | https://fred.stlouisfed.org/series/DGS10 | 2026-10-29 |
| FRED BAA series page | BAA definition, units, frequency, and source metadata | https://fred.stlouisfed.org/series/BAA | 2026-10-29 |
| FRED FEDFUNDS series page | FEDFUNDS definition, units, frequency, and source metadata | https://fred.stlouisfed.org/series/FEDFUNDS | 2026-10-29 |
| FRED MORTGAGE30US series page | Mortgage-rate definition, units, frequency, and source metadata | https://fred.stlouisfed.org/series/MORTGAGE30US | 2026-10-29 |
| FRED/ALFRED documentation | Point-in-time observation and vintage-date implementation context | https://fred.stlouisfed.org/docs/api/fred/series_observations.html | 2026-10-29 |

## Data handling

The app intentionally uses public graph CSV downloads, as specified in the course instructions. No FRED API key, Financial Datasets credential, user account information, or other secret is stored in this folder. The downloads are live, so source content may change after the access date. For a permanent research record, save an immutable raw CSV export alongside its request URL, vintage date, and retrieval timestamp.

## Preserved verification downloads

The following raw CSV files were downloaded on 2026-10-29 and are saved in `raw_data/`. They are the direct evidence behind `verify_lab17.py` and the verification record in the submission.

| Local file | Source URL |
|---|---|
| `BAA_2026-10-05.csv` | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-05 |
| `FEDFUNDS_2026-10-05.csv` | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=FEDFUNDS&vintage_date=2026-10-05 |
| `DGS10_2026-10-05.csv` | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05 |
| `MORTGAGE30US_2026-10-05.csv` | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=MORTGAGE30US&vintage_date=2026-10-05 |
| `PAYEMS_2025-01-15.csv` | https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15 |
| `PAYEMS_current.csv` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS |
