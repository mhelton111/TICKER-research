# Lab 08 — Deal Evidence and Valuation Triangulation

**Target:** Eli Lilly and Company (NYSE: LLY)  
**Comparison date:** September 9, 2026, regular-market close  
**Market data convention:** Market-close data was used, not intraday quotes. Each price below is the September 9, 2026 regular-session **4:00 p.m. EDT close**, in USD per share, matching the saved Lab 06 market-price date. Sources are linked in the input table and separately listed in `SOURCES.md`.

## Question and policy before selecting peers

**Question:** What would LLY's share be worth at defensible peer P/E multiples, and how does that compare with the saved DCF?

**Policy written before reviewing multiples:** Use U.S.-listed operating companies that discover, develop, manufacture, and market human therapeutics; have positive FY2025 reported GAAP diluted EPS available by Sept. 9, 2026; and report in U.S. dollars per share. Qualify rather than hide material differences in therapeutic mix, growth rate, product concentration, geography, and acquisition effects. Exclude companies without compatible positive annual GAAP EPS or a comparable operating model. Do not use cash or debt to bridge a P/E-derived equity value.

**Rejection criteria:** an ETF, distributor, insurer, or contract manufacturer rather than an operating drug company; negative or unavailable annual reported diluted EPS; an annual result published after the comparison date; a non-USD/share-basis mismatch; or a business model whose evidence cannot be verified.

## Target, candidates, and source decisions

The earnings basis is **FY2025 total GAAP diluted EPS**, not adjusted EPS. All fiscal years ended Dec. 31, 2025; all three annual results were public before Sept. 9, 2026. Prices and EPS are USD per share and use the same share basis within each company.

| Company | Market-close data used: Sept. 9, 2026, 4:00 p.m. EDT | FY2025 GAAP diluted EPS | Fiscal year / publication date | Decision and business reason | Source locator |
|---|---:|---:|---|---|---|
| Eli Lilly (LLY), target | $1,124.21 | $22.95 | Dec. 31, 2025 / Feb. 4, 2026 | Target. Lilly discovers, develops, manufactures, and markets human pharmaceutical products in one segment. | [2025 Form 10-K, Item 1—Business](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm); [FY2025 results](https://investor.lilly.com/news-releases/news-release-details/lilly-reports-fourth-quarter-2025-financial-results-and-provides), reported diluted EPS row; [Sept. 9 price history](https://ca.finance.yahoo.com/quote/LLY/history/). |
| Amgen (AMGN), candidate | $391.27 | $14.23 | Dec. 31, 2025 / Feb. 3, 2026 release; Feb. 13, 2026 10-K | **Use, qualified.** Amgen discovers, develops, manufactures, and delivers human therapeutics, matching the core operating model. Its portfolio and growth profile are more mature and less dependent on cardiometabolic products than Lilly's; that difference limits the comparison. | [2025 Form 10-K, Overview and Item 1—Business](https://www.sec.gov/Archives/edgar/data/318154/000031815426000010/amgn-20251231.htm); [FY2025 results](https://investors.amgen.com/news-releases/news-release-details/amgen-reports-fourth-quarter-and-full-year-2025-financial/), full-year GAAP EPS; [Sept. 9 price history](https://stockanalysis.com/stocks/amgn/history/). |
| Gilead (GILD), candidate | $145.65 | $6.78 | Dec. 31, 2025 / Feb. 10, 2026 | **Use, qualified.** Gilead discovers, develops, and delivers medicines in virology, oncology, and other therapeutic areas. Its HIV/virology concentration and materially lower growth differ from Lilly's cardiometabolic-led portfolio; its multiple is therefore a cautious reference, not a direct substitute. | [2025 Form 10-K, Item 1—Business](https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm); [FY2025 results](https://investors.gilead.com/news/news-details/2026/Gilead-Sciences-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx), full-year diluted EPS; [Sept. 9 price history](https://www.investing.com/equities/gilead-sciences-inc-historical-data). |

## Peer P/E calculation and validation

Run `python lly_comps.py` from this folder. The script deduplicates peers, excludes LLY from its own peer set, retains full precision until display, and does not fetch data or use packages.

| Check | Calculation | Result |
|---|---|---:|
| LLY observed P/E, comparison only | $1,124.21 / $22.95 | 48.985185x |
| Amgen P/E | $391.27 / $14.23 | 27.496135x |
| Gilead P/E | $145.65 / $6.78 | 21.482301x |
| Peer median P/E | midpoint of the two unrounded peer multiples | 24.489218x |
| LLY implied range | minimum to maximum peer P/E × $22.95 | $493.02-$631.04 |
| LLY at peer median | 24.489218x × $22.95 | $562.03 |

**Hand check:** Amgen P/E is $391.27 / $14.23 = **27.496135x**, matching the calculator.

**Changed-peer prediction and result:** Removing Amgen, the higher-multiple peer, should lower the median-implied price. The calculator leaves Gilead's one-peer reference estimate of **$493.02**, a **-$69.01** change from the two-peer median. One remaining peer gives no range, so it supplies less information. Removing Gilead instead leaves the Amgen reference estimate of $631.04 (+$69.01).

## DCF comparison and skeptical review

| Method | LLY result and date | Main assumption or limitation |
|---|---|---|
| Saved Week 3 DCF | Base value $218.11/share; sensitivity range $165.71-$311.99; model run Sept. 10, 2026 using the Sept. 9 close as its target-price date | Five-year FCFF-growth path, 10% WACC, 3% terminal growth, and terminal value share of enterprise value. |
| Peer P/E | $493.02-$631.04; median $562.03; Sept. 9, 2026 market close | Two qualified but slower-growth human-therapeutics peers; FY2025 GAAP EPS can include acquisition, impairment, or other non-operating effects. |

The P/E range is above the DCF range but below the **September 9 market-close price**. These methods should **not** be mechanically averaged: the DCF is driven by a specific Lilly FCFF forecast, while the P/E range imports the market multiples of two slower-growth peers.

**Skeptical-colleague criticism:** The weakest supported assumption is that Amgen and Gilead's P/E multiples can benchmark Lilly despite Lilly's unusually large cardiometabolic franchise and much faster recent growth. The comparison is date-consistent and uses the same reported-GAAP annual EPS basis, but it is not a close growth-profile match. **Question that could change the decision:** Can a sourced peer set with comparable cardiometabolic exposure, growth, and sustainable margins support a materially higher P/E range without mixing currencies or adjusted earnings?

**Judgment of the criticism: Accept.** Lilly's 2025 Form 10-K states Mounjaro and Zepbound represented 56% of 2025 revenue, confirming that its concentration and growth profile differ materially from the two peers. The present peer range remains a qualified reference rather than proof of value.

## Conditional conclusion

**Watch-defer for this course exercise.** The **September 9 market-close price** is above both the saved DCF range and this qualified peer-P/E range; neither result alone establishes an investment conclusion. Reconsider if updated, source-supported evidence shows durable FCFF growth and margins beyond the current DCF path, or if a more comparable peer set supports a different defensible range. Monitor quarterly Mounjaro/Zepbound volume, realized price, operating cash flow, and capital expenditure.

This is a course exercise, not investment advice. AI assistance: drafted with Codex; sources, peer decisions, and judgments are presented for review.
