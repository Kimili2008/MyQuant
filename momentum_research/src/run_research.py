"""Run the ETF momentum research design and write reproducible outputs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from data import DEFAULT_TICKERS, download_universe, load_prices
from strategy import performance_metrics, run_strategies


def period_metrics(returns: pd.DataFrame, turnover: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    rows = {}
    for name in returns.columns:
        mask = (returns.index >= start) & (returns.index <= end)
        rows[name] = performance_metrics(returns.loc[mask, name], turnover.loc[mask, name])
    return pd.DataFrame(rows).T


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--start", default="2011-01-01")
    parser.add_argument("--end", default="2026-08-31")
    parser.add_argument("--cost-bps", type=float, default=10.0)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    raw_dir, results_dir = root / "data" / "raw", root / "results"
    if args.download:
        download_universe(DEFAULT_TICKERS, args.start, args.end, raw_dir)
    prices = load_prices(raw_dir, DEFAULT_TICKERS).loc[args.start:args.end].dropna(axis=1, how="any")
    returns, turnover, weights = run_strategies(prices, args.cost_bps)
    results_dir.mkdir(exist_ok=True)
    metrics = pd.concat({
        "research_2011_2018": period_metrics(returns, turnover, "2011-01-01", "2018-12-31"),
        "oos_2019_2026": period_metrics(returns, turnover, "2019-01-01", args.end),
        "full_sample": period_metrics(returns, turnover, args.start, args.end),
    }, axis=1)
    metrics.to_csv(results_dir / "metrics.csv")
    ((1.0 + returns).cumprod()).to_csv(results_dir / "wealth_index.csv")
    turnover.to_csv(results_dir / "daily_turnover.csv")
    for name, frame in weights.items():
        frame.to_csv(results_dir / f"weights_{name.lower().replace(' ', '_')}.csv")
    summary = {"start": str(prices.index.min().date()), "end": str(prices.index.max().date()), "tickers": list(prices.columns), "cost_bps": args.cost_bps}
    (results_dir / "research_summary.json").write_text(json.dumps(summary, indent=2))
    print(metrics.round(4).to_string())


if __name__ == "__main__":
    main()
