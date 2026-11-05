---
name: graham-10k-edgar
description: Apply Benjamin Graham-style current-ratio and earnings-stability checks to five annual SEC 10-K fact rows. Use for Lab 19 investor-panel screening; do not add price-based valuation conclusions.
---

# Graham 10-K panel skill

Use the shared `legend_panel.py` script in this Lab_19 folder. It computes the current ratio from `AssetsCurrent ÷ LiabilitiesCurrent` for the latest year, net-income positivity for every year, and first-to-last net-income growth. Default current-ratio threshold is 2.0.

Return `not found` for missing XBRL facts and `not known` for any dependent check. The Graham memo may cite only printed numbers and should explain that a threshold is a screen design choice, not an intrinsic-value conclusion. Do not use price data.
