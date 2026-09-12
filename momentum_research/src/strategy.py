"""Long-only, monthly 12-1 momentum research functions."""
from __future__ import annotations

import numpy as np
import pandas as pd


def monthly_rebalance_dates(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    return pd.Series(index=index, data=index).groupby(index.to_period("M")).max().to_numpy()


def twelve_one_signal(prices: pd.DataFrame, lookback: int = 252, skip: int = 21) -> pd.DataFrame:
    return prices.shift(skip).div(prices.shift(lookback)).sub(1.0)


def _weights_at_date(prices: pd.DataFrame, date: pd.Timestamp, mode: str, top_n: int, spy: str) -> pd.Series:
    signal = twelve_one_signal(prices.loc[:date]).iloc[-1].dropna()
    columns = prices.columns
    weights = pd.Series(0.0, index=columns)
    if mode == "equal_weight":
        valid = prices.loc[date].dropna().index
        weights.loc[valid] = 1.0 / len(valid)
        return weights
    selected = signal.nlargest(min(top_n, len(signal))).index
    if len(selected) == 0:
        return weights
    if mode == "momentum_equal":
        weights.loc[selected] = 1.0 / len(selected)
        return weights
    volatility = prices.loc[:date, selected].pct_change().tail(63).std(ddof=1) * np.sqrt(252)
    inverse_vol = (1.0 / volatility.replace(0.0, np.nan)).dropna()
    if inverse_vol.empty:
        return weights
    weights.loc[inverse_vol.index] = inverse_vol / inverse_vol.sum()
    if mode == "momentum_regime":
        spy_history = prices.loc[:date, spy].dropna()
        if len(spy_history) < 200 or spy_history.iloc[-1] <= spy_history.tail(200).mean():
            weights[:] = 0.0
    return weights


def rebalance_weights(prices: pd.DataFrame, mode: str, top_n: int = 6, spy: str = "SPY") -> pd.DataFrame:
    if spy not in prices.columns:
        raise KeyError(f"{spy} must be included in prices")
    dates = monthly_rebalance_dates(prices.index)
    rows = {date: _weights_at_date(prices, date, mode, top_n, spy) for date in dates}
    rebalance = pd.DataFrame.from_dict(rows, orient="index").reindex(columns=prices.columns).fillna(0.0)
    # A month-end close signal cannot be traded at that same close.
    daily = rebalance.reindex(prices.index).ffill().shift(1).fillna(0.0)
    return daily


def portfolio_returns(prices: pd.DataFrame, weights: pd.DataFrame, cost_bps: float = 10.0) -> tuple[pd.Series, pd.Series]:
    returns = prices.pct_change().fillna(0.0)
    weights = weights.reindex(index=returns.index, columns=returns.columns).fillna(0.0)
    gross = (weights * returns).sum(axis=1)
    turnover = weights.sub(weights.shift(1).fillna(0.0)).abs().sum(axis=1)
    costs = turnover * (cost_bps / 10_000.0)
    return gross.sub(costs).rename("net_return"), turnover.rename("one_way_turnover")


def performance_metrics(returns: pd.Series, turnover: pd.Series) -> dict[str, float]:
    returns = returns.dropna()
    if returns.empty:
        return {key: float("nan") for key in ["total_return", "cagr", "annualised_volatility", "sharpe", "max_drawdown", "annual_turnover"]}
    wealth = (1.0 + returns).cumprod()
    years = len(returns) / 252.0
    annual_return = wealth.iloc[-1] ** (1.0 / years) - 1.0 if years > 0 else np.nan
    annual_volatility = returns.std(ddof=1) * np.sqrt(252)
    sharpe = returns.mean() * 252 / annual_volatility if annual_volatility else np.nan
    drawdown = wealth.div(wealth.cummax()).sub(1.0)
    return {
        "total_return": wealth.iloc[-1] - 1.0,
        "cagr": annual_return,
        "annualised_volatility": annual_volatility,
        "sharpe": sharpe,
        "max_drawdown": drawdown.min(),
        "annual_turnover": turnover.sum() / years if years > 0 else np.nan,
    }


def run_strategies(prices: pd.DataFrame, cost_bps: float = 10.0) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, pd.DataFrame]]:
    modes = ["equal_weight", "momentum_equal", "momentum_inverse_vol", "momentum_regime"]
    labels = {
        "equal_weight": "Equal weight",
        "momentum_equal": "12-1 momentum",
        "momentum_inverse_vol": "Momentum inverse vol",
        "momentum_regime": "Momentum regime filter",
    }
    all_returns, all_turnover, all_weights = {}, {}, {}
    for mode in modes:
        normalized_mode = "momentum_inverse_vol" if mode == "momentum_inverse_vol" else mode
        weights = rebalance_weights(prices, normalized_mode)
        net_returns, turnover = portfolio_returns(prices, weights, cost_bps)
        all_returns[labels[mode]] = net_returns
        all_turnover[labels[mode]] = turnover
        all_weights[labels[mode]] = weights
    return pd.DataFrame(all_returns), pd.DataFrame(all_turnover), all_weights
