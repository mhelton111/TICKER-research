# Lab 19 — Legend Panel (course instructions archive)

Source: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md  
Accessed: 2026-11-05

## Requirements archive

Extend the Lab 18 SEC-EDGAR 10-K fact workflow by adding `Liabilities`, `AssetsCurrent`, and `LiabilitiesCurrent`, calculating current ratio and liabilities ÷ equity, and adding two skills:

- Graham: current ratio ≥2.0 latest year; net income positive each year; net income grew from first to last.
- Burry: operating cash flow ≥ net income every year; liabilities ≤2× equity latest year.

Each investor requires a memo drawn only from printed numbers. The Streamlit app must show investor × check results, verdicts, three memos side by side, and unprinted-number flagging across all memos.

## Required COST validation

| Fiscal year end | 2022-08-28 | 2023-09-03 | 2024-09-01 | 2025-08-31 | 2026-08-30 |
|---|---:|---:|---:|---:|---:|
| Current ratio | 1.02 | 1.07 | 0.97 | 1.03 | 1.06 |
| Liabilities ÷ equity | 2.11 | 1.75 | 1.96 | 1.64 | 1.49 |

Expected checks: Buffett 3/3; Graham 2/3 because current ratio fails at 1.06; Burry 2/2. Temporarily lower Graham’s threshold to 1.0 and COST should pass Graham’s current-ratio check.

Run a separate company panel, preserve all gaps as `not found` / `not known`, articulate a bull and bear case from the panel, and make a conditional decision about using the screen for Project 2.
