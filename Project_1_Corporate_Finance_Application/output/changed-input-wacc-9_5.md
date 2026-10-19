# Changed-input test - base WACC 9.5%

**Pre-run prediction:** Raising base WACC from 8.5% to 9.5% will reduce per-share value materially, while the Watch/Defer recommendation remains unchanged because the valuation should remain below the preserved market reference.

**Changed input:** `BASE_CASE.wacc`, 8.5% to 9.5%.

**Actual result:** Base enterprise value declined from $608,464m to $511,180m. Base equity value declined from $573,229m to $475,945m. Per-share value declined from $637.42 to $529.24, a decrease of $108.18 or 17.0%. Terminal value's share of enterprise value declined from 80.5% to 77.4%.

**Decision effect:** No change. The recommendation remains Watch/Defer because the changed-case value remains below the preserved $1,124.21 market reference.

**Prediction reconciliation:** Correct. Higher WACC reduced value as predicted and did not reverse the recommendation.

**Restore check:** `lly_model.py` was restored to 8.5% WACC and rerun. The visible final output is `output/model-output.md` and shows the restored $637.42 base per-share result.
