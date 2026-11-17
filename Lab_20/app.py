"""Project 2 readiness app. Run: streamlit run app.py"""

from pathlib import Path
import streamlit as st
from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict

ROOT = Path(__file__).resolve().parent
sleeves, correlations = load_estimates(ROOT / "data" / "prices_through_2026-10-19.csv")

st.set_page_config(page_title="Meridian Portfolio Decision", layout="wide")
st.title("Meridian Portfolio Decision")
st.caption("Educational analysis only, not investment advice. AI (Codex) assisted with code and documentation; analysis and decision are the student's.")
st.write("Mandate: 6.5% estimated annual return, at least 3% in BIL/IEF reserve assets, long-only 5% increments. The calendar-year loss rule is not operationalized until the CIO specifies its measure and breach action.")

objective = st.sidebar.number_input("Annual return objective (%)", 0.0, 25.0, 6.5, .1) / 100
reserve = st.sidebar.number_input("Reserve minimum (%)", 0.0, 100.0, 3.0, 1.0) / 100
portfolio_cases = [("Equal weight", evaluate(equal_weight(sleeves), sleeves, correlations)),
                   ("60/40 VTI/LQD benchmark", evaluate(benchmark(sleeves), sleeves, correlations)),
                   ("Constrained portfolio", optimize(sleeves, correlations, objective, reserve))]

columns = st.columns(3)
for column, (name, result) in zip(columns, portfolio_cases):
    with column:
        st.subheader(name)
        if result is None:
            st.error("FAIL — no feasible 5%-grid mix")
        else:
            st.dataframe({"Weight": {ticker: f"{weight:.0%}" for ticker, weight in result["weights"].items()}}, use_container_width=True)
            st.metric("Estimated annual return", f"{result['return']:.2%}")
            st.metric("Estimated volatility", f"{result['volatility']:.2%}")
            st.metric("Reserve weight", f"{result['reserve']:.0%}")
            st.write(verdict(result, objective, reserve))

st.subheader("Point-in-time signal")
st.write("LLY close, 2026-11-16: **$1,431.67**. This is a comparison signal, preserved with source evidence; it does not enter the portfolio optimizer.")
st.subheader("Committee decision")
st.write("**Pilot, not adopt.** Reverse this only after the CIO defines the calendar-year-loss rule and the process remains feasible under the documented stress and point-in-time data review.")
