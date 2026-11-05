---
name: burry-10k-edgar
description: Apply Michael Burry-style cash-versus-earnings and balance-sheet checks to five annual SEC 10-K fact rows. Use for Lab 19 investor-panel screening; do not invent forensic conclusions beyond the printed facts.
---

# Burry 10-K panel skill

Use the shared `legend_panel.py` script in this Lab_19 folder. It checks whether operating cash flow is at least net income in every year and whether latest-year `Liabilities ÷ StockholdersEquity` is no more than 2.0.

Keep missing inputs as `not found` and dependent checks as `not known`. The Burry memo can frame skepticism, but it may cite only script-printed numbers and must not claim the screen proves or disproves accounting manipulation. Do not use price data.
