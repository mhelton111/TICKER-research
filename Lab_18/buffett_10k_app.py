"""Streamlit viewer for Lab 18's SEC-EDGAR 10-K Buffett analysis."""

from pathlib import Path

import pandas as pd
import streamlit as st

from edgar_buffett import analysis_for_ticker, unprinted_memo_numbers


st.set_page_config(page_title="Buffett 10-K Business Audit", layout="wide")
st.title("Buffett 10-K Business Audit")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
st.info("Numbers are computed from 10-K XBRL facts. The memo is limited to those outputs; no price data are used.")


with st.sidebar:
    ticker = st.text_input("Ticker", value="COST", max_chars=10).upper().strip()
    run = st.button("Run 10-K analysis", type="primary")

if not run:
    st.info("Enter a ticker and select **Run 10-K analysis**. COST is the required known-answer validation; JPM is the missing-capital-spending probe.")
    st.stop()

try:
    analysis = analysis_for_ticker(ticker)
except (RuntimeError, ValueError, KeyError) as error:
    st.error(str(error))
    st.stop()

frame = pd.DataFrame([
    {
        "Fiscal year end": row["fiscal_year_end"], "Revenue ($m)": row["revenue"], "Net income ($m)": row["net_income"],
        "Operating cash flow ($m)": row["operating_cash_flow"], "Capital spending ($m)": row["capital_spending"],
        "Equity ($m)": row["equity"], "ROE (%)": row["roe"], "Owner earnings ($m)": row["owner_earnings"],
        "Revenue tag": row["tags"]["revenue"], "Capex tag": row["tags"]["capital_spending"],
    } for row in analysis["rows"]
])

chart_frame = frame.melt(id_vars="Fiscal year end", value_vars=["Net income ($m)", "Owner earnings ($m)"], var_name="Measure", value_name="USD millions").dropna()
st.subheader(f"{analysis['ticker']} — {analysis['company']}")
st.line_chart(chart_frame, x="Fiscal year end", y="USD millions", color="Measure", width="stretch")
st.subheader("10-K facts and computed outputs")
st.dataframe(frame.style.format(na_rep="not found", precision=1), width="stretch", hide_index=True)

st.subheader("Buffett checks (computed by code)")
checks = pd.DataFrame({"Check": list(analysis["checks"]), "Result": list(analysis["checks"].values())})
st.dataframe(checks, width="stretch", hide_index=True)

memo_path = Path(f"{analysis['ticker']}_buffett_memo.md")
memo_path.write_text(analysis["memo"], encoding="utf-8")
st.subheader("Buffett-style business memo")
st.markdown(analysis["memo"])
flags = unprinted_memo_numbers(analysis["memo"], analysis["rows"], analysis["checks"])
if flags:
    st.error("Numbers in the memo not printed by the script: " + ", ".join(flags))
else:
    st.success("Memo-number check passed: every number in the memo appears in the script's printed inputs/checks.")
st.caption(f"Memo saved to {memo_path.resolve()}")
