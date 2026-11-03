# Lab 18 sources and provenance

| Source | Used for | URL | Accessed |
|---|---|---|---|
| Course Lab 18 instructions | Required rules, validation targets, probes, and deliverables | https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md | 2026-11-03 |
| SEC EDGAR API documentation | Public keyless API, ticker map, CIK padding, and companyfacts endpoint | https://www.sec.gov/search-filings/edgar-application-programming-interfaces | 2026-11-03 |
| SEC ticker map | Ticker-to-CIK mapping | https://www.sec.gov/files/company_tickers.json | 2026-11-03 |
| SEC COST company facts | COST 10-K XBRL facts used in validation | https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json | 2026-11-03 |
| SEC JPM company facts | JPM missing-capital-spending probe | https://data.sec.gov/api/xbrl/companyfacts/CIK0000019617.json | 2026-11-03 |
| FAskills Buffett page | Philosophy context only; no FAskills data or software used | https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md | 2026-11-03 |

## Preserved raw inputs

`raw_data/company_tickers.json`, `raw_data/COST_companyfacts.json`, and `raw_data/JPM_companyfacts.json` are the exact public SEC downloads used for the completed validation. They were downloaded on 2026-11-03 using an educational SEC User-Agent. No market-price data, FRED data, Financial Datasets data, API key, or personal contact information is stored in this folder.
