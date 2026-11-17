"""Meridian Reserve Decision Desk — Project 2 Streamlit application."""
from pathlib import Path
from dataclasses import replace
from datetime import datetime, timezone
import pandas as pd
import requests
import altair as alt
import streamlit as st
from portfolio import benchmark, equal_weight, evaluate, load_estimates, optimize, verdict
from lly_dcf import BASE_CASE, build, valuation

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "prices_through_2026-10-19.csv"
st.set_page_config(page_title="Meridian Reserve Decision Desk", page_icon="◈", layout="wide")
st.markdown("<style>.stMetric{background:#101b2d;padding:14px;border-radius:12px}.stApp{background:#07111f;color:#e8eef8}</style>", unsafe_allow_html=True)
st.title("◈ Meridian Reserve Decision Desk")
st.caption("Decision-ready portfolio process • Educational analysis, not investment advice")
st.info("AI tools assisted with implementation and documentation. The analysis and decision require student review and ownership.")

sleeves, corr = load_estimates(DATA)

@st.cache_data(ttl=900, show_spinner=False)
def fetch_ticker_history(ticker):
    """Fetch a user-requested ticker for display only; never optimizer input."""
    ticker = ticker.strip().upper()
    if not ticker or not all(ch.isalnum() or ch in '.-' for ch in ticker):
        raise ValueError("Use letters, numbers, periods, or hyphens only.")
    response = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}", params={"range":"6mo","interval":"1d"}, timeout=12)
    response.raise_for_status()
    result = response.json()["chart"]["result"][0]
    rows = [(datetime.fromtimestamp(t, timezone.utc), c) for t,c in zip(result["timestamp"], result["indicators"]["quote"][0]["close"]) if c is not None]
    if not rows: raise ValueError("No usable daily closes returned.")
    return ticker, pd.DataFrame(rows, columns=["Date", "Close"]).set_index("Date")

def saved_fred(series):
    frame = pd.read_csv(ROOT / "data" / f"{series}_2026-10-05.csv")
    date_column = frame.columns[0]
    frame[date_column] = pd.to_datetime(frame[date_column])
    value_column = frame.columns[1]
    frame[value_column] = pd.to_numeric(frame[value_column], errors="coerce")
    return frame.dropna().set_index(date_column)[[value_column]].rename(columns={value_column: series})
with st.sidebar:
    st.header("Mandate controls")
    objective = st.slider("Estimated annual return objective", 3.0, 10.0, 6.5, 0.1) / 100
    reserve = st.slider("BIL / IEF reserve minimum", 0.0, 30.0, 3.0, 1.0) / 100
    st.caption("Long-only · 5% increments · no borrowing or derivatives")
    if st.button("Reset all controls to base"):
        st.rerun()

base = evaluate(equal_weight(sleeves), sleeves, corr)
reference = evaluate(benchmark(sleeves), sleeves, corr)
choice = optimize(sleeves, corr, objective, reserve)

def card(column, title, result):
    with column:
        st.subheader(title)
        if result is None:
            st.error("No feasible 5%-grid portfolio")
            return
        st.metric("Mandate verdict", verdict(result, objective, reserve))
        st.metric("Estimated return", f"{result['return']:.2%}")
        st.metric("Estimated volatility", f"{result['volatility']:.2%}")
        st.metric("Reserve", f"{result['reserve']:.0%}")
        st.dataframe({"Weight": {k: f"{v:.0%}" for k,v in result['weights'].items()}}, use_container_width=True)

left, middle, right = st.columns(3)
card(left, "Equal-weight baseline", base)
card(middle, "60/40 VTI/LQD baseline", reference)
card(right, "Constrained decision", choice)

if choice:
    chart_rows = pd.DataFrame({"Portfolio": ["Equal weight", "60/40 VTI/LQD", "Constrained"], "Return": [base["return"], reference["return"], choice["return"]], "Volatility": [base["volatility"], reference["volatility"], choice["volatility"]]}).set_index("Portfolio")
    st.subheader("Interactive portfolio comparison")
    st.altair_chart(alt.Chart(chart_rows.reset_index()).mark_circle(size=170).encode(
        x=alt.X("Volatility:Q", title="Estimated annual volatility", axis=alt.Axis(format="%")),
        y=alt.Y("Return:Q", title="Estimated annual return", axis=alt.Axis(format="%")),
        color=alt.Color("Portfolio:N", legend=None),
        tooltip=[alt.Tooltip("Portfolio:N"), alt.Tooltip("Return:Q", format=".2%"), alt.Tooltip("Volatility:Q", format=".2%")]
    ).interactive(), use_container_width=True)
    weight_data = pd.DataFrame({"Ticker": list(choice["weights"]), "Weight": list(choice["weights"].values())})
    st.altair_chart(alt.Chart(weight_data).mark_bar(color="#38bdf8").encode(
        x=alt.X("Ticker:N"), y=alt.Y("Weight:Q", axis=alt.Axis(format="%")), tooltip=[alt.Tooltip("Ticker:N"), alt.Tooltip("Weight:Q", format=".0%")]
    ), use_container_width=True)

st.divider()
a, b, c = st.columns(3)
a.metric("LLY reference close", "$1,431.67", "2026-11-16 close")
b.metric("Point-in-time rule", "After close", "No same-day pre-close use")
c.metric("Decision", "PILOT", "not adopt")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Decision rationale", "Stress & stop rule", "Evidence boundary", "LLY driver lab", "Market and Fed explorer"])
with tab1:
    st.write("The constrained portfolio is selected only from portfolios that meet the stated return objective and BIL/IEF reserve rule. The baselines remain visible because a higher return does not excuse a reserve-rule failure.")
