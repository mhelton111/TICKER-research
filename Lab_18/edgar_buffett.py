"""Lab 18: deterministic Buffett-style 10-K metrics from SEC EDGAR facts.

Run: python edgar_buffett.py COST
Optional reproducibility mode: python edgar_buffett.py COST --facts-file raw_data/COST_companyfacts.json
"""

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path
import subprocess
from urllib.error import URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
# Set SEC_USER_AGENT to a real name and contact email before live requests.
USER_AGENT = os.environ.get("SEC_USER_AGENT", "FIN43900 Lab 18 educational contact@example.com")
METRICS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "equity": ("StockholdersEquity",),
}
FLOW_METRICS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}


def download_json(url):
    """Retrieve public SEC JSON with a declared User-Agent; curl is a Windows fallback."""
    try:
        request = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError) as first_error:
        try:
            result = subprocess.run(
                ["curl.exe", "-L", "--fail", "--silent", "--show-error", "--connect-timeout", "30", "-A", USER_AGENT, url],
                capture_output=True, check=True, text=True, timeout=40,
            )
            return json.loads(result.stdout)
        except (FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError) as second_error:
            raise RuntimeError(f"SEC download failed ({first_error}); curl fallback failed ({second_error}).") from second_error


def ticker_to_cik(ticker, ticker_map=None):
    ticker = ticker.strip().upper()
    ticker_map = ticker_map if ticker_map is not None else download_json(TICKERS_URL)
    for item in ticker_map.values():
        if item["ticker"].upper() == ticker:
            return int(item["cik_str"]), item["title"]
    raise ValueError(f"Ticker {ticker} was not found in SEC company_tickers.json.")


def usd_facts(facts, tag):
    concept = facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    return concept.get("units", {}).get("USD", [])


def is_annual_10k(fact, flow):
    if fact.get("form") != "10-K" or not fact.get("end"):
        return False
    if not flow:
        return True
    if not fact.get("start"):
        return False
    days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    return 300 <= days <= 380


def latest_fact_for_year(facts, tags, fiscal_end, flow):
    """Select preferred tag and the latest filed 10-K fact for one fiscal-year end."""
    for tag in tags:
        candidates = [fact for fact in usd_facts(facts, tag) if fact.get("end") == fiscal_end and is_annual_10k(fact, flow)]
        if candidates:
            selected = max(candidates, key=lambda fact: (fact.get("filed", ""), fact.get("accn", "")))
            return selected["val"], tag
    return None, "not found"


def fiscal_ends(facts):
    """Use annual 10-K revenue facts to define the most recent five fiscal years."""
    candidates = []
    for tag in METRICS["revenue"]:
        candidates.extend(fact["end"] for fact in usd_facts(facts, tag) if is_annual_10k(fact, flow=True))
    return sorted(set(candidates))[-5:]


def millions(value):
    return None if value is None else value / 1_000_000


def build_rows(facts):
    ends = fiscal_ends(facts)
    if len(ends) < 5:
        raise ValueError("Fewer than five annual 10-K revenue facts were found.")
    rows = []
    for fiscal_end in ends:
        row = {"fiscal_year_end": fiscal_end, "tags": {}}
        for metric, tags in METRICS.items():
            value, tag = latest_fact_for_year(facts, tags, fiscal_end, metric in FLOW_METRICS)
            row[metric] = millions(value)
            row["tags"][metric] = tag
        equity = row["equity"]
        row["roe"] = None if equity is None or equity <= 0 or row["net_income"] is None else row["net_income"] / equity * 100
        row["owner_earnings"] = None if row["operating_cash_flow"] is None or row["capital_spending"] is None else row["operating_cash_flow"] - row["capital_spending"]
        rows.append(row)
    return rows


def every(values, predicate):
    return "not known" if any(value is None for value in values) else ("pass" if all(predicate(value) for value in values) else "fail")


def checks(rows):
    roe = [row["roe"] for row in rows]
    owner = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": every(roe, lambda value: value >= 15),
        "Owner earnings positive every year": every(owner, lambda value: value > 0),
        "Owner earnings grew, first year to last": "not known" if owner[0] is None or owner[-1] is None else ("pass" if owner[-1] > owner[0] else "fail"),
    }


def display(value, decimals=1):
    return "not found" if value is None else f"{value:,.{decimals}f}"


