# Lab 07 — Comparable-Company Policy and Implied Range

**Training case:** Asbury Automotive Group (ABG)  
**Lab date:** September 15, 2026  
**Scope note:** Lab 07 is the course's frozen Asbury P/E case. This folder uses the LLY naming convention only; it does not apply peer multiples to Eli Lilly. Lab 08 applies the method to the student's own company.

## Files and command

- Calculator: `comps.py`
- Run from this folder: `python comps.py`
- Standard library only; no packages or data fetching.

## P/E: what it measures

P/E equals price per share divided by annual diluted earnings per share (EPS). Price is the market value of one share; diluted EPS is the annual earnings attributed to each share after considering dilution. The multiple expresses how many dollars investors pay for each dollar of annual earnings.

P/E puts companies with different share counts on a comparable per-share earnings basis. It complements a DCF: a DCF values forecast cash flows, while P/E asks what the target would be worth if the market valued its earnings like selected peers' earnings.

P/E is useful only when earnings are positive, comparable, and reasonably representative of the businesses. Negative earnings make this positive-multiple comparison not meaningful. Unusual profits, depressed earnings, different growth, risk, business mix, capital structure, or accounting definitions can make a P/E comparison misleading. A lower P/E is therefore a question to investigate, not automatically a better investment.

## Peer policy before multiples

The policy is to use publicly traded franchised vehicle retailers with new and used vehicle sales plus meaningful service/parts operations, positive annual GAAP diluted EPS, and a consistent earnings definition. Scale, geography, and financing activities must be considered rather than hidden in an average.

| Candidate | Decision | Business evidence and qualification |
|---|---|---|
| AutoNation (AN) | **Use, with qualification** | It has similar vehicle-retail and service/parts activities. Its AutoNation Finance operation is a material difference to monitor. |
| Group 1 Automotive (GPI) | **Use, qualified** | It fits the franchised vehicle-retail core, but it operates in both the U.S. and U.K.; its 2024 acquisition of 54 Inchcape dealerships affects comparability. |

Neither peer is an exact copy of Asbury. Those qualifications are reasons to interpret the range cautiously, not reasons to choose a preferred answer after seeing the result.

## Frozen case inputs and sources

This is a retrospective comparison: December 31, 2024 closes are paired with FY2024 total GAAP diluted EPS reported subsequently. It is not a claim about what an investor knew on that date. The model uses total GAAP diluted EPS—not adjusted EPS—and keeps the price and EPS on the same stock-split basis.

| Company / role | Dec. 31, 2024 closing price | FY2024 total GAAP diluted EPS | Source locator |
|---|---:|---:|---|
| Asbury Automotive (ABG), target | $243.03 | $21.50 | [2025 proxy](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000092/abg-20250402.htm), outstanding equity awards footnote (2), search `243.03`; [Jan. 30, 2025 release](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000008/a2024q4ex991.htm), Full Year 2024 Results. |
| AutoNation (AN), peer | $169.84 | $16.92 | [2025 proxy](https://www.sec.gov/Archives/edgar/data/350698/000035069825000068/an-20250311.htm), outstanding equity awards footnote (1), printed p. 30; [Feb. 11, 2025 release](https://www.sec.gov/Archives/edgar/data/350698/000035069825000026/anearningsrelease123124ex9.htm), Full Year 2024 selected GAAP table. |
| Group 1 Automotive (GPI), qualified peer | $421.48 | $36.81 | [2025 proxy](https://www.sec.gov/Archives/edgar/data/1031203/000103120325000018/gpi-20250320.htm), Termination and Change in Control Tables, intro, printed p. 59; [Jan. 29, 2025 release](https://www.group1corp.com/2025-01-29-Group-1-Automotive-Reports-2024-Fourth-Quarter-Financial-Results-and-Record-Full-Year-Revenues-of-19-9-billion), annual consolidated statement of operations, total diluted EPS row. |

Business evidence and the frozen-case definitions: [course worked example](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md).

## Checked results and interpretation

`python comps.py` reproduces the course checks using unrounded calculation values:

| Check | Result |
|---|---:|
| AutoNation P/E | 10.037825x |
| Group 1 P/E | 11.450149x |
| Peer median P/E | 10.743987x |
| Asbury peer-implied range | $215.81-$246.18 |
| Asbury at peer median | $231.00 |
| Remove GPI: remaining AN reference estimate | $215.81 |
| Change from two-peer midpoint | -$15.18 |

Removing GPI lowers the result because GPI has the higher P/E. With only AN remaining, the output correctly calls the result a reference estimate rather than a range: one peer provides no cross-peer dispersion.

The observed Asbury price ($243.03) is inside the peer-implied range. That does not prove the share is fairly valued or attractive. The result depends on the selected peers, GAAP earnings convention, and their different business economics. P/E already compares equity per-share earnings, so cash or debt must not be subtracted from or added to a P/E-derived implied share price.

## Calculator safeguards

The calculator deduplicates peers by ticker, excludes the target, keeps full precision until display, and labels a P/E or implied valuation as not meaningful when price or diluted EPS is missing or nonpositive. One usable peer produces a reference estimate with no range; no usable peers produces no estimate. Every leave-one-out output shows the remaining median-implied price and unrounded dollar change from the full-peer estimate, or reports no estimate when no valid peer remains.

This is a course exercise, not investment advice. AI assistance: drafted with Codex; peer decisions and interpretation are presented for review.
