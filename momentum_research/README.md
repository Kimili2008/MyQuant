# ETF Momentum Research

Research question: does volatility scaling and an SPY 200-day moving-average regime filter improve a long-only 12-1 ETF momentum strategy after 10 bps one-way transaction costs?

## Run

```bash
python3 -m unittest discover -s tests -v
python3 src/run_research.py --download --end 2026-08-31
```

The run caches adjusted-close history in `data/raw/` and writes metrics, wealth indices, monthly weights, and a JSON research summary into `results/`.

## Design fixed before results

- Universe: liquid US-listed asset-class and sector ETFs with long trading histories.
- Research period: 2011-01-01 to 2018-12-31.
- Out-of-sample period: 2019-01-01 to 2026-08-31.
- Signal: return from 252 to 21 trading days before each month-end.
- Portfolios: equal weight, top-six equal-weight momentum, top-six inverse-volatility momentum, and inverse-volatility momentum with SPY above its 200-day moving average.
- Execution: month-end signals become active on the following trading day.
- Costs: 10 bps times one-way turnover.

## Interpretation

This is a research exercise. ETF selection, data availability, parameter choice, and the lack of a point-in-time constituent database can bias results. It is not an investment recommendation.
