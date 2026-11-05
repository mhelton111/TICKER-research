# Lab 19 sources and provenance

| Source | Used for | URL | Accessed |
|---|---|---|---|
| Course Lab 19 instructions | Rules, known answer, threshold probe, and deliverables | https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md | 2026-11-05 |
| SEC EDGAR API documentation | Public keyless facts API, CIK mapping, and companyfacts endpoint | https://www.sec.gov/search-filings/edgar-application-programming-interfaces | 2026-11-05 |
| SEC ticker map | Ticker-to-CIK mapping | https://www.sec.gov/files/company_tickers.json | 2026-11-03 snapshot reused; source accessed 2026-11-05 |
| SEC COST company facts | COST 10-K facts for required validation | https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json | 2026-11-03 snapshot reused; source accessed 2026-11-05 |
| SEC LLY company facts | LLY 10-K facts for single-company panel | https://data.sec.gov/api/xbrl/companyfacts/CIK0000059478.json | 2026-11-05 |
| FAskills Graham page | Graham philosophy context only; no FAskills data/software used | https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md | 2026-11-05 |
| FAskills Burry page | Burry philosophy context only; no FAskills data/software used | https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md | 2026-11-05 |

## Data handling

All numerical inputs are public SEC EDGAR 10-K company-facts data. Exact JSON downloads used in the completed calculations are saved under `raw_data/`. No market-price data, market-close data, FRED data, Financial Datasets data, API key, or personal contact information is stored in this folder.
