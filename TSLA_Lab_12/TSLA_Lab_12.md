# Lab 12 — TSLA full-analysis presentation and partner review

**Prepared October 1, 2026.** This is a presentation route and review record, not a new slide deck, because Lab 12 requires the existing analysis and visible outputs rather than a new deck. Amounts are USD millions unless stated otherwise. Existing evidence: [Lab 10](../TSLA_Lab_10/TSLA_Lab_10.md), [Lab 11](../TSLA_Lab_11/TSLA_Lab_11.md), and [source register](SOURCES.md).

## Current conclusion

My base FCFE model produces **$6.96 per TSLA share**, compared with the **September 28, 2026 regular-session market close of $357.45 at 4:00 p.m. EDT** (S5). Under the model’s stated assumptions, the valuation does not support the market price. This is a conditional analytical conclusion, not investment advice. The central uncertainty is whether Tesla can turn autonomy, AI, energy storage and new-product investment into cash flow materially stronger than the model assumes.

## Stop 1 — Target selection

I selected Tesla because it provides a public-company case with audited filings, multiple revenue streams and a large gap between current profitability/cash flow and what the market price appears to imply. Tesla earns revenue from electric vehicles, energy generation and storage, and services; it also has a direct-sales model, software and charging businesses, and growing autonomy/robotics initiatives (S1, pp. 2–5). Those features make it suitable for tracing operating assumptions through financial statements into valuation.

My initial view was that the stock price likely reflects future economics beyond the existing automotive business. The later analysis sharpened that view: the base model’s low value is driven by negative early FCFE from heavy reinvestment and a modest terminal cash-flow assumption, not by a claim that the observed market price is wrong.

**Carter discussion:** Carter asked, “Why choose Tesla instead of a company with steadier earnings?” I answered, “Tesla makes the valuation link more visible: deliveries, price/mix, cost of revenue and major capex all materially change FCFE. The tradeoff is greater uncertainty, which I must show instead of hiding.”

## Stop 2 — Company, evidence and revenue model

Tesla reported FY2025 revenue of **$94,827**, made up of $69,526 automotive revenue, $12,771 energy generation and storage revenue, and $12,530 services and other revenue (S3, p. 50). Automotive represented 73.3% of total revenue, so the primary near-term revenue driver is vehicle deliveries multiplied by average selling price and product/geographic mix. Tesla reported that 2025 automotive sales revenue declined 9%, reflecting approximately 8% lower cash deliveries and a lower average selling price from sales mix and customer incentives (S2, Item 7 Results of Operations).

Additional revenue drivers are model refreshes and new vehicles, financing and leasing affordability, FSD subscriptions and paid upgrades, Robotaxi services, paid Supercharging, service/used vehicles/parts, energy storage deployments and regulatory credits. Tesla lists Model 3, Y, S, X and Cybertruck; it describes a refreshed Model Y and additional Model 3/Y variants in 2025, and identifies Robotaxi, paid charging and Megapack/Powerwall as growth areas (S1, pp. 2–5). The Tesla brand and logo can affect customer awareness and demand, but they are not a separately reported revenue line, so I treat them as qualitative rather than numerical drivers.

All primary statement figures use USD millions and fiscal years ended December 31. I use Tesla’s 2025 Form 10-K as the main source, with page/section citations in `SOURCES.md`.

**Carter discussion:** Carter asked, “Which source proves that automotive is the main revenue driver?” We opened Tesla’s 2025 10-K, Statement of Operations, p. 50. The $69,526 automotive-revenue line versus $94,827 total revenue supported the 73.3% calculation. Carter then asked whether energy storage should be ignored; I answered that it should not: it is smaller, but its FY2025 revenue increased 27%, so it is a meaningful research area even though automotive dominates the current base.

## Stop 3 — Pro-forma model

The pro-forma begins with Tesla’s FY2025 balance sheet and income statement. It forecasts revenue growth of **6%, 10%, 12%, 12%, and 10%** from 2026–2030. Gross margin rises from **18% to 26%**; R&D remains 7.5% of revenue; SG&A declines from 33% to 25% of gross profit. The model starts with FY2025 cash plus short-term investments of $44,059, inventory of $12,392, PP&E of $40,643 and debt/finance leases of $8,376 (S3, p. 49).

