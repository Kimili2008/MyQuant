"""European Black-Scholes, Monte Carlo, and discrete delta-hedging utilities."""
from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, log, sqrt

import numpy as np


def normal_cdf(value: float | np.ndarray) -> float | np.ndarray:
    return 0.5 * (1.0 + np.vectorize(erf)(np.asarray(value) / sqrt(2.0)))


def normal_pdf(value: float | np.ndarray) -> float | np.ndarray:
    value = np.asarray(value)
    return np.exp(-0.5 * value * value) / sqrt(2.0 * np.pi)


@dataclass(frozen=True)
class Option:
    spot: float
    strike: float
    rate: float
    volatility: float
    maturity: float
    kind: str = "call"

    def _d1_d2(self, spot: float | None = None, maturity: float | None = None, volatility: float | None = None) -> tuple[float, float]:
        spot = self.spot if spot is None else spot
        maturity = self.maturity if maturity is None else maturity
        volatility = self.volatility if volatility is None else volatility
        if maturity <= 0 or volatility <= 0:
            return float("inf") if spot > self.strike else float("-inf"), float("inf") if spot > self.strike else float("-inf")
        d1 = (log(spot / self.strike) + (self.rate + 0.5 * volatility ** 2) * maturity) / (volatility * sqrt(maturity))
        return d1, d1 - volatility * sqrt(maturity)

    def price(self, spot: float | None = None, maturity: float | None = None, volatility: float | None = None) -> float:
        spot = self.spot if spot is None else spot
        maturity = self.maturity if maturity is None else maturity
        volatility = self.volatility if volatility is None else volatility
        if maturity <= 0:
            payoff = max(spot - self.strike, 0.0) if self.kind == "call" else max(self.strike - spot, 0.0)
            return payoff
        d1, d2 = self._d1_d2(spot, maturity, volatility)
        discount = exp(-self.rate * maturity)
        if self.kind == "call":
            return float(spot * normal_cdf(d1) - self.strike * discount * normal_cdf(d2))
        return float(self.strike * discount * normal_cdf(-d2) - spot * normal_cdf(-d1))

    def delta(self, spot: float | None = None, maturity: float | None = None) -> float:
        spot = self.spot if spot is None else spot
        maturity = self.maturity if maturity is None else maturity
        if maturity <= 0:
            if self.kind == "call":
                return float(spot > self.strike)
            return -float(spot < self.strike)
        d1, _ = self._d1_d2(spot, maturity)
        return float(normal_cdf(d1) if self.kind == "call" else normal_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return float(normal_pdf(d1) / (self.spot * self.volatility * sqrt(self.maturity)))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return float(self.spot * normal_pdf(d1) * sqrt(self.maturity) / 100.0)

    def theta(self) -> float:
        d1, d2 = self._d1_d2()
        first = -self.spot * normal_pdf(d1) * self.volatility / (2.0 * sqrt(self.maturity))
        if self.kind == "call":
            second = -self.rate * self.strike * exp(-self.rate * self.maturity) * normal_cdf(d2)
        else:
            second = self.rate * self.strike * exp(-self.rate * self.maturity) * normal_cdf(-d2)
        return float((first + second) / 365.0)


def finite_difference_delta(option: Option, bump: float = 0.01) -> float:
    return (option.price(spot=option.spot + bump) - option.price(spot=option.spot - bump)) / (2.0 * bump)


def monte_carlo_price(option: Option, paths: int = 100_000, seed: int = 7) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    terminal = option.spot * np.exp((option.rate - 0.5 * option.volatility ** 2) * option.maturity + option.volatility * sqrt(option.maturity) * rng.standard_normal(paths))
    payoff = np.maximum(terminal - option.strike, 0.0) if option.kind == "call" else np.maximum(option.strike - terminal, 0.0)
    discounted = exp(-option.rate * option.maturity) * payoff
    return float(discounted.mean()), float(discounted.std(ddof=1) / sqrt(paths))


def simulate_short_call_hedge(option: Option, realised_volatility: float, rebalance_every: int = 1, paths: int = 10_000, steps: int = 252, seed: int = 7, jump_probability: float = 0.0, jump_size: float = -0.08) -> np.ndarray:
    """P&L of selling one call and delta hedging with a model-volatility delta."""
    rng = np.random.default_rng(seed)
    dt = option.maturity / steps
    spots = np.full(paths, option.spot, dtype=float)
    delta = np.full(paths, option.delta(), dtype=float)
    cash = np.full(paths, option.price() - option.delta() * option.spot, dtype=float)
    for step in range(1, steps + 1):
        shocks = rng.standard_normal(paths)
        spots *= np.exp((option.rate - 0.5 * realised_volatility ** 2) * dt + realised_volatility * sqrt(dt) * shocks)
        if jump_probability > 0:
            spots *= np.where(rng.random(paths) < jump_probability * dt, 1.0 + jump_size, 1.0)
        cash *= exp(option.rate * dt)
        if step % rebalance_every == 0 and step < steps:
            remaining = option.maturity - step * dt
            d1 = (np.log(spots / option.strike) + (option.rate + 0.5 * option.volatility ** 2) * remaining) / (option.volatility * sqrt(remaining))
            new_delta = normal_cdf(d1)
            cash -= (new_delta - delta) * spots
            delta = new_delta
    payoff = np.maximum(spots - option.strike, 0.0)
    return cash + delta * spots - payoff
