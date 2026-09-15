"""Lab 07 P/E comparable-company training case. Run: python comps.py"""

from statistics import median


# Editable target and peer inputs. Prices are dollars per share; EPS is annual GAAP diluted EPS.
TARGET = {"symbol": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"symbol": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92},
    {"symbol": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81},
]


def valid_price_and_eps(company: dict[str, object]) -> bool:
    """P/E is meaningful only for positive numeric price and annual diluted EPS."""
    price, eps = company.get("price"), company.get("eps")
    return (
        isinstance(price, (int, float))
        and not isinstance(price, bool)
        and price > 0
        and isinstance(eps, (int, float))
        and not isinstance(eps, bool)
        and eps > 0
    )


def valid_target_eps() -> bool:
    eps = TARGET.get("eps")
    return isinstance(eps, (int, float)) and not isinstance(eps, bool) and eps > 0


def format_input(value: object) -> str:
    return f"${value:.2f}" if isinstance(value, (int, float)) and not isinstance(value, bool) else "missing"


def unique_non_target_peers() -> list[dict[str, object]]:
    """Deduplicate on ticker and exclude the target from its own peer set."""
    unique_peers = []
    seen_symbols = set()
    target_symbol = str(TARGET["symbol"])
    for peer in PEERS:
        symbol = str(peer.get("symbol", ""))
        if symbol == target_symbol or symbol in seen_symbols:
            continue
        seen_symbols.add(symbol)
        unique_peers.append(peer)
    return unique_peers


def peer_multiple(peer: dict[str, object]) -> float | None:
    if not valid_price_and_eps(peer):
        return None
    return float(peer["price"]) / float(peer["eps"])


def implied_price(multiple: float) -> float | None:
    if not valid_target_eps():
        return None
    return multiple * float(TARGET["eps"])


def print_peer_multiples(peers: list[dict[str, object]]) -> list[tuple[dict[str, object], float]]:
    valid_peers = []
    print("Peer P/E multiples")
    for peer in peers:
        multiple = peer_multiple(peer)
        if multiple is None:
            print(f"{peer['symbol']} P/E: not meaningful (price and diluted EPS must both be positive)")
        else:
            print(f"{peer['symbol']} P/E: {multiple:.6f}x")
            valid_peers.append((peer, multiple))
    return valid_peers


def print_full_peer_estimate(valid_peers: list[tuple[dict[str, object], float]]) -> float | None:
    if not valid_peers:
        print("\nPeer estimate: no usable peers.")
        return None
    if not valid_target_eps():
        print("\nTarget implied prices: not meaningful (target diluted EPS must be positive).")
        return None

    multiples = [multiple for _, multiple in valid_peers]
    minimum, midpoint, maximum = min(multiples), median(multiples), max(multiples)
    low_price, median_price, high_price = (implied_price(value) for value in (minimum, midpoint, maximum))
    print(f"\nPeer median P/E: {midpoint:.6f}x")
    if len(valid_peers) == 1:
        print(f"Target reference estimate (one usable peer; no range): ${median_price:.2f}")
    else:
        print(f"Target implied range: ${low_price:.2f}-${high_price:.2f}")
        print(f"Target at peer median: ${median_price:.2f}")
    return median_price


def print_leave_one_out(valid_peers: list[tuple[dict[str, object], float]], full_estimate: float | None) -> None:
    print("\nLeave-one-out checks")
    for removed_peer, _ in valid_peers:
        remaining_multiples = [multiple for peer, multiple in valid_peers if peer is not removed_peer]
        if not remaining_multiples or full_estimate is None:
            print(f"Remove {removed_peer['symbol']}: no estimate (no usable peers remain).")
            continue
        remaining_estimate = implied_price(median(remaining_multiples))
        change = remaining_estimate - full_estimate
        label = "reference estimate" if len(remaining_multiples) == 1 else "median-implied price"
        print(f"Remove {removed_peer['symbol']}: remaining {label} ${remaining_estimate:.2f}; change from full-peer estimate ${change:+.2f}")


def main() -> None:
    print("Lab 07: Asbury Automotive P/E comparable-company training case")
    print(
        f"Target: {TARGET['name']} ({TARGET['symbol']}), "
        f"price {format_input(TARGET.get('price'))}, "
        f"FY2024 GAAP diluted EPS {format_input(TARGET.get('eps'))}"
    )
    target_multiple = peer_multiple(TARGET)
    if target_multiple is None:
        print("Target observed P/E: not meaningful (price and diluted EPS must both be positive)")
    else:
        print(f"Target observed P/E (comparison only): {target_multiple:.6f}x")
    peers = unique_non_target_peers()
    valid_peers = print_peer_multiples(peers)
    full_estimate = print_full_peer_estimate(valid_peers)
    print_leave_one_out(valid_peers, full_estimate)


if __name__ == "__main__":
    main()