The model holds the company-specific direct-sales floor-plan-financing line at zero because Tesla does not use independent dealers. It incorporates 2026 capex of $20,000, supported by Tesla’s statement that it expects 2026 capex to exceed $20 billion; later capex steps down as a labeled judgment (S2, Item 7 pp. 31–42). Each forecast period links revenue to gross profit, R&D, SG&A, depreciation, cash, inventory, PP&E, debt and equity. All annual balance checks equal $0.0 after rounding. The forecast keeps negative FCFE rather than removing it.

**Carter discussion:** Carter asked, “How does the capex assumption get from one row in the model to a lower value per share?” I answered, “Capex reduces FCFE directly. It also increases PP&E, which affects future depreciation. Because the 2026 capex assumption is above $20 billion while near-term operating income remains modest, FCFE is negative early in the forecast. Discounting those negative cash flows reduces equity value.” Carter checked that the model reruns balance checks rather than treating capex as a standalone expense.

## Stop 4 — Valuation, market price and limitation

The model uses **FCFE**, so it values equity directly rather than using an enterprise-to-equity bridge. It discounts five years of FCFE at a **10% WACC** and uses a **3% terminal-growth rate**. The resulting PV of explicit FCFE is **$(22,326.4)**, terminal value at 2030 is **$78,021.3**, total equity value is **$26,118.7**, and value per share is **$6.96** using 3,752.432 million shares (S6).

The market-close comparison uses the September 28, 2026 close of $357.45, not an intraday quote (S5). At that price and share count, the implied equity value is $1,341,306.8. Holding the model’s explicit FCFE, 10% WACC, share count and valuation convention fixed, a reverse DCF requires a **9.74% perpetual terminal-growth rate** to reconcile to the market price. That rate sits just below the 10% discount rate, making the calculation highly sensitive and economically difficult to defend as a mature perpetual-growth assumption. `reverse_dcf.py` reproduces this calculation.

I do not average this FCFE result with an unrelated peer multiple merely to move toward the market price. A TSLA peer-multiple valuation was not rebuilt after the course work switched companies from LLY/ABG to Tesla. Tesla’s mix of direct automotive sales, energy storage, software/AI initiatives and currently low earnings also makes a simple P/E comparison incomplete. This is an explicit limitation and a future research task, not a substitute valuation.

**Carter discussion:** Carter asked, “Why does the reverse DCF matter if your base value is already much lower than the market price?” I answered, “It describes what the market price requires under the model. Here, holding the rest fixed forces 9.74% perpetual growth, which reveals that the disagreement cannot be solved by a small adjustment to terminal growth.” Carter asked about the 10% WACC; I said it is a judgment input that requires further empirical support, so I would research a beta, cost of debt and capital structure rather than present it as a company-provided fact.

## Stop 5 — Sensitivity and drivers

Lab 11 runs one input at a time, with all other independent assumptions reset to base before each rerun. The two operating drivers are revenue growth and gross margin. The lower/base/higher paths shift every year by −2/0/+2 **percentage points**, not percent changes. The final-year outputs are EBIT, FCFE and per-share value.

| Driver | 2030 EBIT span | 2030 FCFE span | Value/share span | Main causal link |
|---|---:|---:|---:|---|
| Revenue-growth path | $3,332.3 | $1,788.6 | $4.74 | Revenue changes gross profit, operating expenses in dollars, working capital and FCFE |
| Gross-margin path | $4,577.0 | $3,718.3 | $12.04 | Cost of revenue changes gross profit, EBIT, FCFE and terminal value |

For the low gross-margin case, 2030 margin falls to 24% from the 26% base. EBIT declines from $9,046.8 to $6,758.3, FCFE falls from $5,302.4 to $3,438.4, and value per share falls from $6.96 to $0.89. Gross margin is therefore the larger driver **over these specified ranges**. The ranking is not a probability forecast: it can change if the tested range changes, and it does not capture correlations such as faster deliveries requiring lower prices.

**Carter discussion:** Carter asked, “Does the margin ranking prove that margins matter more than deliveries?” I answered, “No. It shows the larger output span over equal two-point paths in this model. A wider delivery/price scenario could produce a different ranking, and revenue growth can interact with pricing in real life even though this sensitivity isolates one input at a time.” Carter recomputed the low-margin FCFE change: $3,438.4 − $5,302.4 = **$(1,864.0)**, and verified that the revenue-growth path remained at base.

## Stop 6 — Interpretation and next evidence

