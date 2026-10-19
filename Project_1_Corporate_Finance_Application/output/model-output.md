# LLY Integrated Model — Executed Output

All dollars are USD millions except per-share values. Run date and source cutoff are stated in README.md.

## Valuation range

| Case | WACC | Terminal growth | EV | Equity value | Value/share |
|---|---:|---:|---:|---:|---:|
| Low | 9.5% | 2.5% | $279,728 | $244,493 | $271.87 |
| Base | 8.5% | 3.0% | $608,464 | $573,229 | $637.42 |
| High | 8.0% | 3.0% | $886,003 | $850,768 | $946.03 |

Reference market close preserved from Lab 08: $1,124.21 (2026-09-09). Base-case terminal-value share of EV: 80.5%.

## Base-case five-year pro-forma

| Year | Revenue | EBIT | Net income | CFO | Capex | FCFF | Cash | Debt | Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026 | $77,423 | $38,934 | $29,617 | $30,493 | $10,065 | $21,958 | $20,292 | $42,503 | $48,748 |
| 2027 | $90,557 | $44,964 | $34,441 | $35,706 | $10,867 | $26,369 | $36,520 | $42,503 | $74,579 |
| 2028 | $103,535 | $50,763 | $39,080 | $40,858 | $11,389 | $30,999 | $56,219 | $42,503 | $103,889 |
| 2029 | $115,073 | $55,688 | $43,021 | $45,441 | $11,507 | $35,464 | $79,397 | $42,503 | $136,154 |
| 2030 | $123,903 | $59,141 | $45,782 | $48,949 | $11,151 | $39,328 | $105,750 | $42,503 | $170,491 |

## WACC / terminal-growth sensitivity ($/share)

| WACC \ g | 2.5% | 3.0% | 3.5% |
|---|---:|---:|---:|
| 8.0% | $649.36 | $707.80 | $779.23 |
| 8.5% | $589.60 | $637.42 | $694.79 |
| 9.0% | $539.08 | $578.80 | $625.74 |

## Market-implied diagnostic

5.52% terminal growth required to equal $1,124.21

## Validation

- PASS base-year balance sheet: assets - liabilities - equity = 0.0
- PASS 2026: balance sheet
- PASS 2026: cash-flow-to-cash tie
- PASS 2027: balance sheet
- PASS 2027: cash-flow-to-cash tie
- PASS 2028: balance sheet
- PASS 2028: cash-flow-to-cash tie
- PASS 2029: balance sheet
- PASS 2029: cash-flow-to-cash tie
- PASS 2030: balance sheet
- PASS 2030: cash-flow-to-cash tie
- PASS DCF monotonicity: +100bp WACC lowers value
- PASS DCF monotonicity: +50bp terminal growth raises value
- PASS enterprise-to-equity bridge

## Required interpretation

The model holds debt at its FY2025 level and assumes distributions equal 25% of forecast net income; cash is the residual balance that makes the three statements articulate. These are explicit model conventions, not management forecasts. The DCF uses FY2025 cash and debt for the enterprise-to-equity bridge despite the later comparison-price date, so the range must be read with the staleness qualification in the memo.