# Sources and data lineage

All historical values are USD millions unless noted. Retrieval for the public links: October 19, 2026. No source was used that post-dates the stated historical fact; the price references retain their original as-of dates.

| Input/use | Value/definition | Primary source and as-of | Transformation / qualification |
|---|---|---|---|
| FY2025 revenue | $65,179m | [LLY 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm), filed 2026-02-12 | Base-year income-statement revenue; rounded $m. |
| Mounjaro and Zepbound sales | $22,965m + $13,542m = $36,507m | Same 10-K, MD&A product sales | Personalized cardiometabolic starting driver; remaining revenue is modeled separately. |
| Cash / debt / shares | $7,268m / $42,503m / 899.3m diluted weighted average | Same 10-K, balance sheet, Borrowings note, and EPS statement | Cash/debt bridge uses FY25 balances; share count is an EPS denominator proxy, not current diluted shares. |
| FY2025 assets/equity/OCF/capex | $112,476m / $26,535m / $16,813m / $7,841m | Same 10-K, statements of financial position/cash flows | Used only for base-year reconciliation and model architecture. |
| FY2025 tax rate | 19.8% | Same 10-K, Note 14 Income Taxes | Model rounds to 20.0% for forecast transparency. |
| LLY/AMGN/GILD P/E evidence | See copied `prior_work/Lab_08_comps.md` | [LLY](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm), [Amgen](https://www.sec.gov/Archives/edgar/data/318154/000031815426000010/amgn-20251231.htm), [Gilead](https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm) FY25 filings plus linked historical closes | Equity-value multiple only, consistent annual GAAP diluted EPS basis; two qualified but less cardiometabolic-exposed peers. |
| LLY observed EV/revenue | Synthetic EV $1,077,155m / FY25 revenue $65,179m = 16.52x | 2025 10-K plus preserved 2026-08-31 $1,158.59 close in Edition A | Enterprise-value multiple: equity value + FY25 debt − FY25 cash. It is an observed target multiple, not a standalone valuation. |

## Forecast inputs (analyst judgments, not company facts)

The code labels five-year Mounjaro/Zepbound volume growth, realized-price changes, other-revenue growth, gross margin, R&D, SG&A, capex, working capital, WACC, and terminal growth as forecast assumptions. Their rationale is in `MEMO.md`; adverse evidence that would change them is in `VALIDATION_AND_AI_USE.md`. The $35,000m opening PPE schedule anchor, constant FY2025 debt, 25% net-income distributions, and 4.5% debt-interest rate are model conventions, not reported forecasts.
