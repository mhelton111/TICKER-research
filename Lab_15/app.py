"""Streamlit user interface for the Lab 15 portfolio engine."""

from copy import deepcopy
from datetime import datetime, timezone

import requests
import streamlit as st

from portfolio import CORRELATIONS, OBJECTIVE_RETURN, RESERVE_ELIGIBLE, SLEEVES, estimate_from_csv, search_lowest_risk_mix


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")


@st.cache_data(ttl=60, show_spinner=False)
def yahoo_intraday_quote(ticker):
    """Return a live market-data quote, preferring Yahoo Finance and falling back to Nasdaq."""
    ticker = ticker.strip().upper()
    if not ticker or not all(character.isalnum() or character in ".-" for character in ticker):
        return None, "Enter a ticker using letters, numbers, periods, or hyphens."
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    try:
        response = requests.get(url, params={"range": "1d", "interval": "1m"}, timeout=10)
        response.raise_for_status()
        result = response.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]
        observations = [(stamp, close) for stamp, close in zip(timestamps, closes) if close is not None]
        if not observations:
            raise ValueError("Yahoo Finance returned no intraday price for this ticker.")
        timestamp, price = observations[-1]
        return {"ticker": ticker, "price": price, "time": datetime.fromtimestamp(timestamp, timezone.utc), "source": "Yahoo Finance"}, None
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
        try:
            response = requests.get(
                f"https://api.nasdaq.com/api/quote/{ticker}/info",
                params={"assetclass": "stocks"},
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            primary_data = response.json()["data"]["primaryData"]
            price = float(primary_data["lastSalePrice"].replace("$", "").replace(",", ""))
            return {"ticker": ticker, "price": price, "time": primary_data.get("lastTradeTimestamp", "time not supplied"), "source": "Nasdaq (Yahoo unavailable)"}, None
        except (requests.RequestException, KeyError, TypeError, ValueError) as fallback_error:
            return None, f"Yahoo Finance unavailable ({error}); Nasdaq fallback unavailable ({fallback_error})."


with st.expander("Optional Yahoo Finance market-data check (not optimizer input)"):
    live_ticker = st.text_input("Ticker", value="LLY", max_chars=12).upper()
    if st.button("Get latest market price"):
        quote, error = yahoo_intraday_quote(live_ticker)
        if error:
            st.warning(error)
        else:
            st.metric(f"{quote['ticker']} latest price", f"${quote['price']:,.2f}")
            timestamp = quote["time"] if isinstance(quote["time"], str) else quote["time"].strftime("%Y-%m-%d %H:%M UTC")
            st.caption(f"Source: {quote['source']}; timestamp: {timestamp}. Intraday data may be delayed.")
    st.link_button("Open LLY on Yahoo Finance", "https://finance.yahoo.com/quote/LLY/")
    st.caption("This panel is informational only. The optimizer continues to use the dated monthly adjusted-close CSV so its lab results remain reproducible.")

with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input("Objective return (%)", value=OBJECTIVE_RETURN * 100, step=0.1) / 100
    reserve_minimum = st.number_input("Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0, step=1.0) / 100
    uploaded = st.file_uploader("Upload monthly prices CSV", type="csv")
    last_36 = st.toggle("Use last 36 monthly returns", value=False)

try:
    if uploaded is not None:
        base_sleeves, correlations = estimate_from_csv(uploaded, last_36)
        st.info("Using return, volatility, and correlation estimates calculated from the uploaded CSV.")
    else:
        base_sleeves, correlations = deepcopy(SLEEVES), deepcopy(CORRELATIONS)
        st.info("Using Meridian's course-authored training inputs. Upload prices.csv for your fund universe.")
except ValueError as error:
    st.error(str(error))
    st.stop()

st.subheader("Expected-return estimates")
edited_sleeves = deepcopy(base_sleeves)
columns = st.columns(len(base_sleeves))
for column, name in zip(columns, base_sleeves):
    with column:
        edited_sleeves[name]["return"] = st.number_input(
            f"{base_sleeves[name]['label']} (%)", value=float(base_sleeves[name]["return"] * 100), step=0.1, key=f"return_{name}"
        ) / 100

st.subheader("Reserve eligibility")
eligible = []
checkboxes = st.columns(len(edited_sleeves))
for column, name in zip(checkboxes, edited_sleeves):
    if column.checkbox(edited_sleeves[name]["label"], value=name in RESERVE_ELIGIBLE, key=f"eligible_{name}"):
        eligible.append(name)

loaded_answer = search_lowest_risk_mix(base_sleeves, correlations, objective, eligible, reserve_minimum)
edited_answer = search_lowest_risk_mix(edited_sleeves, correlations, objective, eligible, reserve_minimum)

def display_answer(column, title, answer):
    with column:
        st.subheader(title)
        if answer is None:
            st.warning("No mix meets the objective and reserve rule.")
            return
        st.dataframe({"Weight (%)": {name: round(weight * 100, 0) for name, weight in answer["weights"].items()}}, width="stretch")
        st.metric("Expected return", f"{answer['return'] * 100:.2f}%")
        st.metric("Volatility", f"{answer['volatility'] * 100:.2f}%")
        st.metric("Reserve-eligible weight", f"{answer['reserve_weight'] * 100:.0f}%")

left, right = st.columns(2)
display_answer(left, "As loaded", loaded_answer)
display_answer(right, "With edited return estimates", edited_answer)

if loaded_answer and edited_answer:
    largest_change = max(abs(edited_answer["weights"][name] - loaded_answer["weights"][name]) for name in edited_sleeves)
    st.success(f"Largest weight change: {largest_change * 100:.0f} points")
