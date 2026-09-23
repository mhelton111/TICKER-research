# Lab 09 — Pro-Forma Build: the Engine and the Known Answer

**Training case:** Asbury Automotive Group (ABG)  
**Lab date:** September 23, 2026  
**Scope note:** Lab 09 is the course's ABG training case. The `LLY_Lab_09` folder name follows the existing workspace convention; no LLY operating or market inputs are mixed into this model.

## Question and three judgments

**Question:** What are five years of a company's statements worth, built from assumptions that can be defended, and how do we know the statements are right?

The three judgments carrying the valuation are the revenue-growth path, operating margins (gross margin and SG&A as a percentage of gross profit), and cost of equity/terminal growth. Cash is computed last because it is the balancing result of operating cash generation, investment, working-capital changes, scheduled financing, and the revolver rule—not an assumption that can be chosen independently.

## Assumptions and opening balance sheet

All amounts are USD millions except percentages and shares. These are the course-provided ABG training inputs, transcribed from Lab 09's **R — the assumption set** and **Opening balance sheet, FY2025** sections. No market data is used in this lab.

| Assumption | Value | Label / source locator |
|---|---:|---|
| Organic revenue growth | 1.8% annually | Judgment; Lab 09, R section |
| Gross margin | 17.05% | Judgment; Lab 09, R section |
| SG&A / gross profit, 2026-2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment; Lab 09, R section |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | FY2025 history; Lab 09, R section |
| Impairment, non-cash | 120 annually | Judgment; Lab 09, R section |
| Capital spending | 250 annually | Guidance; Lab 09, R section |
| Tax rate | 25.5% | Judgment; Lab 09, R section |
| Inventory days | 2,135.8 / (17,999.0 - 3,071.7) x 365 | FY2025 history; Lab 09, R section |
| Inventory loans / inventory | 2,027.0 / 2,135.8 | FY2025 history; Lab 09, R section |
| Other working capital | 0.8% of revenue change | Judgment; Lab 09, R section |
| Minimum cash / revolver limit / rate | 25 / 850 / 6% | History / judgment / judgment; Lab 09, R section |
| Debt repayment / share buyback | 150 / 150 annually | Judgment; Lab 09, R section |
| Interest: floor plan / term debt | 4.67% / 5.44% | History; Lab 09, R section |
| Cost of equity / terminal growth | 10% / 2.5% | Judgment; Lab 09, R section |
| Shares outstanding | 17.951349 million | Fact; ABG 10-Q, June 30, 2026; Lab 09, R section |

| FY2025 opening balance sheet | Value |
|---|---:|
| Revenue | 17,999.0 |
| Inventory | 2,135.8 |
| PP&E | 3,070.4 |
| Other assets | 6,371.6 |
| Cash | 40.4 |
| Floor plan | 2,027.0 |
| Term debt | 3,572.0 |
| Other liabilities | 2,127.5 |
| Equity | 3,891.7 |

## Engine and validation

Run `python proforma.py` from this folder. The standard-library-only script projects the income statement, balance sheet, and FCFE for 2026-2030. Each projected year calculates cash only after operating results and all non-cash balance-sheet lines. It draws the revolver only when cash would fall below $25.0 million, repays the revolver first when cash exceeds that minimum, asserts the balance sheet, and values equity from five FCFE plus the specified terminal value.

| Line | FY2026E | FY2030E | Known-answer check |
|---|---:|---:|---|
| Revenue | 18,323.0 | 19,678.3 | Match |
| Operating income | 844.2 | 971.4 | Match |
| Net income | 413.6 | 527.5 | Match |
| Free cash flow to equity | 211.4 | 342.3 | Match |
| Cash, year end | 101.8 | 719.8 | Match |
| Assets - liabilities - equity | 0.0 | 0.0 | Match |
| Value per share | $291.75 | $291.75 | Match |
| Share of value after 2030 | 79.8% | 79.8% | About 80%; match |

The valuation uses the handout's formula: present value of 2026-2030 FCFE plus terminal value of `(2030 FCFE + 2030 debt repayment) x (1 + terminal growth) / (cost of equity - terminal growth)`, discounted five years, divided by 17.951349 million shares.

## Break test and model checks

`assert_balanced` runs before valuation for every projected year and raises a named error if assets minus liabilities minus equity differs from zero or cash is below the minimum.

For the prescribed break test, set `CASH_OVERRIDES = {2026: 40.4}` at the top of `proforma.py`, run `python proforma.py`, and then undo the change. The model refuses the edited FY2026 cash with:

```text
ValueError: FY2026E is not balanced: assets - liabilities - equity = -61.4
```

The -61.4 is the FY2026 cash increase (101.8 minus the $40.4 opening cash) with the sign reversed. It reveals that a user overwrote the cash-flow result instead of allowing cash to reconcile the statements.

## Floor-plan learning and partner explanation

A floor plan is inventory financing: dealership lenders, including manufacturer-affiliated finance arms and banks, lend against vehicle inventory. It rises as inventory rises, so the model sets floor-plan debt as a ratio of projected inventory. Interest is calculated using the opening floor-plan balance because that balance is outstanding during the year. The FCFE bridge includes the change in floor plan because an increase in inventory financing supplies cash for inventory; treating it as unrelated debt would distort operating working-capital cash flow.

Removing floor-plan financing removes that offset to inventory investment, which is why cash falls to roughly negative $1.1 billion in the course video. The lesson is not that the debt disappears economically; it is that omitting a funding source while leaving the inventory need in place breaks the cash logic. Asbury's 2025 10-Q states that understanding the relationship between floor-plan notes payable and new-vehicle inventory is important for working capital and operating cash flow.

## Sources

- [Lab 09 — Pro-Forma Build: the Engine and the Known Answer](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-09-proforma-build.md), especially **R — the assumption set**, **I — build the engine**, **V — prove it on the known answer**, and **Floor plan — Learn on your own**.
- [Asbury 2025 Q1 Form 10-Q](https://asburyautomotivegroupinc.gcs-web.com/static-files/eaf2de2a-9054-4a1f-be47-902ccdc686c8), floor-plan notes payable discussion in the liquidity/working-capital discussion.

This is a course training exercise, not investment advice. AI assistance: drafted with Codex; all assumptions are the course-provided ABG training inputs.
