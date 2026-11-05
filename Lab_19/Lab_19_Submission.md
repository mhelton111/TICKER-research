# Lab 19 — Legend Panel

> **Disclaimer:** This is an educational analysis based on public SEC EDGAR 10-K facts. It is not investment research, investment advice, or a recommendation to buy, sell, or hold any security. No market-price data were used.

## Decision question

**When three investor skills read the same 10-K facts, where do they agree, where do they split, and would the panel be trustworthy as a screen?**

## Deliverable and reproducibility

`legend_panel.py` uses the same SEC company-facts source and 10-K-only methodology as Lab 18. It adds `Liabilities`, `AssetsCurrent`, and `LiabilitiesCurrent`; calculates current ratio and liabilities-to-equity; and runs three separate deterministic check sets. The bundled Graham and Burry skills are in `graham-10k-edgar-skill/SKILL.md` and `burry-10k-edgar-skill/SKILL.md`; discoverable Codex pointers are installed in the local skills directory.

Run live analysis (enter an accurate contact User-Agent before a live SEC request):

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.com"
python legend_panel.py LLY
streamlit run legend_panel_app.py
```

Replay the completed analysis from exact public SEC downloads preserved in `raw_data/`:

```powershell
python verify_lab19.py
python -m unittest -v test_lab19.py
```

The Streamlit app provides the investor-by-check panel, shared fact table, cash/earnings chart, three side-by-side memos, and a separate unsupported-number guard for every memo.

## Rules in code

| Investor | Checks |
|---|---|
| Buffett | ROE ≥15% every year; owner earnings positive every year; owner earnings grew first year to last. |
| Graham | Latest current ratio ≥2.0; net income positive every year; net income grew first year to last. |
| Burry | Operating cash flow ≥ net income every year; latest liabilities ÷ equity ≤2.0. |

All values come from five annual 10-K fact rows. Revenue, net income, operating cash flow, capital spending, and equity follow the Lab 18 tag-priority rules. A missing input prints `not found`; any dependent calculation or check prints `not known`, never an estimate.

## COST known-answer validation

| Fiscal year end | 2022-08-28 | 2023-09-03 | 2024-09-01 | 2025-08-31 | 2026-08-30 |
|---|---:|---:|---:|---:|---:|
| Current ratio | 1.02 | 1.07 | 0.97 | 1.03 | 1.06 |
| Liabilities ÷ equity | 2.11 | 1.75 | 1.96 | 1.64 | 1.49 |

| Investor | Check | COST result |
|---|---|---|
| Buffett | ROE of 15% or more every year | Pass |
| Buffett | Owner earnings positive every year | Pass |
| Buffett | Owner earnings grew, first year to last | Pass |
| Graham | Current ratio of 2.0 or more, latest year | Fail (1.06) |
| Graham | Net income positive every year | Pass |
| Graham | Net income grew, first year to last | Pass |
| Burry | Operating cash flow at least net income every year | Pass |
| Burry | Liabilities no more than twice equity, latest year | Pass (1.49) |

The code-generated panel exactly matches the course known answer: **Buffett 3 of 3; Graham 2 of 3; Burry 2 of 2.** The four saved raw SEC files and `verify_lab19.py` reproduce the result without a live download.

## Threshold probe

With Graham’s current-ratio threshold temporarily changed from **2.0** to **1.0**, COST passes all three Graham checks because its latest current ratio is 1.06. The threshold was restored to **2.0**. I retain 2.0 because it is the course’s specified conservative liquidity screen; lowering a threshold changes the screen’s design, not Costco’s 10-K facts.

## My company panel — Eli Lilly (LLY)

LLY is used as the requested single-company analysis. No market data were needed, so the 11/4/2026 market-close instruction does not apply. The panel uses five annual 10-K fiscal years ending 2021–2025 from the SEC company-facts snapshot downloaded 2026-11-05.

| Investor | LLY result |
|---|---|
| Buffett | ROE ≥15% every year: Pass; owner-earnings checks: Not known because the specified capital-spending fact is not found. |
| Graham | Current ratio latest year: Fail (1.58 versus 2.0); net income positive every year: Pass; net income grew first to last: Pass. |
| Burry | Operating cash flow ≥ net income every year: Fail; liabilities ÷ equity latest year: Not known because the specified `Liabilities` fact is not found. |

The LLY gaps remain visible. The script does not substitute another capital-spending or liability tag merely to complete a ratio. The three generated LLY memos are saved as `LLY_buffett_memo.md`, `LLY_graham_memo.md`, and `LLY_burry_memo.md`; all memo-number guards pass.

## Bull and bear from the same panel

**Bull case:** LLY passes the ROE and net-income-growth screens, and the latest current ratio of 1.58 is an improvement over earlier years in the shared panel. Those outputs support the view that reported profitability has strengthened even though the conservative Graham liquidity threshold is not met.

**Bear case:** The panel does not permit a confident owner-earnings judgment because the specified capital-spending fact is absent, and Burry’s cash-flow-versus-net-income check fails. The current-ratio failure and missing liabilities input mean that neither liquidity nor leverage should be treated as cleared by this screen.

## Partner Q&A and discussion

**Q1: Why can three investors disagree when they receive the same five rows?**  
**A:** They apply different decision rules to the same evidence. Buffett emphasizes durable returns and owner earnings; Graham prioritizes a conservative current ratio and earnings stability; Burry compares cash conversion with accounting profit and constrains leverage. The facts do not change, but the threshold and the question each skill asks change the verdict.

**Q2: What did the COST result teach about a screen versus a business judgment?**  
**A:** COST passes all Buffett checks and both Burry checks but fails Graham’s 2.0 current-ratio rule at 1.06. That does not prove Costco is weak; it shows that its short-term balance-sheet structure does not meet this particular conservative liquidity screen. A panel should expose that disagreement rather than averaging it away.

**Q3: What happens when Graham’s threshold changes to 1.0?**  
**A:** COST then passes the current-ratio check because 1.06 exceeds 1.0, changing Graham from 2 of 3 to 3 of 3. The underlying assets, liabilities, income, and cash flow do not move—the rule moves. This is why thresholds must be declared before examining the result and recorded when changed.

**Q4: Why is LLY owner earnings “not known” rather than estimated from a different cash-flow label?**  
**A:** The assignment specifies two permitted capital-spending tags. Neither produced the required annual 10-K input in the saved LLY fact set, so owner earnings cannot be computed under the stated method. Replacing the missing input with a convenient alternative would silently change the definition and destroy comparability with COST.

**Q5: What is the most important limitation of Burry’s cash-flow test?**  
**A:** Operating cash flow below net income is a flag, not proof of poor earnings quality or fraud. It can reflect working-capital timing, business investment, or other legitimate factors. The panel identifies where deeper filing and footnote work belongs; it does not make a forensic conclusion from one comparison.

**Q6: How does the memo-number guard work across all three investors?**  
**A:** The code builds an allowed set from every fiscal-end date and computed table value, plus the stated threshold. It scans each memo separately. A manually added 40.0 is flagged for the memo where it appears because no script output printed that number; the test verifies this behavior.

**Q7: Does the panel recommend buying or shorting LLY?**  
**A:** No. It is a business and financial-statement screen without price, valuation, market data, or a full qualitative diligence record. The correct conclusion is about evidence quality and screen results, not a trading action.

**Q8: Would I let this panel screen Project 2 companies?**  
**A:** **Only with a condition:** use it as a transparent first-pass screen after preserving the five 10-K source rows and require a human review of every failure and every `not known` result. It may prioritize follow-up work, but it cannot substitute for valuation, business-risk research, or an explanation of missing facts.

## Reflection

The panel agrees that a mechanical result should come from code and source facts, but it splits because its screens express different definitions of strength. COST’s threshold probe shows that screening outcomes are partly design choices. On LLY, the correct response to a missing fact is to preserve the gap and narrow the conclusion; “not known” is evidence of a limit, not a defect to hide.

## Submission contents

- `legend_panel.py` — 10-K-only SEC facts engine, investor checks, memos, and memo-number guard.
- `legend_panel_app.py` — Streamlit panel interface with chart, table, checks, and side-by-side memos.
- `graham-10k-edgar-skill/SKILL.md` and `burry-10k-edgar-skill/SKILL.md` — two bundled investor skills.
- `COST_*_memo.md`, `LLY_*_memo.md`, and `threshold_probe/` — generated memo records and threshold test output.
- `verify_lab19.py` and `test_lab19.py` — replayable validation and focused tests.
- `raw_data/` — exact SEC JSON downloads used for COST and LLY.
- `lab-19-legend-panel.md` and `SOURCES.md` — archived assignment and source ledger.
