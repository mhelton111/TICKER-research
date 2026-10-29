"""Pure parsing and audit functions for Lab 17; no Streamlit or network calls."""

from io import StringIO
import re

import pandas as pd


SERIES_ID = re.compile(r"^[A-Za-z0-9_-]{1,40}$")


def clean_series_id(series_id):
    """Normalize a user-entered FRED ID and reject unsafe/malformed IDs."""
    series_id = series_id.strip().upper()
    if not SERIES_ID.fullmatch(series_id):
        raise ValueError("Series ID must use only letters, numbers, underscores, or hyphens (40 characters or fewer).")
    return series_id


def parse_fred_csv(text, requested_id):
    """Parse FRED/ALFRED graph CSV, treating '.' as a missing observation."""
    frame = pd.read_csv(StringIO(text), na_values=".")
    if frame.empty or "observation_date" not in frame.columns:
        raise ValueError("The download did not contain an observation_date column.")
    value_columns = [column for column in frame.columns if column != "observation_date"]
    if len(value_columns) != 1:
        raise ValueError("The download did not contain exactly one requested series column.")
    frame = frame.rename(columns={"observation_date": "date", value_columns[0]: "value"})[["date", "value"]]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.dropna(subset=["date", "value"]).drop_duplicates("date", keep="last").sort_values("date")
    if frame.empty:
        raise ValueError(f"{requested_id} returned no usable observations.")
    return frame.set_index("date")


def calculate_audit(today, asof, as_known_on):
    """Calculate the required last-known, late, and same-date-revision fields."""
    cutoff = pd.Timestamp(as_known_on)
    asof = asof.loc[asof.index <= cutoff]
    if asof.empty:
        raise ValueError("ALFRED returned no non-missing observation on or before this as-known-on date.")
    last_date = asof.index.max()
    asof_value = float(asof.loc[last_date, "value"])
    same_dates = today.index.intersection(asof.index)
    revised = 0
    if len(same_dates):
        revised = int((today.loc[same_dates, "value"].round(12) != asof.loc[same_dates, "value"].round(12)).sum())
    return {
        "last_known_date": last_date,
        "last_known_value": asof_value,
        "today_last_date": today.index.max(),
        "today_last_value": float(today.iloc[-1]["value"]),
        "published_later_count": int((today.index > last_date).sum()),
        "revised_count": revised,
    }
