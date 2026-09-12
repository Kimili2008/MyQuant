"""Public-price download and local cache utilities."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

DEFAULT_TICKERS = [
    "SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "IEF", "SHY", "HYG", "LQD",
    "GLD", "SLV", "DBC", "USO", "UUP", "XLE", "XLF", "XLK", "XLV", "XLY",
    "XLP", "XLI", "XLB", "XLU",
]


def _epoch(date_text: str) -> int:
    return int(datetime.fromisoformat(date_text).replace(tzinfo=timezone.utc).timestamp())


def download_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download daily adjusted close from Yahoo Finance's public chart endpoint."""
    query = urlencode({"period1": _epoch(start), "period2": _epoch(end) + 86_400, "interval": "1d", "events": "history"})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 MyQuant educational research"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    result = payload["chart"]["result"][0]
    stamps = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_localize(None).normalize()
    quote = result["indicators"]["quote"][0]
    adjusted = result["indicators"].get("adjclose", [{"adjclose": quote["close"]}])[0]["adjclose"]
    frame = pd.DataFrame({"date": stamps, "close": quote["close"], "adjusted_close": adjusted})
    frame = frame.dropna(subset=["adjusted_close"]).drop_duplicates("date").sort_values("date")
    return frame


def download_universe(tickers: list[str], start: str, end: str, output_dir: Path, pause_seconds: float = 0.15) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for ticker in tickers:
        frame = download_ticker(ticker, start, end)
        frame.to_csv(output_dir / f"{ticker}.csv", index=False)
        time.sleep(pause_seconds)


def load_prices(raw_dir: Path, tickers: list[str]) -> pd.DataFrame:
    series = []
    for ticker in tickers:
        path = raw_dir / f"{ticker}.csv"
        if not path.exists():
            continue
        frame = pd.read_csv(path, parse_dates=["date"])
        series.append(frame.set_index("date")["adjusted_close"].rename(ticker))
    if not series:
        raise FileNotFoundError("No cached price files found. Run with --download first.")
    prices = pd.concat(series, axis=1).sort_index().ffill(limit=5)
    return prices