with tab2:
    stress = optimize(sleeves, corr, .075, reserve)
    st.write("Recorded stress: raise the objective from 6.5% to 7.5%. Result: BIL 50%, VTI 35%, XLV 15%; 7.52% estimated return and 7.07% volatility.")
    st.warning("Stop the process if no feasible mix exists, a mandate rule fails, point-in-time timing cannot be defended, or the CIO rejects the calendar-year-loss implementation.")
with tab3:
    st.write("Monthly ETF adjusted-close input is preserved through 2026-10-19. LLY is a separate public-company comparison signal as of the 2026-11-16 close, not an optimizer sleeve. The calendar-year-loss limit is disclosed but not coded because the CIO has not defined its measurement convention or breach response.")
with tab4:
    st.subheader("Bounded LLY valuation context")
    st.caption("This panel is a sensitivity context only. It does not change the Meridian fund allocation or create an investment recommendation.")
    x,y,z,w = st.columns(4)
    with x: dcf_wacc = st.slider("WACC (%)", 7.5, 10.0, 8.5, .1) / 100
    with y: volume_shift = st.slider("Cardiometabolic volume shift (pp)", -8.0, 8.0, 0.0, 1.0) / 100
    with z: margin_shift = st.slider("Gross margin shift (pp)", -3.0, 3.0, 0.0, .5) / 100
    with w: capex_shift = st.slider("Capex ratio shift (pp)", -3.0, 3.0, 0.0, .5) / 100
    case = replace(BASE_CASE, wacc=dcf_wacc,
        cardio_volume=tuple(max(-.20, v + volume_shift) for v in BASE_CASE.cardio_volume),
        gross_margin=tuple(max(.65, min(.90, v + margin_shift)) for v in BASE_CASE.gross_margin),
        capex_pct=tuple(max(.03, v + capex_shift) for v in BASE_CASE.capex_pct))
    value = valuation(build(case), case.wacc, case.terminal_growth)
    q1,q2,q3 = st.columns(3)
    q1.metric("Illustrative DCF value/share", f"${value['per_share']:,.2f}")
    q2.metric("LLY reference close", "$1,431.67", "2026-11-16 close")
    q3.metric("Terminal-value share", f"{value['tv_share']:.1%}")
    st.warning("Most distrusted input: WACC. The prior model used an analyst-judgment 8.5% rate. Use `docs/wacc-rebuild.md` before treating a revised rate as decision evidence.")
with tab5:
    st.subheader("Type any public ticker")
    typed = st.text_input("Ticker", value="LLY", max_chars=12, key="market_ticker")
    if st.button("Load ticker chart", key="load_ticker"):
        try:
            symbol, history = fetch_ticker_history(typed)
            st.metric(f"{symbol} latest returned close", f"${history['Close'].iloc[-1]:,.2f}", history.index[-1].strftime("%Y-%m-%d %H:%M UTC"))
            ticker_chart = history.reset_index()
            st.altair_chart(alt.Chart(ticker_chart).mark_line(color="#38bdf8").encode(
                x=alt.X("Date:T", title="Date"), y=alt.Y("Close:Q", title="Close (USD)", scale=alt.Scale(zero=False)),
                tooltip=[alt.Tooltip("Date:T", title="Date"), alt.Tooltip("Close:Q", title="Close", format="$.2f")]
            ).interactive(), use_container_width=True)
            st.caption("Source: Yahoo Finance chart endpoint. Display data may be delayed and is not used by the optimizer.")
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
            st.error(f"Ticker data unavailable: {error}")
    st.subheader("Federal Reserve context from Lab 17")
    fed_left, fed_right = st.columns(2)
    with fed_left:
        dgs10 = saved_fred("DGS10")
        dgs_plot=dgs10.loc["2020-01-01":].reset_index()
        st.altair_chart(alt.Chart(dgs_plot).mark_line(color="#38bdf8").encode(x=alt.X("observation_date:T",title="Date"),y=alt.Y("DGS10:Q",title="Percent",scale=alt.Scale(zero=False)),tooltip=[alt.Tooltip("observation_date:T",title="Date"),alt.Tooltip("DGS10:Q",title="DGS10",format=".2f")]).interactive(),use_container_width=True)
        st.caption("DGS10: 10-year Treasury yield, saved ALFRED vintage as known on 2026-10-05.")
    with fed_right:
        funds = saved_fred("FEDFUNDS")
        funds_plot=funds.loc["2020-01-01":].reset_index()
        st.altair_chart(alt.Chart(funds_plot).mark_line(color="#f59e0b").encode(x=alt.X("observation_date:T",title="Date"),y=alt.Y("FEDFUNDS:Q",title="Percent",scale=alt.Scale(zero=False)),tooltip=[alt.Tooltip("observation_date:T",title="Date"),alt.Tooltip("FEDFUNDS:Q",title="Fed funds rate",format=".2f")]).interactive(),use_container_width=True)
        st.caption("FEDFUNDS: effective federal funds rate, saved ALFRED vintage as known on 2026-10-05.")
    st.info("These rate charts provide macro and discount-rate context. They are not silently inserted into the portfolio optimizer or LLY WACC. See docs/data-card.md for the point-in-time rule.")