def memo_text(ticker, company, rows, result_checks):
    """Write a bounded Buffett-style business memo using only computed outputs, never price data."""
    first, last = rows[0], rows[-1]
    owner_available = first["owner_earnings"] is not None and last["owner_earnings"] is not None
    if not owner_available:
        verdict = "watch"
        owner_sentence = "Owner earnings are not known because the required operating-cash-flow or capital-spending input was not found in the 10-K facts."
    elif all(value == "pass" for value in result_checks.values()):
        verdict = "own the business"
        owner_sentence = f"Owner earnings rose from ${display(first['owner_earnings'])} million to ${display(last['owner_earnings'])} million across the reported period."
    else:
        verdict = "watch"
        owner_sentence = f"Owner earnings moved from ${display(first['owner_earnings'])} million to ${display(last['owner_earnings'])} million, so the mechanical checks do not justify an unqualified business verdict."
    roe_sentence = "ROE is not known for every year." if any(row["roe"] is None for row in rows) else f"ROE ran from {display(first['roe'])}% in the first reported year to {display(last['roe'])}% in the last reported year."
    return f"""# Buffett-style business memo — {ticker}

**Company:** {company}  
**Verdict:** **{verdict}**

This is a business-quality judgment, not a price or buy/sell recommendation. {roe_sentence} {owner_sentence} The three code checks are: ROE of 15% or more every year — **{result_checks['ROE of 15% or more every year']}**; owner earnings positive every year — **{result_checks['Owner earnings positive every year']}**; and owner earnings grew from the first year to the last — **{result_checks['Owner earnings grew, first year to last']}**.

The annual filing facts support a review of earning power, but they do not establish a durable moat, management quality, or a sensible purchase price. Those are judgment questions that require evidence beyond this five-year fact table. No market-price data were used.
"""


def printed_numbers(rows, result_checks):
    """Numeric tokens permitted in a memo: fiscal-end dates, table values, and 15% check threshold."""
    allowed = {"15", "0"}
    for row in rows:
        allowed.update(row["fiscal_year_end"].replace("-", " ").split())
        for metric in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "roe", "owner_earnings"):
            value = row[metric]
            if value is not None:
                allowed.add(display(value).replace(",", ""))
                allowed.add(display(value, 1).replace(",", ""))
    return allowed


def unprinted_memo_numbers(memo, rows, result_checks):
    """Return memo number tokens that do not originate in printed table/check inputs."""
    allowed = printed_numbers(rows, result_checks)
    tokens = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", memo)
    return sorted({token for token in tokens if token.replace(",", "") not in allowed})


def analysis_for_ticker(ticker, facts=None, ticker_map=None):
    cik, company = ticker_to_cik(ticker, ticker_map)
    facts = facts if facts is not None else download_json(FACTS_URL.format(cik=cik))
    rows = build_rows(facts)
    result_checks = checks(rows)
    memo = memo_text(ticker.upper(), company, rows, result_checks)
    return {"ticker": ticker.upper(), "cik": f"{cik:010d}", "company": company, "rows": rows, "checks": result_checks, "memo": memo}


def print_analysis(analysis):
    print(f"{analysis['ticker']} | CIK {analysis['cik']} | {analysis['company']}")
    print("Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE % | Owner earnings")
    for row in analysis["rows"]:
        values = [row["fiscal_year_end"], *(display(row[key]) for key in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity")), display(row["roe"]), display(row["owner_earnings"])]
        print(" | ".join(values))
        print("  tags: " + "; ".join(f"{key}={tag}" for key, tag in row["tags"].items()))
    print("Checks")
    for label, result in analysis["checks"].items():
        print(f"  {label}: {result}")


def main():
    parser = argparse.ArgumentParser(description="Compute Lab 18 Buffett checks from SEC 10-K XBRL facts.")
    parser.add_argument("ticker")
    parser.add_argument("--facts-file", type=Path, help="Use a saved SEC companyfacts JSON file.")
    parser.add_argument("--ticker-file", type=Path, help="Use a saved SEC company_tickers JSON file.")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    facts = json.loads(args.facts_file.read_text(encoding="utf-8")) if args.facts_file else None
    ticker_map = json.loads(args.ticker_file.read_text(encoding="utf-8")) if args.ticker_file else None
    analysis = analysis_for_ticker(args.ticker, facts, ticker_map)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    memo_path = args.output_dir / f"{analysis['ticker']}_buffett_memo.md"
    memo_path.write_text(analysis["memo"], encoding="utf-8")
    print_analysis(analysis)
    print(f"Memo saved: {memo_path}")


if __name__ == "__main__":
    main()
