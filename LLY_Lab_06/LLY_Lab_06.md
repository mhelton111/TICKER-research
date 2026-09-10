# Lab 06 — Sensitivity, Reverse DCF, and Conditional Recommendation

**Company:** Eli Lilly and Company (NYSE: LLY)  
**Lab date:** September 10, 2026  
**Market status:** Market closed. The target is the most recent completed NYSE session: **$1,124.21 at the Sept. 9, 2026, 4:00 p.m. EDT close.**

## Inputs and sources

All dollar amounts are USD millions except share price and per-share values. Financial-statement inputs are from Lilly's latest annual filing available at the lab date: the 2025 Form 10-K, filed February 12, 2026.

| Input | Value used | Status and calculation | As-of date and exact locator |
|---|---:|---|---|
| Starting FCFF | 9,479.666 | 16,813 operating cash flow + 633 cash interest paid x (1 - 19.8% tax rate) - 7,841 purchases of property and equipment | Dec. 31, 2025; 2025 Form 10-K, Consolidated Statements of Cash Flows, p. 60; Note 14—Income Taxes, p. 86. |
| Growth, Years 1-5 | 25%, 20%, 15%, 10%, 5% | **Estimate.** The path deliberately decelerates from 2025 revenue growth of 45% and Q2 2026 revenue growth of 48%. | 2025 Form 10-K, Item 7—MD&A, pp. 43, 49; Lilly Q2 2026 earnings release, Aug. 5, 2026, p. 1. |
| WACC | 10% | **Estimate.** Conservative working assumption to revisit using a current risk-free rate, beta, debt-note yield, and market-value weights. | Sept. 10, 2026; estimate, not a filing fact. |
| Terminal growth | 3% | **Estimate.** Long-run nominal-economy assumption, not a company-specific forecast. | Sept. 10, 2026; estimate. |
| Cash | 7,268 | Cash and cash equivalents. | Dec. 31, 2025; 2025 Form 10-K, Consolidated Balance Sheets, p. 59. |
| Debt | 42,503 | Total debt. | Dec. 31, 2025; 2025 Form 10-K, Note 11—Borrowings, p. 76. |
| Diluted weighted-average shares | 899.3 | Diluted shares used in EPS calculation. | Year ended Dec. 31, 2025; 2025 Form 10-K, Consolidated Statements of Operations, p. 57. |
| Target share price | $1,124.21 | Latest completed close when checked; market closed. | Sept. 9, 2026, 4:00 p.m. EDT; [StockAnalysis LLY price history](https://stockanalysis.com/stocks/lly/history/). |

Primary filing: [Lilly 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm).

## Model result and reasonableness

Run `python dcf.py` from this folder for the exact output. The base case is **$218.11 per diluted share** versus the $1,124.21 target price (0.19x), outside the 0.5x-2x reasonableness band. I did not alter assumptions to make it match.

The input I distrust most is the five-year FCFF-growth path. It begins with a one-year cash-flow base and does not explicitly model the timing, scale, or margins of the obesity portfolio; small changes have a large effect because terminal value is a substantial share of enterprise value.

## Sensitivity and reverse DCF

The grid holds all operating inputs and the equity bridge fixed. Its centre is the 10% WACC / 3% terminal-growth base case. Value falls as WACC rises and rises as terminal growth rises. The grid range is **$165.71** at 11% WACC / 2% terminal growth to **$311.99** at 9% WACC / 4% terminal growth.

The reverse DCF uses bisection in the required -5 to +10 percentage-point bracket. It solves for a uniform shift applied to all five forecast growth rates while holding starting FCFF, WACC, terminal growth, cash, debt, and diluted shares fixed. LLY's $1,124.21 price is not reachable inside that bracket, so the script correctly reports no solution rather than presenting a bound as the implied growth.

## Conditional call

**Watch-defer.** Initiate only if the price drops into a range supported by my forecast path, or new sourced evidence supports materially higher durable FCFF growth and margins. Otherwise, defer. Monitor the next quarter's operating cash flow, capital expenditure, and Mounjaro/Zepbound volume and realized-price trends.

## Completion checks

- `python dcf.py` prints the twelve baseline DCF lines, the nine-cell grid, and the reverse-DCF result from one file and one command.
- The grid keeps the 10% / 3% base case in the middle, rises to the right, and falls down.
- The reverse DCF rejects an unreachable target within its configured bracket instead of returning a bound.
- The training-case check produces the required grid and a +1.7780 percentage-point growth shift at a $30.00 target.

This is a course exercise, not investment advice. AI assistance: drafted with Codex; source locations and judgments are presented for review.
