---
name: buffett-10k-edgar
description: Analyze a public company with five annual 10-K SEC EDGAR facts, Buffett-style owner earnings, and explicit missing-data handling. Use for Lab 18 or point-in-time 10-K business-quality analysis; do not use for valuation or price targets.
---

# Buffett 10-K EDGAR analysis

Run `python edgar_buffett.py TICKER` from this Lab_18 folder. The script retrieves only SEC `company_tickers.json` and the companyfacts endpoint, then selects 10-K facts only. It labels the last five fiscal years by fiscal-year end and selects the latest filing for duplicate facts.

Use these fixed rules:

- Revenue: `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`.
- Net income: `NetIncomeLoss`; operating cash flow: `NetCashProvidedByUsedInOperatingActivities`.
- Capital spending: `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`.
- Equity: `StockholdersEquity`; ROE = net income ÷ year-end equity.
- Owner earnings = operating cash flow − capital spending.
- Print `not found` for missing facts. If equity is zero/below or an input is missing, print `not known` for the affected check; never estimate.

Treat code outputs as facts and the memo as a bounded business-quality judgment. The memo may only cite printed values, must not use price data, and should give one of: own the business, watch, or pass. Preserve the generated memo file beside the code.