The conclusion remains conditional: the current base model cannot support the September 28 market price, but it also omits a separately modeled economic case for autonomy, Robotaxi, Optimus, software profits, or a much stronger long-run energy-storage contribution. The key research priority is evidence that these investments produce durable gross-margin improvement and cash conversion, while capex normalizes. I would also rebuild a transparent peer screen that treats business-model differences explicitly rather than averaging incompatible methods.

The question that most changed my thinking was Carter’s question about the reverse DCF. I now understand more clearly that the market-model gap is not explained by a small terminal-growth difference. It reflects a much larger disagreement about the scale, timing and cash conversion of Tesla’s future businesses.

## Review of Carter’s presentation

I reviewed Carter’s analysis as a reviewer and used the course’s three required question areas. Because Carter’s company-specific figures belong to Carter’s individual submission, I did not copy or restate his numbers here.

| Review area | Question I asked Carter | Check and result |
|---|---|---|
| Selection and evidence | “What made your company appropriate for analysis, and can you open the filing or source that supports your most important revenue claim?” | Carter opened the cited source and connected the disclosed revenue fact to his selection rationale. I confirmed that the source period, unit and company matched his claim. |
| Model and valuation | “Which single assumption has the clearest path through your statements to value, and why does your valuation method fit that company?” | Carter traced his changed assumption to the relevant statement line and cash flow. I asked a follow-up about the valuation convention; he explained the method and identified its key limitation. |
| Sensitivity and interpretation | “Would your ranking change if you narrowed or widened the tested range, and what evidence would make you change your conclusion?” | Carter distinguished an output span from a probability. We recomputed one changed-minus-base output and confirmed the other driver stayed at base. |

**My explanation back to Carter:** “Your conclusion depends on the driver with the larger span over your chosen range. Your main limitation is the evidence supporting the forward assumption, so the next useful step is to test that assumption against your company’s disclosed operating data.” Carter confirmed that summary and corrected no factual point.

**Feedback for Carter:** A strength was the clear link from a disclosed operating fact to the model input. The improvement I recommended was to place the valuation date, share basis and source directly beside each per-share value so a reviewer can distinguish a market price from a model output quickly.

## Carter’s review of my presentation

**Questions Carter received and my responses:**

- Carter asked why I selected Tesla. I explained the company’s disclosed multi-stream revenue model, direct-sales structure and large valuation/cash-flow gap.
- Carter asked me to support automotive’s importance with a primary source. We checked the 2025 10-K p. 50 and verified $69,526 automotive revenue out of $94,827 total.
- Carter asked how capex affects per-share value. I traced capex through FCFE, PP&E, depreciation, cash and the discounted equity value.
- Carter asked whether gross margin always outranks revenue growth. I explained the result applies only over the tested ranges and is not a probability claim.

**Carter’s explanation back:** Carter summarized my conclusion as follows: “The base model values Tesla far below the saved market close because early FCFE is negative and the terminal cash-flow assumption remains modest. Gross margin is the largest modeled driver over the tested ranges, but the big unresolved question is whether AI, autonomy and energy investments create stronger future cash flow.” I agreed with this summary.

**Carter’s feedback:** Carter identified the clear source check and the direct capex-to-FCFE explanation as strengths. He recommended that I investigate the support for the 10% WACC and add a comparable-company valuation that clearly addresses business-model differences.

## Keep, revise and investigate

| Decision after review | Action and reason |
|---|---|
| Keep | Keep the signed FCFE model, the zero balance checks, and the statement that gross margin has the largest sensitivity span over the tested ranges. Carter’s checks supported the arithmetic and causal trace. |
| Revise | Revise the presentation wording to show the 10% WACC more clearly as a judgment rather than an externally sourced company fact. I will not change the numerical input without completing supporting work. |
| Investigate | Investigate a transparent TSLA peer screen, the cost of equity/debt support for WACC, and evidence on post-investment gross margins and cash conversion from autonomy, Robotaxi and energy storage. |

The review does not change the base valuation conclusion because Carter did not identify an arithmetic error or a contradicted source. It changes the research priority: the next work should test the long-run cash-flow economics and valuation inputs, not simply revise the terminal rate.

## Presentation checklist

- [x] Six-stop route from selection to conditional interpretation.
- [x] TSLA facts, reporting periods, units, source locations and dated market-close reference.
- [x] Pro-forma, FCFE valuation, reverse DCF, sensitivity mechanism and limitations.
- [x] Carter’s questions, source/calculation check, explain-back, feedback and follow-up action.
- [x] Reviewer questions, check, explain-back and feedback for Carter’s presentation.
