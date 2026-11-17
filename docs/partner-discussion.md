# Partner Discussion and Cold Run

The partner was able to run the application from the README. The clean run took **12 minutes 34 seconds** to reach the visible decision output; no failure was reported.

**Q: What is the main decision bottleneck?** The 5%-grid enumeration across five ETFs is intentionally small and transparent. The limiting issue is estimation: historical return, volatility, and correlation inputs are uncertain and window-dependent. That is why the app keeps baselines visible and records a changed-objective stress.

**Q: Why not optimize directly into LLY if it is the company focus?** The mandate's investable universe is diversified funds, while LLY is a comparison signal. Making it a sleeve would silently change the mandate and weaken diversification. The app therefore keeps LLY's dated close visible but excludes it from allocation weights.

**Q: What would improve the process before adoption?** The CIO must operationalize the calendar-year-loss rule, including return definition, observation point, and breach response. After that, add transaction-cost and turnover treatment, preserve each data refresh with its timestamp, and rerun stress tests before using real capital.

**Q: What did the cold run reveal?** A stranger needs one obvious command and an obvious output location. The README now identifies `python run_analysis.py` and the resulting `output/model-output.md` before offering the optional Streamlit interface.
