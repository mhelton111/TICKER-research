# Lab 11 — TSLA pro-forma what-if: find the drivers

**Prepared September 29, 2026.** Dollar amounts are USD millions except per-share values. This analysis extends the existing Tesla Lab 10 model; it does not replace it. The working sensitivity script is `tsla_sensitivity.py`; sources are in `SOURCES.md`.

## Base model and dated market reference

The base inputs and forecast are unchanged from Lab 10. The latest available **market-closed** TSLA reference requested for this lab is **$357.45 on September 28, 2026, at 4:00 p.m. EDT** (S5). It is a reference point, not an input to the forecast or a recommendation.

| Base driver | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Revenue growth | 6% | 10% | 12% | 12% | 10% |
| Gross margin | 18% | 20% | 22% | 24% | 26% |

Base visible outputs: 2030 operating profit (EBIT) = **$9,046.8**; 2030 **FCFE** = **$5,302.4**; value per share = **$6.96**. The annual accounting checks are $0.0 (within rounding) for 2026–2030.

## Revenue, cost, and profit drivers

**Definitions.** A *revenue driver* is the operational factor that changes sales dollars, such as unit volume, price, product mix, or a new revenue stream. A *cost driver* is the operational factor that changes cost of revenue or operating expense, such as units produced, battery/material inputs, labor, logistics, capacity utilization, and warranty. A *profit driver* is a factor that changes gross profit, operating profit, or free cash flow after both revenue and costs are considered.

Tesla’s revenue is automotive (sales, regulatory credits, and leasing), energy generation and storage, and services and other. In FY2025, automotive revenue was **$69,526** of total revenue of **$94,827** (73.3%), compared with energy generation/storage at $12,771 and services/other at $12,530 (S1, p. 50). **The top revenue driver is automotive sales revenue—vehicle deliveries (volume) multiplied by average selling price/mix, including the mix of models and geographies.** It dominates because automotive is the largest revenue stream; pricing, product mix, production/delivery capacity, financing availability, and demand all transmit through it.

The top cost driver is automotive cost of revenue: $57,165 of $77,733 total cost of revenues in FY2025 (73.5%; S1, p. 50). Its main operational levers are battery/raw-material and component cost, manufacturing labor/overhead, logistics, warranty/recall cost, and factory utilization. The principal profit driver is gross margin: it converts every revenue dollar into gross profit before R&D and SG&A. In this model, operating profit is then reduced by R&D, SG&A, and depreciation; FCFE is further reduced by capex and working-capital investment. Tesla’s expected 2026 capex above $20bn makes reinvestment a separate near-term cash-flow driver (S3).

## Locked changed-input record

**Recorded September 29, 2026, before sensitivity runs.**

| Driver | Locked change and units | Range rationale | Prediction |
|---|---|---|---|
| Revenue growth | Base 6%, 10%, 12%, 12%, 10%; low is 2 percentage points lower in every year; high is 2 percentage points higher in every year | **Judgment:** FY2025 revenue fell 2.9% after FY2024 was nearly flat, so the base is uncertain; ±2 points tests a reproducible, moderate alternative path rather than a percentage change. | Higher growth should raise 2030 EBIT, FCFE, and value/share, but the effect may be moderated by capex and working capital. |
| Gross margin | Base 18%, 20%, 22%, 24%, 26%; low/high are −/+2 percentage points in every year | **History + judgment:** FY2023–2025 gross margin was 18.2%, 17.9%, and 18.0% (S1). The base recovery is judgment; ±2 points tests the uncertainty around cost/mix improvement. | Higher margin should have the larger effect because it directly changes gross profit on all revenue and flows into EBIT and FCFE. |

Only one independent input is changed in each run. All other inputs reset to the separate `BASE` copy before recalculation. Percentage-point shifts are not treated as percent changes.

## One-at-a-time sensitivity results

All results are from a complete rerun of the linked model. The output is final-year 2030 operating profit (EBIT), 2030 **FCFE**, and value per share. “Change” is scenario minus base. Every scenario’s annual accounting checks passed (absolute check less than $0.01 million).

### A. Revenue-growth path

| Case | Actual growth input: 2026–2030 | 2030 EBIT | Change | 2030 FCFE | Change | Value/share | Change |
|---|---|---:|---:|---:|---:|---:|---:|
| Low | 4%, 8%, 10%, 10%, 8% | $7,441.2 | $(1,605.5) | $4,430.7 | $(871.7) | $4.65 | $(2.31) |
| Base | 6%, 10%, 12%, 12%, 10% | $9,046.8 | $0.0 | $5,302.4 | $0.0 | $6.96 | $0.00 |
| High | 8%, 12%, 14%, 14%, 12% | $10,773.5 | $1,726.7 | $6,219.3 | $916.8 | $9.39 | $2.43 |
| **Output span** |  | **$3,332.3** |  | **$1,788.6** |  | **$4.74** |  |

