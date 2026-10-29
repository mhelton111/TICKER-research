"""Lab 17 point-in-time FRED/ALFRED rate viewer.

Run from this folder: streamlit run asof_app.py
The app uses the public CSV endpoints specified by the course; no API key is
needed or accepted.  It never writes credentials or downloaded data to disk.
"""

from datetime import date
import pandas as pd
import requests
import streamlit as st
import altair as alt

from asof_core import calculate_audit, clean_series_id, parse_fred_csv


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}
FRED_GRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_GRAPH = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"
def _download(url, series_id):
    response = requests.get(url, timeout=30, headers={"User-Agent": "FIN43900-Lab17 educational app"})
    response.raise_for_status()
    return parse_fred_csv(response.text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fred_csv(series_id):
    """Get the latest values visible on FRED today (one HTTP request per ID)."""
    series_id = clean_series_id(series_id)
    return _download(FRED_GRAPH.format(series_id=series_id), series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_alfred_csv(series_id, vintage_date):
    """Get the vintage visible on `vintage_date` from ALFRED (one request per ID)."""
    series_id = clean_series_id(series_id)
    vintage_date = pd.Timestamp(vintage_date).date().isoformat()
    return _download(ALFRED_GRAPH.format(series_id=series_id, vintage_date=vintage_date), series_id)


def format_value(value):
    return f"{value:,.3f}".rstrip("0").rstrip(".")


def point_in_time_chart(series_id, current, vintage, start_date, as_known_on):
    """Create a clear current-versus-vintage chart without changing the audit data."""
    start = pd.Timestamp(start_date)
    current_plot = current.loc[current.index >= start].reset_index(names="date")
    current_plot["vintage"] = "Current FRED values"
    vintage_plot = vintage.loc[vintage.index >= start].reset_index(names="date")
    vintage_plot["vintage"] = f"Known on {as_known_on.isoformat()}"
    chart_data = pd.concat([current_plot, vintage_plot], ignore_index=True)
    base = alt.Chart(chart_data).encode(
        x=alt.X("date:T", title="Observation date"),
        y=alt.Y("value:Q", title="Percent", scale=alt.Scale(zero=False)),
        color=alt.Color("vintage:N", title=None, scale=alt.Scale(range=["#164e63", "#f59e0b"])),
        tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("value:Q", title="Value", format=".3f"), alt.Tooltip("vintage:N", title="Series")],
    )
    lines = base.mark_line(strokeWidth=2.5).encode(strokeDash=alt.condition(alt.datum.vintage == "Current FRED values", alt.value([1, 0]), alt.value([6, 4])))
    cutoff = alt.Chart(pd.DataFrame({"date": [pd.Timestamp(as_known_on)]})).mark_rule(color="#64748b", strokeDash=[4, 4]).encode(x="date:T")
    return (lines + cutoff).properties(height=310, title=f"{series_id}: current history versus selected vintage").interactive()


st.set_page_config(page_title="Point-in-Time Rate Audit", layout="wide")
st.title("Point-in-Time Rate Audit")
st.caption("Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded live; built with AI help, a learning demonstration, not investment advice.")
st.info("Blue is the latest FRED history. Gold is the selected ALFRED vintage. The dashed vertical line marks the information cutoff.")

with st.sidebar:
    st.header("Audit controls")
    selected_ids = st.multiselect("Rate series", options=list(SERIES), default=list(SERIES), format_func=lambda item: f"{item} — {SERIES[item]}")
    extra_id = st.text_input("Add another FRED series ID", placeholder="Example: PAYEMS or a prework series")
    start_date = st.date_input("Chart start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today(), max_value=date.today())

if extra_id.strip():
    try:
        extra_id = clean_series_id(extra_id)
        if extra_id not in selected_ids:
            selected_ids.append(extra_id)
    except ValueError as error:
        st.sidebar.error(str(error))

if not selected_ids:
    st.info("Choose at least one series in the sidebar.")
    st.stop()

rows = []
for series_id in selected_ids:
    label = SERIES.get(series_id, "User-entered FRED series")
    st.subheader(f"{series_id} — {label}")
    try:
        today_values = fetch_fred_csv(series_id)
        vintage_values = fetch_alfred_csv(series_id, as_known_on.isoformat())
        if today_values.loc[today_values.index >= pd.Timestamp(start_date)].empty:
            st.warning(f"{series_id}: no current values on or after {start_date.isoformat()}.")
        else:
            st.altair_chart(point_in_time_chart(series_id, today_values, vintage_values, start_date, as_known_on), use_container_width=True)
        audit = calculate_audit(today_values, vintage_values, as_known_on)
        metric_current, metric_vintage, metric_revisions = st.columns(3)
        metric_current.metric("Latest FRED value", format_value(audit["today_last_value"]), audit["today_last_date"].date().isoformat())
        metric_vintage.metric(f"Known on {as_known_on.isoformat()}", format_value(audit["last_known_value"]), audit["last_known_date"].date().isoformat())
        metric_revisions.metric("Same-date revisions", audit["revised_count"], "Compared with selected vintage")
        rows.append({
            "Series": series_id,
            "FRED page": f"https://fred.stlouisfed.org/series/{series_id}",
            "Last date known then": audit["last_known_date"].date(),
            "Value known then": format_value(audit["last_known_value"]),
            "Last date measured today": audit["today_last_date"].date(),
            "Value today": format_value(audit["today_last_value"]),
            "Today's values after last known date": audit["published_later_count"],
            "Same-date values revised": audit["revised_count"],
        })
    except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
        st.error(f"{series_id}: {error}")

if rows:
    st.subheader("Point-in-time audit table")
    table = pd.DataFrame(rows)
    st.dataframe(
        table,
        column_config={"FRED page": st.column_config.LinkColumn("FRED page", display_text="Open series")},
        hide_index=True,
        use_container_width=True,
    )

st.divider()
st.markdown("**Interpretation:** ‘Today's values after last known date’ measures release lag. ‘Same-date values revised’ compares the ALFRED vintage with today's FRED values only where both report the same observation date. A zero revision count does not prove a series is never revised; it only describes the selected vintage comparison.")
