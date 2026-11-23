# Lab 16 — Provenance Gate

> **Disclaimer:** This is an educational point-in-time-data exercise using a fictional course table. It is not investment research, investment advice, or a recommendation to buy, sell, or hold any security. The results illustrate data provenance and do not predict future performance.

## Decision question

**On 31 March 2026, what did the card-spend index actually say, and how much of the result visible later was not yet knowable?**

The course table is fictional. This submission therefore does not use LLY filings or a live FRED series: using them would answer a different question and would make the required known-answer check less reproducible.

## Method and reproducibility

Run from this folder:

```powershell
python asof.py
python -m unittest -v test_lab16.py
```

`asof.py` uses only the Python standard library and computes every result from the editable table at the top of the file. The filter applies the required rules in order:

1. Quarantine a row without a ticker.
2. Remove an exact duplicate.
3. Remove rows published after the decision date.
4. Within each ticker/month, keep the most recent publication that was available by the decision date.

Rule 4 is the provenance gate. It prevents a later revision from being treated as if it were available on the original decision date. The script separately prints a deliberately naive panel that ignores publication date, so the effect is visible rather than hidden.

## Verified row funnel

| Step | Rows removed | Why it matters |
|---|---|---|
| Quarantined: no ticker | 11 | An unkeyed record cannot be assigned to a company. |
| Exact duplicate | 7 | Prevents the same BBB observation from being counted twice. |
| Published after 31 March 2026 | 3, 8, 10 | These values did not exist in the decision-date information set. |
| Older vintage replaced by a revision | 2 | AAA's 25 March revision supersedes its 10 March February value. |
| Final as-of panel | 1, 4, 5, 6, 9, 12 | The complete point-in-time evidence set. |

## Results: knowable versus naive

| Ticker | As-of signal on 31 March | Naive signal | What the naive result improperly includes |
|---|---:|---:|---|
| AAA | +1.98% (February) | +5.83% (March) | A March observation published 10 April. |
| BBB | −1.02% (February) | −5.15% (March) | A March observation published 10 April. |
| CCC | +0.91% (February) | +1.82% (February, revised) | A February revision published 5 April. |

All values match the course's known answer. The most consequential row is **AAA row 3**: the naive calculation turns a modest, knowable February increase into a much stronger March increase that was unavailable until 10 April. A backtest using the naive column would claim a decision-maker saw information that arrived later. That is **look-ahead bias**.

## Why month measured is not publication date

The month measured answers, “When did the underlying activity occur?” The publication date answers, “When could a decision-maker have observed this estimate?” A revision adds a third time dimension: it may measure an old month but become available only later. A valid historical decision rule must use the version actually released by its decision date, not the newest version displayed today.

This is precisely the use case for ALFRED: it provides the vintage that was available on a historical date, whereas current FRED displays the latest release. For an interest-rate or macro series, the implementation would save the series identifier, observation date, vintage/release date, retrieval date, transformations, and the complete source extract with the analysis.

## Later-date check

Changing `DECISION_DATE` to `2026-04-15` makes every course publication available. The as-of signals then equal the naive signals ticker by ticker: AAA +5.83%, BBB −5.15%, and CCC +1.82%. This is the expected crossover and confirms that the difference on 31 March is an information-timing issue, not a formula difference. Restore the editable input to `2026-03-31` after the demonstration.

### Verification record (27 October 2026)

| Check | Result |
|---|---|
| `python asof.py` at 31 March 2026 | Funnel removed 11; 7; 3, 8, 10; and 2. The final panel was 1, 4, 5, 6, 9, and 12. Signals were AAA +1.98%, BBB −1.02%, and CCC +0.91%. |
| `python -m unittest -v test_lab16.py` | Passed: 3 tests, 0 failures. |
| Temporary decision date: 15 April 2026 | As-of and naive signals matched exactly: AAA +5.83% (March), BBB −5.15% (March), and CCC +1.82% (February). |
| Restored input | `DECISION_DATE` is restored to `2026-03-31` in `asof.py`. |

## Exchange walkthrough and reflection record

### Rule 4 code explanation

`latest_publication_per_month()` first groups the rows by the pair `(ticker, month)`. For each group, `max(..., key=published date)` selects the most recent publication. That selected row is added to the retained panel; all other rows in the same ticker/month group are recorded as older vintages. Crucially, the function is called only after the publication-date gate, so it selects the latest **available** vintage rather than the latest vintage visible today.

**Question:** Why is `max()` applied after filtering on `published <= decision_date` instead of before it?  
**Answer:** If `max()` ran first, it could select a later revision and discard the value that was actually available on the decision date. Filtering first makes the choice point-in-time valid.

### Swap-and-break check

The decision-date input was changed to 15 April 2026. The as-of panel then included the later March releases and CCC's later February revision, and its signals matched the naive comparison exactly. Returning the input to 31 March restored the information set and the original as-of results. This demonstrates that the gap between the two signal columns is caused by publication timing.

### Learn and reflect

**Look-ahead bias** occurs when an analysis uses information that was not available when its historical decision was supposedly made. In this table, event time is the month measured, publication time is the date of release, and a revision is a newer released estimate for an already measured month. AAA's naive +5.83% March signal looks stronger than the knowable +1.98% February signal because the March value was published ten days after the 31 March decision date.

The most important removal for the trading decision is the publication-date rule: it excludes AAA row 3, BBB row 8, and CCC row 10. A backtest built from the naive column would overstate what the strategy could have known and could falsely attribute performance to an unavailable March trend or later revision.

## Partner Q&A / discussion points

**Q: Why is AAA row 4 retained while row 2 is removed?**  
**A:** Both measure AAA in February, but row 4 was published later (25 March versus 10 March) and was still available by 31 March. It is the newest information actually knowable at the decision date.

**Q: Why not simply use the latest value on FRED today?**  
**A:** That can import revisions or releases that were unavailable historically. ALFRED is designed to retrieve the vintage available at a particular historical date; FRED's API also exposes real-time and vintage-date parameters.

**Q: Is the naive signal “wrong”?**  
**A:** It is not wrong as a description of the latest revised history. It is wrong only if represented as a signal one could have traded on 31 March 2026.

**Q: Which time stamp should a trading backtest use?**  
**A:** The timestamp at which the market could access the release, with an explicit execution assumption (for example, trade after release or next session). The observation month alone is insufficient.

**Q: What else should be recorded for real macro/interest-rate work?**  
**A:** Series ID, source, units, frequency, seasonal adjustment, observation period, vintage date, release time/time zone if relevant, retrieval date, transformation, and code/data file used.

## Submission contents

- `Lab_16_Submission.md` — completed analysis, validation, reflection, and partner Q&A.
- `asof.py` — standard-library point-in-time filter and printed audit trail.
- `test_lab16.py` — regression tests for the known answer and later-date crossover.
- `lab-16-provenance-gate.md` — saved course instructions used for the lab.
- `SOURCES.md` — source ledger and provenance notes.
