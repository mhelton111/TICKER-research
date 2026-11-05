"""Lab 19: Buffett, Graham, and Burry checks from the same SEC 10-K facts.

Run: python legend_panel.py COST
Replay: python legend_panel.py COST --facts-file raw_data/COST_companyfacts.json --ticker-file raw_data/company_tickers.json
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
USER_AGENT = os.environ.get("SEC_USER_AGENT", "FIN43900 Lab 19 educational contact@example.com")
METRICS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "equity": ("StockholdersEquity",),
    "liabilities": ("Liabilities",),
    "assets_current": ("AssetsCurrent",),
    "liabilities_current": ("LiabilitiesCurrent",),
}
FLOW_METRICS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}


def download_json(url):
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
    ticker_map = ticker_map if ticker_map is not None else download_json(TICKERS_URL)
    for item in ticker_map.values():
        if item["ticker"].upper() == ticker.strip().upper():
            return int(item["cik_str"]), item["title"]
    raise ValueError(f"Ticker {ticker} was not found in the SEC ticker map.")


def usd_facts(facts, tag):
    return facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def annual_10k(fact, is_flow):
    if fact.get("form") != "10-K" or not fact.get("end"):
        return False
    if not is_flow:
        return True
    if not fact.get("start"):
        return False
    days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    return 300 <= days <= 380


def latest_fact(facts, tags, fiscal_end, is_flow):
    for tag in tags:
        candidates = [fact for fact in usd_facts(facts, tag) if fact.get("end") == fiscal_end and annual_10k(fact, is_flow)]
        if candidates:
            selected = max(candidates, key=lambda item: (item.get("filed", ""), item.get("accn", "")))
            return selected["val"] / 1_000_000, tag
    return None, "not found"


def fiscal_ends(facts):
    ends = []
    for tag in METRICS["revenue"]:
        ends.extend(fact["end"] for fact in usd_facts(facts, tag) if annual_10k(fact, is_flow=True))
    result = sorted(set(ends))[-5:]
    if len(result) < 5:
        raise ValueError("Fewer than five annual 10-K revenue facts were found.")
    return result


def build_rows(facts):
    rows = []
    for fiscal_end in fiscal_ends(facts):
        row = {"fiscal_year_end": fiscal_end, "tags": {}}
        for metric, tags in METRICS.items():
            row[metric], row["tags"][metric] = latest_fact(facts, tags, fiscal_end, metric in FLOW_METRICS)
        row["roe"] = None if row["equity"] is None or row["equity"] <= 0 or row["net_income"] is None else row["net_income"] / row["equity"] * 100
        row["owner_earnings"] = None if row["operating_cash_flow"] is None or row["capital_spending"] is None else row["operating_cash_flow"] - row["capital_spending"]
        row["current_ratio"] = None if row["assets_current"] is None or row["liabilities_current"] is None or row["liabilities_current"] <= 0 else row["assets_current"] / row["liabilities_current"]
        row["liabilities_to_equity"] = None if row["liabilities"] is None or row["equity"] is None or row["equity"] <= 0 else row["liabilities"] / row["equity"]
        rows.append(row)
    return rows


def every(values, predicate):
    return "not known" if any(value is None for value in values) else ("pass" if all(predicate(value) for value in values) else "fail")


def buffett_checks(rows):
    roe = [row["roe"] for row in rows]
    owner = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": every(roe, lambda value: value >= 15),
        "Owner earnings positive every year": every(owner, lambda value: value > 0),
        "Owner earnings grew, first year to last": "not known" if owner[0] is None or owner[-1] is None else ("pass" if owner[-1] > owner[0] else "fail"),
    }


def graham_checks(rows, current_ratio_threshold=2.0):
    income = [row["net_income"] for row in rows]
    latest_ratio = rows[-1]["current_ratio"]
    return {
        f"Current ratio of {current_ratio_threshold:.1f} or more, latest year": "not known" if latest_ratio is None else ("pass" if latest_ratio >= current_ratio_threshold else "fail"),
        "Net income positive every year": every(income, lambda value: value > 0),
        "Net income grew, first year to last": "not known" if income[0] is None or income[-1] is None else ("pass" if income[-1] > income[0] else "fail"),
    }


def burry_checks(rows):
    cash_vs_income = [None if row["operating_cash_flow"] is None or row["net_income"] is None else row["operating_cash_flow"] - row["net_income"] for row in rows]
    latest_leverage = rows[-1]["liabilities_to_equity"]
    return {
        "Operating cash flow at least net income every year": every(cash_vs_income, lambda value: value >= 0),
        "Liabilities no more than twice equity, latest year": "not known" if latest_leverage is None else ("pass" if latest_leverage <= 2 else "fail"),
    }


def verdict(checks, positive_verdict, neutral_verdict="watch"):
    values = list(checks.values())
    if any(value == "not known" for value in values):
        return "watch — incomplete facts"
    return positive_verdict if all(value == "pass" for value in values) else neutral_verdict


def fmt(value, decimals=2):
    return "not found" if value is None else f"{value:,.{decimals}f}"


def memo_texts(ticker, company, rows, panel_checks, threshold):
    first, latest = rows[0], rows[-1]
    b = panel_checks["Buffett"]
    g = panel_checks["Graham"]
    u = panel_checks["Burry"]
    buffett = f"""# Buffett memo — {ticker}

