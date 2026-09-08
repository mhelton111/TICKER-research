# Lab 05 — Build and Validate an FCFF DCF

**Company for the next lab:** Eli Lilly and Company (LLY)  
**Lab date:** September 8, 2026

## Question

What is one share of a company worth on a five-year FCFF DCF, and what growth does the current share price imply?

This lab builds and validates the training model. It does not use LLY operating inputs; those will be researched for the next lab.

## Files and run command

- Model: `dcf.py`
- Run from this folder: `python dcf.py`

The model uses only Python's standard library and exposes the seven editable assumptions at the top of the file. Values are USD millions except the per-share result.

## Training inputs

| Input | Value |
|---|---:|
| Starting FCFF | 100.0 |
| Growth rates, Years 1–5 | 8%, 6%, 5%, 4%, 3% |
| WACC | 10% |
| Terminal growth | 3% |
| Non-operating cash | 50.0 |
| Debt | 300.0 |
| Diluted shares | 50.0 million |

## Validation

The baseline output matches the Lab 05 known-answer check to four decimal places:

| Output | Model result | Expected |
|---|---:|---:|
| FCFF Year 1 | 108.0000 | 108.0000 |
| FCFF Year 2 | 114.4800 | 114.4800 |
| FCFF Year 3 | 120.2040 | 120.2040 |
| FCFF Year 4 | 125.0122 | 125.0122 |
| FCFF Year 5 | 128.7625 | 128.7625 |
| PV of explicit FCFF | 448.4408 | 448.4408 |
| Terminal value, Year 5 | 1,894.6486 | 1,894.6486 |
| PV of terminal value | 1,176.4277 | 1,176.4277 |
| Enterprise value | 1,624.8685 | 1,624.8685 |
| Equity value | 1,374.8685 | 1,374.8685 |
| Value per diluted share | 27.4974 | 27.4974 |
| PV of TV / enterprise value | 0.7240 | 0.7240 |

For the required proof check, raising WACC from 10% to 11% changes value per diluted share to about $23.41. The file has been returned to the required 10% baseline afterward.

## Logic reflection

The model compounds the starting FCFF separately by each of the five forecast growth rates, discounts each year-end cash flow to today, and adds their present values. It then calculates a Gordon-growth terminal value at the end of Year 5, discounts that terminal value five years, bridges enterprise value to equity value with cash and debt, and divides by diluted shares.

The terminal value is discounted five years because it is measured at the end of Year 5, after the fifth explicit FCFF. Discounting it six years would treat it as if it were dated at the end of Year 6 and would understate its present value.

A higher WACC lowers value because it increases the discount applied to both the explicit FCFF and terminal value; it also increases the denominator in the Gordon-growth formula. In this training case, moving WACC from 10% to 11% reduces value per share from $27.50 to about $23.41.

## Reversed DCF

A reversed DCF starts with the market price rather than starting with an estimated intrinsic value. It holds the other assumptions fixed and solves for the growth, margin, cash flow, or other operating assumptions needed for the DCF to equal that price. It is useful because it turns a price into a testable expectation: the analyst can ask whether the implied performance is plausible for the company.

## Lab source

[FIN 43900 Lab 05 — Build and Validate an FCFF DCF](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-05-dcf-build.md)

AI assistance: drafted with ChatGPT/Codex. The training inputs and required checks are from the Lab 05 instruction; the explanation and reflections are my own learning notes.
