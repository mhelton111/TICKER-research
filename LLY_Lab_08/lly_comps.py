"""Lab 08 LLY P/E peer comparison. Run: python lly_comps.py"""

from statistics import median


# Editable inputs. Prices and annual GAAP diluted EPS are USD per share.
TARGET = {"symbol": "LLY", "name": "Eli Lilly and Company", "price": 1124.21, "eps": 22.95}
PEERS = [
    {"symbol": "AMGN", "name": "Amgen Inc.", "price": 391.27, "eps": 14.23},
    {"symbol": "GILD", "name": "Gilead Sciences, Inc.", "price": 145.65, "eps": 6.78},
]


def positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def format_value(value: object) -> str:
    return f"${value:.2f}" if isinstance(value, (int, float)) and not isinstance(value, bool) else "missing"


def valid_price_and_eps(company: dict[str, object]) -> bool:
    """A positive P/E requires positive price and annual diluted EPS."""
    return positive_number(company.get("price")) and positive_number(company.get("eps"))


def unique_non_target_peers() -> list[dict[str, object]]:
    """Deduplicate ticker symbols and exclude the target from its own peer set."""
    seen_symbols = set()
    accepted = []
    target_symbol = str(TARGET.get("symbol", ""))
    for peer in PEERS:
        symbol = str(peer.get("symbol", ""))
        if symbol == target_symbol or symbol in seen_symbols:
            continue
        seen_symbols.add(symbol)
        accepted.append(peer)
    return accepted


def pe_multiple(company: dict[str, object]) -> float | None:
    if not valid_price_and_eps(company):
        return None
    return float(company["price"]) / float(company["eps"])


def implied_price(multiple: float) -> float | None:
    if not positive_number(TARGET.get("eps")):
        return None
    return multiple * float(TARGET["eps"])


def print_peer_multiples(peers: list[dict[str, object]]) -> list[tuple[dict[str, object], float]]:
    valid_peers = []
    print("Peer P/E multiples")
    for peer in peers:
        multiple = pe_multiple(peer)
        if multiple is None:
            print(f"{peer['symbol']} P/E: not meaningful (price and annual diluted EPS must both be positive).")
        else:
            print(f"{peer['symbol']} P/E: {multiple:.6f}x")
            valid_peers.append((peer, multiple))
    return valid_peers


def print_full_peer_estimate(valid_peers: list[tuple[dict[str, object], float]]) -> float | None:
    if not valid_peers:
        print("\nPeer estimate: no usable peers.")
        return None
    if not positive_number(TARGET.get("eps")):
        print("\nTarget implied prices: not meaningful (target annual diluted EPS must be positive).")
        return None

    multiples = [multiple for _, multiple in valid_peers]
    low, middle, high = min(multiples), median(multiples), max(multiples)
    low_price, middle_price, high_price = (implied_price(value) for value in (low, middle, high))
    print(f"\nPeer median P/E: {middle:.6f}x")
    if len(valid_peers) == 1:
        print(f"LLY reference estimate (one usable peer; no range): ${middle_price:.2f}")
    else:
        print(f"LLY implied range: ${low_price:.2f}-${high_price:.2f}")
        print(f"LLY at peer median: ${middle_price:.2f}")
    return middle_price


def print_leave_one_out(valid_peers: list[tuple[dict[str, object], float]], full_estimate: float | None) -> None:
    print("\nLeave-one-out checks")
    for removed_peer, _ in valid_peers:
        remaining = [multiple for peer, multiple in valid_peers if peer is not removed_peer]
        if not remaining or full_estimate is None:
            print(f"Remove {removed_peer['symbol']}: no estimate (no usable peers remain).")
            continue
        remaining_estimate = implied_price(median(remaining))
        change = remaining_estimate - full_estimate
        label = "reference estimate" if len(remaining) == 1 else "median-implied price"
        print(f"Remove {removed_peer['symbol']}: remaining {label} ${remaining_estimate:.2f}; change from full-peer estimate ${change:+.2f}")


def main() -> None:
    print("Lab 08: Eli Lilly P/E peer comparison")
    print(f"Comparison date: September 9, 2026 regular-market close")
    print(
        f"Target: {TARGET['name']} ({TARGET['symbol']}), "
        f"price {format_value(TARGET.get('price'))}, "
        f"FY2025 GAAP diluted EPS {format_value(TARGET.get('eps'))}"
    )
    target_multiple = pe_multiple(TARGET)
    if target_multiple is None:
        print("LLY observed P/E: not meaningful (price and annual diluted EPS must both be positive).")
    else:
        print(f"LLY observed P/E (comparison only): {target_multiple:.6f}x")
    valid_peers = print_peer_multiples(unique_non_target_peers())
    full_estimate = print_full_peer_estimate(valid_peers)
    print_leave_one_out(valid_peers, full_estimate)


if __name__ == "__main__":
    main()
