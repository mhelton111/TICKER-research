# Lab 14 Portfolio Baselines

## Question

What does each simple portfolio earn and risk, and does it meet the Meridian mandate?

The portfolio engine uses the course-authored return, volatility, and correlation inputs. These are training values, not market forecasts. The expected-return objective is 6.5%, calculated as the labelled CPI estimate of 2.5% plus 4.0%.

## Results

| Portfolio | Bills | 10-year | IG bonds | Equity | Expected return | Volatility | Reserve-eligible | Meets 6.5% return objective? | Meridian mandate verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Benchmark | 0.0% | 0.0% | 40.0% | 60.0% | 6.80% | 10.46% | 0.0% | Yes | Fails reserve rule |
| Equal weight | 25.0% | 25.0% | 25.0% | 25.0% | 5.20% | 5.21% | 50.0% | No | Passes checkable Lab 13 rules, but misses return objective |
| Inverse volatility | 84.3% | 6.0% | 7.0% | 2.6% | 3.77% | 1.05% | 90.3% | No | Passes checkable Lab 13 rules, but misses return objective |

The benchmark is the only baseline that reaches the 6.5% expected-return objective, but Candidate E in `mandate.py` fails the mandated 3.0% reserve requirement because it has 0.0% in cash or daily-liquid government securities. Equal weight and inverse volatility meet the reserve rule but miss the return objective. The mandate checker cannot test the calendar-year loss statement because the CIO did not define a measure or breach rule.

## Method

The engine first validates that every correlation is between -1 and 1 and that the table is symmetric. It then builds each covariance cell as:

`covariance(i,j) = correlation(i,j) x volatility(i) x volatility(j)`

Portfolio variance is the double sum of `weight(i) x weight(j) x covariance(i,j)` across all sleeve pairs. Portfolio volatility is the square root of that variance. Keeping the cross terms is essential: leaving out the correlation terms would understate the benchmark volatility.

For the benchmark, the calculation is:

`sqrt((0.40 x 0.06)^2 + (0.60 x 0.16)^2 + 2 x 0.40 x 0.60 x 0.25 x 0.06 x 0.16) = 10.46%`

## Required Validation Checks

1. The normal run reproduces the known answers: benchmark 6.80% return and 10.46% volatility; equal weight 5.20% and 5.21%; inverse volatility 3.77% and 1.05%.
2. Changing both IG-bond/equity correlation cells from 0.25 to 0.50 raises benchmark volatility to 11.00%; changing them back restores the normal result.
3. Setting one IG-bond/equity correlation cell to 1.30 makes `portfolio.py` stop with a clear out-of-range correlation message.
4. Candidate E is the Lab 14 benchmark (40% IG bonds, 60% equity) in `mandate.py`. It fails one checkable mandate rule: reserve-eligible weight is 0.0%, below the 3.0% required minimum.

## Partner Q and A

**Q: Why can two risky assets together be less risky than either asset alone?**

**A:** A portfolio includes the relationship between the assets, not just each asset's stand-alone volatility. When correlation is below +1, the assets do not move exactly together, so the covariance cross term reduces the total variance. The 40% IG-bond/60% equity benchmark is 10.46% volatile, below the 16.0% equity volatility, even though both sleeves are risky.

**Q: Which code block turns the inputs into portfolio volatility?**

**A:** `covariance_matrix()` calculates correlation times the two sleeve volatilities. `portfolio_variance()` sums every weighted covariance term, including cross terms in both directions. `portfolio_volatility()` takes the square root. The weights must remain decimals in these functions; percentages are only used for display.

**Q: Why does inverse volatility allocate so much to Treasury bills?**

**A:** Its rule assigns each sleeve a preliminary weight equal to one divided by volatility. Bills have 0.5% volatility, far lower than the other sleeves, so their inverse-volatility score dominates when the scores are scaled to total 100%.

**Q: Which baseline should the CIO see first?**

**A:** The benchmark should be shown first because it is the stated reference portfolio and is the only baseline that reaches the 6.5% expected-return objective. It must be shown beside the mandate result: it violates the reserve requirement, so it is a return/risk reference rather than a permissible Meridian reserve portfolio.

## Thursday Fund Universe

My main company focus is Eli Lilly and Company (`LLY`). LLY is included in `prices.csv` as a company-focus comparison series, using its adjusted close as of the October 19, 2026 market close. It is not assigned a portfolio sleeve because the Thursday preparation specifically asks for funds. The fund universe below supplies the required investable roles; LLY can be evaluated separately against the diversified equity funds.

| Ticker | Fund name | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve sleeve |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government-bond sleeve |
| LQD | iShares iBoxx USD Investment Grade Corporate Bond ETF | Investment-grade fixed-income sleeve |
| VTI | Vanguard Total Stock Market ETF | Broad U.S. equity sleeve |
| XLV | Health Care Select Sector SPDR Fund | Healthcare equity comparison sleeve relevant to the LLY focus |

`prices.csv` contains five years of monthly Yahoo Finance adjusted-close data, ordered oldest month first, for the five funds and LLY. Yahoo Finance historical data was downloaded October 20, 2026. Adjusted close is used because it incorporates distributions; these data are for the course exercise, not a recommendation.

## Files and Commands

- `portfolio.py` - standard-library portfolio risk engine. Run: `python portfolio.py`
- `mandate.py` - Lab 13 checker with Candidate E. Run: `python mandate.py`
- `test_lab14.py` - automated known-answer and validation tests. Run: `python -m unittest -v test_lab14.py`
- `prices.csv` - five years of monthly adjusted-close data for the Thursday fund universe and LLY comparison series.
- `SOURCES.md` - course and Yahoo Finance source record.
- `lab-13-portfolio-mandate.md` and `lab-14-portfolio-baselines.md` - copied course instructions used for this work.