Mechanism: changing the growth path changes revenue, which changes gross profit and R&D/SG&A dollars, then inventory and other operating balance changes. The result matched the predicted direction. The higher case’s FCFE increase is smaller than its EBIT increase because the model still funds working-capital needs and scheduled capex.

### B. Gross-margin path

| Case | Actual margin input: 2026–2030 | 2030 EBIT | Change | 2030 FCFE | Change | Value/share | Change |
|---|---|---:|---:|---:|---:|---:|---:|
| Low | 16%, 18%, 20%, 22%, 24% | $6,758.3 | $(2,288.5) | $3,438.4 | $(1,864.0) | $0.89 | $(6.07) |
| Base | 18%, 20%, 22%, 24%, 26% | $9,046.8 | $0.0 | $5,302.4 | $0.0 | $6.96 | $0.00 |
| High | 20%, 22%, 24%, 26%, 28% | $11,335.3 | $2,288.5 | $7,156.8 | $1,854.4 | $12.93 | $5.97 |
| **Output span** |  | **$4,577.0** |  | **$3,718.3** |  | **$12.04** |  |

Mechanism: gross margin changes cost of revenue at a given revenue level. That change enters gross profit immediately, then EBIT, taxes, FCFE, and terminal value. The result matched the prediction: gross margin has the larger span across all three outputs.

## Verification and interpretation

The restored base was rerun after all scenarios and exactly matched the original base: $9,046.8 EBIT, $5,302.4 FCFE, and $6.96/share. All annual balance checks pass in every usable run. The script raises an error instead of ranking any run if a balance check fails.

Over **these stated ranges**, gross margin is the main driver: its EBIT span ($4,577.0), FCFE span ($3,718.3), and value/share span ($12.04) each exceed revenue growth’s respective spans ($3,332.3, $1,788.6, and $4.74). This does not mean margin is universally more important than revenue: rankings depend on the chosen ranges, and these are equal ±2 percentage-point paths. A sensitivity table is not a forecast probability because it does not assign probabilities to cases, capture correlations (for example, growth may require price cuts), or include all possible outcomes.

The sensitivity does not change the model’s valuation conclusion: even the high-margin case ($12.93/share) remains far below the September 28 market close. My research priority is therefore evidence on durable margin expansion and cash conversion from Tesla’s AI/autonomy, energy, and manufacturing investments—not a minor adjustment to the assumed revenue path.

## Partner exchange notes

**Exchange 1 — prediction and range check.** My partner asked whether the ±2 percentage-point growth change was a percent change; I clarified that it is a percentage-point shift in each annual growth rate, and they confirmed gross margin and revenue growth are independent inputs. I explained that automotive deliveries and average selling price/mix are Tesla’s top revenue mechanism because automotive was 73.3% of FY2025 revenue.

**Exchange 2 — result check.** I showed my partner the low gross-margin case and the base. They recomputed the FCFE change as $3,438.4 − $5,302.4 = **$(1,864.0)** and verified that the revenue-growth path was left at base. I traced the change from cost of revenue to gross profit, EBIT, FCFE, and terminal value.

**Exchange 3 — ranking limitation.** My partner asked whether the margin ranking was partly caused by my chosen ranges. My answer was yes: it is the larger driver *over these ranges*, not proof of universal importance. I checked my partner’s analysis by confirming that their selected independent input changed alone, their change-from-base arithmetic recomputed, and their conclusion distinguished span from probability.

### Partner comparison

My partner and I compared mechanisms rather than raw dollar spans because our companies and input ranges are not directly comparable. For Tesla, gross margin was the main driver over the tested ranges because it changes cost of revenue and therefore gross profit, EBIT, FCFE, and terminal value across the full revenue base. I asked my partner whether their ranking could instead be driven by the width of their chosen range; we agreed that a sensitivity ranking is conditional on the stated ranges and is not a probability forecast.

## Learning check

1. **One-at-a-time sensitivity** reruns the full linked model while changing one independent input and resetting all others to base. It isolates the modeled effect of that input. The chosen range affects the ranking because a wider range can mechanically create a larger output span.
2. A sensitivity table is not a probability forecast: it shows conditional results for selected inputs, but does not estimate likelihoods or relationships among drivers.

## Submission checklist

- [x] Two independent TSLA operating drivers, with lower/base/higher paths, units, years, and sourced/judgment range reasons.
- [x] Locked pre-run prediction, visible lower/base/higher FCFE results, signed changes, spans, and statement mechanism.
- [x] Accounting checks for each run and passing restored-base check.
- [x] Revenue, cost, and profit drivers defined; top Tesla revenue driver identified.
- [x] Dated market-close reference, source register with sections/pages, partner exchanges, and learning reflection.
