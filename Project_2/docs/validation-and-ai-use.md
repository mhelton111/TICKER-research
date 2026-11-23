# Validation and AI Use

Educational analysis only; not investment advice. AI tools assisted source organization, Python/Streamlit implementation, testing, and drafting. The student must verify sources, own the prediction and decision, and explain the calculation code.

Run `python -m unittest -v test_project2.py` and `python run_analysis.py`. The nine automated checks verify baseline failures, constrained-portfolio feasibility, the objective-stress direction, estimate/cost return effects, the reproducible shorter-window run, an explicit no-feasible-mix stop condition, invalid-correlation rejection, the Lab 14 course-known-answer benchmark, and the LLY DCF base reconciliation.

## Locked changed-input record

The immutable pre-run source is `docs/locked-changed-input-record.md` in local Git commit [`f2ff122bbb0961252e0c59adebc14d499bd8e5fb`](https://github.com/mhelton111/TICKER-research/commit/f2ff122bbb0961252e0c59adebc14d499bd8e5fb). This section reproduces that record so this required validation file is complete when attached to Brightspace. The student owns the prediction and must accurately describe its timing relative to any earlier exploratory runs.

**Student AI-off prediction:** I personally believe that raising the required return will push the portfolio toward higher-return, higher-volatility tickers and reduce its reserve allocation if a feasible mix remains. The same tradeoff can appear when estimated returns are reduced or implementation costs are added. I made this prediction before the official validation run.

| Input family | Old value | New value | Pre-run prediction |
|---|---|---|---|
| Estimates | Saved annualized return estimates | Each asset return reduced by 1.00 percentage point | Lower expected returns should require heavier weights in higher-return, higher-volatility tickers, or make the mandate infeasible. |
| Window | Full preserved monthly series through 2026-10-19 | Trailing 36 monthly returns from the same file | The selected weights and volatility may change materially because the sample is shorter; I expect the result to remain sensitive to the return estimates. |
| Costs | 0.00% annual implementation drag | 0.25% annual implementation drag | Lower net return should require heavier weights in higher-return, higher-volatility tickers, or make the mandate infeasible. |
| Constraints | 6.5% objective and 3% reserve | 7.5% objective and 10% reserve | A higher required return should shift weight toward higher-return, higher-volatility tickers; the tighter reserve requirement may partially limit that shift. |

**Commit evidence:** Official run command: `python -m unittest -v test_project2.py; python run_analysis.py`. Actual results appear below and in `output/model-output.md`.

| Input family | Actual result | Decision effect |
|---|---|---|
| Estimates: 1.00% annual return haircut | BIL 50% / VTI 35% / XLV 15%; 6.52% estimated return; 7.07% volatility | Feasible, but the higher-risk mix reinforces Pilot. |
| Window: trailing 36 monthly returns | BIL 85% / VTI 10% / XLV 5%; 6.57%; 1.69% | Allocation is window-sensitive; preserve the selected window and rerun before any adoption decision. |
| Costs: 0.25% annual implementation drag | BIL 60% / VTI 30% / XLV 10%; 6.57%; 5.77% | Feasible under the explicit cost proxy, but actual trading costs require holdings and execution assumptions. |
| Constraints: 7.5% objective and 10% reserve | BIL 50% / VTI 35% / XLV 15%; 7.52%; 7.07% | Feasible, but greater equity exposure and risk do not overcome the governance blocker. |

The process stops if a stress produces no feasible mix, a modeled rule fails, point-in-time timing cannot be defended, or the CIO does not define the loss measure, observation date, and breach response.

## Prediction reconciliation

| Input family | Student prediction before official run | Actual direction | Disposition and decision effect |
|---|---|---|---|
| Estimates haircut | More higher-return/higher-volatility exposure, or no feasible mix | VTI/XLV rose from 35% to 50%; estimated volatility rose from 5.27% to 7.07% | Direction confirmed; the mandate stayed feasible, but higher estimated risk supports Pilot rather than live adoption. |
| Shorter window | Weights and volatility could change materially | BIL rose from 65% to 85% and volatility fell to 1.69% | Direction confirmed; window dependence requires the chosen window and date boundary to be preserved. |
| Cost drag | More higher-return/higher-volatility exposure, or no feasible mix | XLV rose from 5% to 10%; BIL fell to 60%; the mandate stayed feasible | Direction broadly confirmed, but the change was not only VTI exposure. This is why the cost stress is a sensitivity, not a forecast. |
| Tighter return and reserve rules | Higher-return/higher-volatility exposure, partly limited by the reserve floor | VTI/XLV rose from 35% to 50% and volatility rose to 7.07% | Direction confirmed; the result remains Pilot because governance rules are still unresolved. |

## Student review of AI-assisted work

Material AI use: OpenAI Codex, a GPT-5-based coding assistant, was used during November 2026 for source organization, candidate Python/Streamlit implementation, test scaffolding, and draft documentation. I accepted code only after running the tests and reconciling results; I revised the decision language after forming and supplying my own views on liquidity, return credibility, LLY concentration, loss governance, and AI limitations. I did not treat AI as a source for investment conclusions or unsourced company facts.

AI helped accelerate the model, app, tests, and documentation. It did not replace judgment. I checked the arithmetic and model flow because an AI-produced calculation can appear polished while using an unsupported assumption, an incorrect data boundary, or a broken bridge between inputs and results. In particular, I verified that portfolio weights sum to 100%, that the app distinguishes a failed return rule from a failed reserve rule, and that the model returns no recommendation when no feasible mix exists.

I also distinguish public evidence from information the model cannot know. AI has an outside view of available numbers; it cannot validate nonpublic management context, future events, or whether an assumption is appropriate for this committee. Any credible public disclosure about governance, legal issues, or insider trading would require a fresh committee review rather than automatic reliance on the current output. This is why the decision remains a paper pilot and why the student, not AI, owns the recommendation.