**Verdict:** **{verdict(b, 'own the business')}**

ROE moved from {fmt(first['roe'], 1)}% to {fmt(latest['roe'], 1)}%, and owner earnings moved from ${fmt(first['owner_earnings'], 1)} million to ${fmt(latest['owner_earnings'], 1)} million. The code checks are {', '.join(b.values())}. This is a business-quality screen only; no price or valuation data were used.
"""
    graham = f"""# Graham memo — {ticker}

**Verdict:** **{verdict(g, 'watch')}**

The latest current ratio is {fmt(latest['current_ratio'])} against the stated {fmt(threshold)} threshold. Net income moved from ${fmt(first['net_income'], 1)} million to ${fmt(latest['net_income'], 1)} million. The code checks are {', '.join(g.values())}; a balance-sheet screen can reject a company even when earnings improve. No price data were used.
"""
    burry = f"""# Burry memo — {ticker}

**Verdict:** **{verdict(u, 'watch')}**

The latest liabilities-to-equity ratio is {fmt(latest['liabilities_to_equity'])}, and the code compares operating cash flow with net income for every reported year. The code checks are {', '.join(u.values())}. This is a forensic screen, not proof that all accounting risk has been eliminated. No price data were used.
"""
    return {"Buffett": buffett, "Graham": graham, "Burry": burry}


def printed_number_tokens(rows, threshold):
    allowed = {"0", fmt(threshold).replace(",", "")}
    for row in rows:
        allowed.update(row["fiscal_year_end"].replace("-", " ").split())
        for value in row.values():
            if isinstance(value, (float, int)):
                allowed.add(fmt(value).replace(",", ""))
                allowed.add(fmt(value, 1).replace(",", ""))
    return allowed


def unprinted_numbers(memos, rows, threshold):
    allowed = printed_number_tokens(rows, threshold)
    flags = {}
    for investor, memo in memos.items():
        tokens = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", memo)
        flags[investor] = sorted({token for token in tokens if token.replace(",", "") not in allowed})
    return flags


def analyze(ticker, facts=None, ticker_map=None, graham_threshold=2.0):
    cik, company = ticker_to_cik(ticker, ticker_map)
    facts = facts if facts is not None else download_json(FACTS_URL.format(cik=cik))
    rows = build_rows(facts)
    panel_checks = {"Buffett": buffett_checks(rows), "Graham": graham_checks(rows, graham_threshold), "Burry": burry_checks(rows)}
    memos = memo_texts(ticker.upper(), company, rows, panel_checks, graham_threshold)
    return {"ticker": ticker.upper(), "cik": f"{cik:010d}", "company": company, "rows": rows, "checks": panel_checks,
            "memos": memos, "graham_threshold": graham_threshold, "memo_flags": unprinted_numbers(memos, rows, graham_threshold)}


def print_analysis(analysis):
    print(f"{analysis['ticker']} | CIK {analysis['cik']} | {analysis['company']}")
    print("Fiscal year end | Current ratio | Liabilities/equity | Net income | Operating cash flow | Equity")
    for row in analysis["rows"]:
        print(" | ".join([row["fiscal_year_end"], fmt(row["current_ratio"]), fmt(row["liabilities_to_equity"]), fmt(row["net_income"], 1), fmt(row["operating_cash_flow"], 1), fmt(row["equity"], 1)]))
    for investor, checks in analysis["checks"].items():
        print(investor)
        for label, result in checks.items():
            print(f"  {label}: {result}")
    for investor, flags in analysis["memo_flags"].items():
        print(f"{investor} memo unprinted numbers: {', '.join(flags) if flags else 'none'}")


def main():
    parser = argparse.ArgumentParser(description="Compute Lab 19 investor-panel checks from SEC 10-K facts.")
    parser.add_argument("ticker")
    parser.add_argument("--facts-file", type=Path)
    parser.add_argument("--ticker-file", type=Path)
    parser.add_argument("--graham-current-ratio", type=float, default=2.0)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    facts = json.loads(args.facts_file.read_text(encoding="utf-8")) if args.facts_file else None
    ticker_map = json.loads(args.ticker_file.read_text(encoding="utf-8")) if args.ticker_file else None
    analysis = analyze(args.ticker, facts, ticker_map, args.graham_current_ratio)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for investor, memo in analysis["memos"].items():
        (args.output_dir / f"{analysis['ticker']}_{investor.lower()}_memo.md").write_text(memo, encoding="utf-8")
    print_analysis(analysis)


if __name__ == "__main__":
    main()
