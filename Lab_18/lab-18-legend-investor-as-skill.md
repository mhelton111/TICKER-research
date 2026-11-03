# Lab 18 — Legend Investor as Skill (course instructions archive)

Source: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md  
Accessed: 2026-11-03

## Required rules

- Use SEC EDGAR company facts and 10-K filings only, for the latest five fiscal years labelled by fiscal-year-end date.
- For same-period facts in multiple filings, the latest filing wins.
- Revenue: `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`.
- Net income: `NetIncomeLoss`; operating cash flow: `NetCashProvidedByUsedInOperatingActivities`.
- Capital spending: `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`.
- Equity: `StockholdersEquity`; ROE is net income ÷ year-end equity; owner earnings is operating cash flow − capital spending.
- A missing value is `not found`, never an estimate. A dependent check with a missing input is `not known`.
- Compute: ROE ≥15% each year; owner earnings positive each year; and owner earnings growth from first year to last.
- Create a Streamlit app with chart, table, checks, memo, and memo-number flagging; no price data.

## Required validation

For COST, the five annual rows must match the course table ending in FY2026: revenue 303,154; net income 9,226; operating cash flow 15,817; capital spending 6,435; equity 35,803; ROE 25.8%; owner earnings 9,382 (all $ millions). All three checks pass.

For JPM, capital spending and owner earnings must remain `not found`, and both owner-earnings checks must be `not known`. A manually typed number not printed by the script (such as 40.0% ROE) must be flagged.
