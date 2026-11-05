"""Streamlit app for Lab 19's three-investor SEC-EDGAR panel."""

import pandas as pd
import streamlit as st

from legend_panel import analyze, fmt


st.set_page_config(page_title="Legend Investor Panel", layout="wide")
st.title("Legend Investor Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
st.info("Buffett, Graham, and Burry read the same five annual 10-K fact rows. No price data are used.")

with st.sidebar:
    ticker = st.text_input("Ticker", value="LLY", max_chars=10).upper().strip()
    ratio_threshold = st.number_input("Graham current-ratio threshold", value=2.0, min_value=0.1, step=0.1)
    run = st.button("Run panel", type="primary")

if not run:
    st.info("Run LLY for the required single-company panel; run COST for the course known-answer validation.")
    st.stop()

try:
    analysis = analyze(ticker, graham_threshold=ratio_threshold)
except (RuntimeError, ValueError, KeyError) as error:
    st.error(str(error))
    st.stop()

rows = []
for investor, checks in analysis["checks"].items():
    for check, result in checks.items():
        rows.append({"Investor": investor, "Check": check, "Result": result})

table = pd.DataFrame(rows)
st.subheader(f"{analysis['ticker']} — {analysis['company']}")
st.subheader("Panel checks")
st.dataframe(table, hide_index=True, width="stretch")

metric_table = pd.DataFrame([{
    "Fiscal year end": row["fiscal_year_end"], "Net income ($m)": row["net_income"], "Operating cash flow ($m)": row["operating_cash_flow"],
    "Equity ($m)": row["equity"], "Current ratio": row["current_ratio"], "Liabilities / equity": row["liabilities_to_equity"],
    "Owner earnings ($m)": row["owner_earnings"],
} for row in analysis["rows"]])
st.subheader("Shared 10-K fact panel")
st.dataframe(metric_table.style.format(na_rep="not found", precision=2), hide_index=True, width="stretch")

chart_data = metric_table.melt(id_vars="Fiscal year end", value_vars=["Net income ($m)", "Operating cash flow ($m)", "Owner earnings ($m)"], var_name="Measure", value_name="USD millions").dropna()
st.line_chart(chart_data, x="Fiscal year end", y="USD millions", color="Measure", width="stretch")

st.subheader("Investor memos")
columns = st.columns(3)
for column, investor in zip(columns, ("Buffett", "Graham", "Burry")):
    with column:
        st.markdown(analysis["memos"][investor])
        flags = analysis["memo_flags"][investor]
        if flags:
            st.error("Unprinted numbers: " + ", ".join(flags))
        else:
            st.success("Memo-number check passed.")

st.caption(f"Graham threshold used: {fmt(ratio_threshold)}. A lower threshold changes the screen design, not the underlying 10-K facts.")
