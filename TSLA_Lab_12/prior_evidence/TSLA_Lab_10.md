# Lab 10 — Tesla, Inc. (NASDAQ: TSLA) company-specific pro forma

**Prepared September 24, 2026.** All dollars are USD millions except per-share figures.  This is TSLA, the assigned company—not the LLY version prepared before the company correction.  The executable model is `tsla_proforma.py`; every external source and filing location is in `SOURCES.md`.

## 1. Three-year history

Operations history comes from Tesla’s audited 2025 10-K, Item 8, p. 50 (S1).  FY2025/FY2024 balance-sheet data comes from p. 49 (S2), with the FY2023 balance sheet independently cross-checked to the 2024 10-K (S3).

| Fiscal year ended Dec. 31 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Revenue | 96,773 | 97,690 | 94,827 |
| Gross profit | 17,660 | 17,450 | 17,094 |
| SG&A | 4,800 | 5,150 | 5,834 |
| Net income | 14,974 | 7,153 | 3,855 |
| Inventory | 13,626 | 12,017 | 12,392 |
| PP&E, net | 29,725 | 35,836 | 40,643 |
| Total stockholders’ equity | 62,634 | 72,913 | 82,137 |

**Manual checks:** (1) 2025 gross profit equals $94,827 − $77,733 cost of revenues = **$17,094**. (2) 2025 stockholders’ equity equals common stock $3 + APIC $42,770 + AOCI $361 + retained earnings $39,003 = **$82,137**. Both agree to the 2025 10-K, pp. 49–50 (S1–S2).

| Ratio / filed input | 2023 | 2024 | 2025 | Calculation / source |
|---|---:|---:|---:|---|
| Reported revenue growth | 18.8% | 0.9% | (2.9%) | year-over-year revenue; S1 |
| Gross margin | 18.2% | 17.9% | 18.0% | gross profit ÷ revenue; S1 |
| SG&A ÷ gross profit | 27.2% | 29.5% | 34.1% | SG&A ÷ gross profit; S1 |
| Inventory days | 62.9 | 54.7 | 58.2 | ending inventory ÷ cost of revenues × 365; S1–S3 |
| Depreciation ÷ year-end PP&E | 11.2% | 11.5% | 12.4% | depreciation ÷ PP&E; S5 |
| Capex | 8,899 | 11,342 | 8,527 | purchases of PP&E, net of sales; S4 |
| Effective tax rate | (50.1%) | 20.4% | 27.0% | tax provision ÷ pretax income; S1 |
| Organic / same-store growth | N/A | N/A | N/A | Tesla does not report either a company-wide organic or same-store metric. |

Tesla reports total revenue and discusses changes by automotive, energy, services, product mix, pricing and volume in Item 7 (S6); it does not give a comparable same-store/organic measure.  “N/A” is therefore more accurate than inventing one.

## 2. Assumptions

| Assumption | 2026 | 2027 | 2028 | 2029 | 2030 | Label and reason |
|---|---:|---:|---:|---:|---:|---|
| Revenue growth | 6% | 10% | 12% | 12% | 10% | **Judgment:** starts cautiously after 2025’s 2.9% decline, then reflects ramp/AI and energy opportunities discussed in Item 7; not company revenue guidance. |
| Gross margin | 18% | 20% | 22% | 24% | 26% | **History + judgment:** starts at FY2025’s 18.0%; later improvement is the model’s required scale/mix assumption, not disclosed guidance. |
| R&D / revenue | 7.5% each year |  |  |  |  | **History + judgment:** FY2025 was 6.8%; modestly higher rate reflects continued autonomy/AI investment (S1, S6). |
| SG&A / gross profit | 33% | 31% | 29% | 27% | 25% | **History + judgment:** FY2025 was 34.1%; gradual scale benefit, not a sharp cost cut. |
| Inventory days | 58 | 56 | 54 | 53 | 52 | **History + judgment:** close to FY2025’s 58.2 days, with gradual supply-chain efficiency. |
| Depreciation / PP&E | 12.4% each year |  |  |  |  | **History:** matches FY2025; S5. |
| Capex | 20,000 | 17,000 | 14,000 | 12,000 | 10,000 | **Guidance + judgment:** Tesla says 2026 capex will exceed $20bn (S6); later years fade from that investment peak. |
| Tax rate | 27% each year |  |  |  |  | **History:** FY2025 effective rate; S1. |
| Interest income / expense | 3.8% / 4.0% |  |  |  |  | **Judgment:** makes the unusually large liquid-investment portfolio and debt explicit; filed 2025 interest income/expense were $1,680/$338 (S1). |
| Debt repayment | 0 each year |  |  |  |  | **Judgment:** no asserted repayment schedule; debt is held constant rather than invented. |
| Minimum liquidity / revolver | 2,000 / 5,000 |  |  |  |  | **Judgment / filing:** model liquidity floor; filed unused RCF capacity is $5bn (S6). |
| Floor-plan financing | **None (0)** | **None (0)** | **None (0)** | **None (0)** | **None (0)** | Tesla does not fund franchised dealers’ inventory: it sells directly. This is an explicit company-specific zero, not a missing assumption. |
| WACC / terminal growth | 10% / 3% |  |  |  |  | **Judgment:** required return and a mature long-run growth rate. |

