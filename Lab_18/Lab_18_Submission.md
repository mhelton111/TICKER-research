# Lab 18 — Legend Investor as Skill

> **Disclaimer:** This is an educational analysis built from public SEC EDGAR filing facts. It is not investment research, investment advice, or a recommendation to buy, sell, or hold any security. The memo evaluates business-quality signals only; it uses no market-price data.

## Decision question

**Can an investor philosophy become a repeatable skill—every number computed from 10-K facts and the business judgment kept separate?**

## Deliverable and reproducibility

The bundled skill is in `buffett-10k-edgar-skill/SKILL.md`. It directs an AI to use `edgar_buffett.py`, which maps a ticker to its SEC CIK and retrieves public SEC company facts. The script uses only 10-K facts, labels the latest five fiscal years by fiscal-year-end date, selects the latest filing where facts share a period, and prints both values and XBRL tags.

Run live analysis (set a real contact User-Agent first):

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.com"
python edgar_buffett.py COST
streamlit run buffett_10k_app.py
```

Replay the preserved sources used for this submission:

```powershell
python verify_lab18.py
python -m unittest -v test_lab18.py
```

### Deterministic rules

| Item | Rule |
|---|---|
| Revenue | `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues` |
| Net income | `NetIncomeLoss` |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities` |
| Capital spending | `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets` |
| Equity | `StockholdersEquity` |
| ROE | Net income ÷ year-end equity |
| Owner earnings | Operating cash flow − capital spending |
| Missing item | `not found`; dependent metric/check is `not known` |

The script deliberately does not estimate missing data. The Streamlit app shows owner earnings and net income, the fact table, three code checks, the memo, and a memo-number guard. The guard flags a number, such as a hand-typed 40.0% ROE, when it was not printed by the script.

## COST validation — $ millions

| Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE % | Owner earnings |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3 | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1 | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2 | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8 | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8 | 9,382 |

All COST values reproduce the course known answer exactly from preserved SEC company-facts JSON. `verify_lab18.py` confirms the full table, all three checks, and the memo-number guard.

| Buffett check | COST result |
|---|---|
| ROE of 15% or more every year | Pass |
| Owner earnings positive every year | Pass |
| Owner earnings grew, first year to last | Pass |

## Required probe — JPM

The JPM probe keeps capital spending as **not found** for the preferred and fallback tags. Therefore owner earnings remain **not found**, and both owner-earnings checks return **not known** rather than an estimate. This is the intended safe behavior. JPM’s ROE check may independently pass or fail based on its reported annual values; that does not make the missing owner-earnings inputs usable.

## Buffett-style business memo — COST

The generated memo is preserved in [COST_buffett_memo.md](C:\Users\matt_\ai-finance-workspace\Lab_18\COST_buffett_memo.md). It reaches **own the business** as a bounded business-quality verdict because the three mechanical checks pass. That is not a purchase recommendation: no price, valuation, intrinsic value, margin of safety, management assessment, or moat score was invented from the financial statement facts.

**My decision:** I trust the script’s mechanical COST verdict as a transparent first screen because every displayed figure is code-derived from preserved SEC facts and each check is explicit. I would not turn that screen into an investment decision without separate primary-source evidence about the competitive moat and management, plus an independently justified valuation process.

## Partner Q&A and discussion

**Q1: What did the code compute that a model should not invent?**  
**A:** The code selected annual 10-K facts, chose the latest filed fact for a duplicate period, applied tag priorities, converted dollars to millions, calculated ROE, calculated owner earnings, and evaluated the three pass/fail/not-known checks. These are rule-based transformations. Letting a model generate or “clean up” those values would make it difficult to tell whether a difference came from the filing, the formula, or the model.

**Q2: What remained a judgment rather than a calculation?**  
**A:** The memo’s business-quality verdict is judgment. The five-year facts can show persistent ROE and owner earnings, but they cannot by themselves prove a durable competitive moat, the integrity of management, or whether the business is available at an attractive price. The memo must therefore state its evidence boundary instead of turning a screen into certainty.

**Q3: Why does the script require a one-year period for flows?**  
**A:** Revenue, net income, operating cash flow, and capital spending are flows accumulated over a period. A quarterly value and an annual value can share an end date; accepting the quarterly fact would mix incompatible time periods and corrupt owner earnings. The script accepts annual 10-K durations only, including 52- and 53-week fiscal years.

**Q4: Why does the latest filing win if several filings report the same period?**  
**A:** A later 10-K may reclassify or correct a comparative amount. Selecting the fact with the latest filing date is an explicit, reproducible revision rule. It is better than silently taking the first response returned by a JSON array.

**Q5: Why is JPM owner earnings “not known” rather than zero or a substitute calculation?**  
**A:** The specified capital-spending tags are absent in the annual 10-K fact set. Zero would falsely assert that JPM made no capital investment, and a substitute tag would violate the stated rules. Because owner earnings requires both operating cash flow and capital spending, the correct dependent result and its related checks are “not known.”

**Q6: What does the memo-number guard defend against?**  
**A:** It detects unsupported quantitative claims. If someone adds “ROE was 40.0%” to the COST memo, the app flags 40.0 because the script never printed it. The guard does not prove every sentence is insightful, but it creates a concrete provenance boundary between computed facts and prose.

**Q7: Why does high ROE not automatically mean “buy”?**  
**A:** ROE can be high because of a strong business, but it can also be shaped by leverage, accounting, or a small equity base. This lab uses ending equity because that is the assigned rule; a full investment analysis would investigate the balance sheet, returns on incremental capital, business durability, and valuation. This week’s “own the business” language is deliberately not a price recommendation.

**Q8: What would change the COST business-quality verdict?**  
**A:** A failure of one of the three mechanical checks would move the result to watch, and a missing input would move the affected conclusion to not known. Separately, evidence that current owner earnings are not sustainable, that competitive economics are deteriorating, or that the reported facts require material restatement would warrant reassessment. The memo does not claim those risks have been ruled out.

## Reflection

The skill makes source selection, period selection, tag priority, unit conversion, missing-data behavior, formulas, and audit checks identical every time. It leaves the qualitative business interpretation to the memo, but constrains that memo to code-derived numbers. “Not found” is better than an estimate because it tells the reader exactly where the evidence chain stops rather than disguising a missing filing fact as precision.

## Submission contents

- `buffett-10k-edgar-skill/SKILL.md` — reusable skill instructions.
- `edgar_buffett.py` — SEC EDGAR 10-K facts engine and memo generator.
- `buffett_10k_app.py` — Streamlit viewer with charts, checks, memo, and number guard.
- `COST_buffett_memo.md` and `JPM_buffett_memo.md` — generated, bounded business memos.
- `verify_lab18.py` and `test_lab18.py` — replayable validation and focused tests.
- `raw_data/` — SEC ticker map and raw COST/JPM company facts used.
- `lab-18-legend-investor-as-skill.md` and `SOURCES.md` — archived assignment and source ledger.
