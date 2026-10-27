# Lab 16 — Provenance Gate (course instructions archive)

Source: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md  
Accessed: 2026-10-27

## Question

On the day you would have traded, what did this data actually say — and how much of what you see now came later?

## Training table

Decision date: 31 March 2026. A row is knowable only if it was published on or before that day.

| Row | Ticker | Month measured | Published on | Index |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 2 | AAA | 2026-02 | 2026-03-10 | 104.0 |
| 3 | AAA | 2026-03 | 2026-04-10 | 109.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 7 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 8 | BBB | 2026-03 | 2026-04-10 | 92.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 10 | CCC | 2026-02 | 2026-04-05 | 112.0 |
| 11 |  | 2026-02 | 2026-03-10 | 99.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

Apply these rules in order: (1) quarantine a row with no ticker; (2) remove an exact duplicate; (3) remove a row published after the decision date; (4) when a ticker/month has two publications, keep the latest publication available by the decision date. The signal is the index percent change from the previous month to the latest knowable month. Also calculate a naive comparison that ignores publication date.

## Required known answer

| Funnel step | Rows removed |
|---|---|
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

| Ticker | As-of signal | Naive signal |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

With the decision date set to 2026-04-15, the as-of signals should equal the naive signals ticker by ticker.