## 3. Five-year engine and checks

The model carries cash plus short-term investments as one liquid-balance line (opening $44,059), because both are available liquidity in Tesla’s balance sheet.  It separately forecasts inventory, PP&E, other assets/liabilities, debt, equity, and cash.  Tesla pays no cash dividend; equity therefore rolls forward with net income.  Negative FCFE in 2026–2029 is retained rather than “fixed”: the disclosed >$20bn 2026 capex program makes this a genuine cash-use case.  Cash remains above the $2bn floor, so the revolver is not drawn.

| Year | Revenue | Net income | FCFE | Cash + investments | Debt | Total equity | Balance check |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026 | 100,516.6 | 644.6 | (14,992.7) | 29,066.3 | 8,376.0 | 83,509.6 | 0.0 |
| 2027 | 110,568.3 | 613.5 | (9,915.1) | 19,151.3 | 8,376.0 | 84,123.2 | 0.0 |
| 2028 | 123,836.5 | 1,679.3 | (4,825.8) | 14,325.5 | 8,376.0 | 85,802.4 | 0.0 |
| 2029 | 138,696.9 | 3,820.3 | (247.6) | 14,077.9 | 8,376.0 | 89,622.7 | 0.0 |
| 2030 | 152,566.5 | 6,750.1 | 5,302.4 | 19,380.3 | 8,376.0 | 96,372.8 | 0.0 |

The script raises an error if an annual balance check exceeds $0.01 million.  All five displayed checks are zero after rounding.

## 4. FCFE value and market comparison

| Output | Amount |
|---|---:|
| PV of explicit FCFE | $(22,326.4) |
| Terminal value at 2030 | $78,021.3 |
| Equity value | $26,118.7 |
| Shares used | 3,752.432 million |
| **Model value per share** | **$6.96** |

The latest fully **market-closed** regular-session TSLA price when this was prepared was **$380.12 on September 23, 2026 at 4:00 p.m. EDT** (S7).  September 24 was still trading, so no intraday value is called a close.  This model’s $6.96 per share is far below the $380.12 market close; that is an observation, not a recommendation.

### Why the model value is only $6.96 per share

The low value is a consequence of this particular FCFE model, not a claim that the market price is an error.  The model preserves Tesla’s near-term cash burden: it uses the company’s stated expectation that 2026 capex will exceed $20 billion (S6), while revenue growth begins at only 6% after FY2025 revenue declined 2.9%.  As a result, forecast FCFE is negative for 2026–2029 and its discounted value is **$(22.3) billion**; those cash outflows consume much of the benefit of later operating improvement.

The terminal value assumes gross margin recovers only gradually from 18.0% in FY2025 to 26.0% in 2030, with a 10% WACC and 3% terminal-growth rate.  That still produces a positive $78.0 billion terminal value, but after discounting it and subtracting the negative explicit-period FCFE, the modeled equity value is only $26.1 billion.  Dividing by 3.752 billion shares produces $6.96 per share.  The large gap to the market price suggests investors may be assigning substantially more value to autonomy, AI, robotics, energy growth, margin expansion, or a faster cash-flow inflection than this deliberately conservative base case includes.

**Decision-changing question:** Can Tesla turn the planned AI, autonomy, robotics and capacity spending into a much higher long-run gross margin and positive FCFE sooner than this base case assumes?  The answer matters because most of the gap to the market price cannot be closed by minor terminal-growth changes alone.

## 5. Skeptical partner review

**Partner attack:** The 26% 2030 gross-margin assumption is the least supported input because it is well above the 17.9%–18.2% history and depends on unproven mix/AI economics.  If that recovery does not occur, the terminal FCFE and the already-low $6.96 per-share result fall further.

**Response:** I agree it is the key judgment, and it is explicitly labeled rather than presented as guidance.  Before changing the conclusion, I would obtain evidence of sustained segment/product margin improvement and cash conversion; I would not average methods or invent an unsupported valuation range.

## Submission checklist

- [x] Correct company: TSLA.
- [x] Three 10-K years, source pages/sections, manual checks, and ratio history.
- [x] Labeled assumptions including Tesla-specific no-floor-plan/direct-sales treatment.
- [x] Five-year balanced engine, cash floor/revolver check, and negative-FCFE treatment.
- [x] Dated market-close comparison, sourced valuation, organic-growth explanation, and partner critique.
