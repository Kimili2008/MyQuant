from __future__ import annotations

import csv
from pathlib import Path

from option_models import Option, finite_difference_delta, monte_carlo_price, simulate_short_call_hedge


def main() -> None:
    option = Option(spot=100.0, strike=100.0, rate=0.04, volatility=0.25, maturity=1.0)
    mc_price, mc_se = monte_carlo_price(option, paths=100_000)
    rows = [
        ["analytical_call_price", option.price()],
        ["monte_carlo_price", mc_price],
        ["monte_carlo_standard_error", mc_se],
        ["analytical_delta", option.delta()],
        ["finite_difference_delta", finite_difference_delta(option)],
        ["gamma", option.gamma()],
        ["vega_per_1pct", option.vega()],
        ["theta_per_day", option.theta()],
    ]
    for name, realised, frequency, jump_probability in [
        ("daily_matched_vol", 0.25, 1, 0.0),
        ("weekly_matched_vol", 0.25, 5, 0.0),
        ("daily_higher_realised_vol", 0.35, 1, 0.0),
        ("daily_jump_risk", 0.25, 1, 0.15),
    ]:
        pnl = simulate_short_call_hedge(option, realised, rebalance_every=frequency, jump_probability=jump_probability)
        rows.extend([[f"{name}_mean_pnl", pnl.mean()], [f"{name}_p05_pnl", __import__("numpy").quantile(pnl, 0.05)]])
    result_dir = Path(__file__).resolve().parents[1] / "results"
    result_dir.mkdir(exist_ok=True)
    with (result_dir / "lab_summary.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)
    for row in rows:
        print(f"{row[0]}: {row[1]:.6f}")


if __name__ == "__main__":
    main()
